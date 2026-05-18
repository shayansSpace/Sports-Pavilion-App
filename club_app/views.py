from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, datetime, timedelta
from django.utils import timezone
from decimal import Decimal
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa

from .models import (
    Member, MembershipPlan, MemberPhone,
    PlayUnit, Visitor, VisitorPhone,
    Booking, VisitorBooking, MemberBooking,
    Payment, BookingPayment, MembershipPayment,
    SportsFacility
)


# ─────────────────────────────────────────
# HELPER: calculate price for a booking
# ─────────────────────────────────────────
def _calculate_price(play_unit, start_time_str, end_time_str):
    """
    Returns Decimal price = hourly_rate × hours booked.
    start_time_str / end_time_str are 'HH:MM' strings from the form.
    """
    fmt = "%H:%M"
    start = datetime.strptime(start_time_str, fmt)
    end   = datetime.strptime(end_time_str,   fmt)
    hours = Decimal(str((end - start).seconds / 3600))          # e.g. 1.5
    rate  = play_unit.facility.sp_hourly_rate                    # DecimalField
    return (rate * hours).quantize(Decimal("0.01"))


# ─────────────────────────────────────────
# HOME
# ─────────────────────────────────────────
def index(request):
    is_member = False
    has_gym   = False
    if request.user.is_authenticated:
        member_profile = Member.objects.filter(mem_email=request.user.email).first()
        if member_profile:
            is_member = True
            if member_profile.plan and member_profile.plan.gym_access:
                has_gym = True
    context = {
        'title'    : 'Sports Pavilion - Home',
        'is_member': is_member,
        'has_gym'  : has_gym,
    }
    return render(request, 'index.html', context)


# ─────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────
def registerUser(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        email  = request.POST.get('email')
        p_word = request.POST.get('password')

        if User.objects.filter(username=u_name).exists():
            messages.error(request, "Username is already taken!")
            return redirect('login')

        user = User.objects.create_user(username=u_name, email=email, password=p_word)
        user.save()
        login(request, user)
        request.session.set_expiry(1209600)
        messages.success(request, f"Welcome to Sports Pavilion, {user.username}!")
        return redirect('home')

    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        u_name = request.POST.get('username').strip()
        p_word = request.POST.get('password')
        user   = authenticate(username=u_name, password=p_word)

        if user is not None:
            login(request, user)
            request.session.set_expiry(1209600)
            return redirect('member_list') if user.is_staff else redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html', {'title': 'Login'})

    return render(request, 'login.html', {'title': 'Login'})


def logoutUser(request):
    logout(request)
    return redirect('/login')


def about(request):
    return render(request, 'about.html', {'title': 'Sports Pavilion - About Us'})


# ─────────────────────────────────────────
# BECOME A MEMBER  ➜  shows receipt after
# ─────────────────────────────────────────
@login_required(login_url='login')
def become_member(request):
    # Already a member? Bail out.
    existing = Member.objects.filter(mem_email=request.user.email).first()
    if existing:
        messages.info(request, "You are already recorded as an active member!")
        return redirect('home')

    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        phone   = request.POST.get('phone')
        plan    = get_object_or_404(MembershipPlan, pk=plan_id)

        # ── 1. Create the Member row ──────────────────────────────────────
        new_member = Member.objects.create(
            plan_id        = plan_id,
            mem_first_name = request.POST.get('first_name'),
            mem_last_name  = request.POST.get('last_name'),
            mem_email      = request.user.email,
            mem_join_date  = date.today(),
        )

        # ── 2. Multi-valued phone ─────────────────────────────────────────
        MemberPhone.objects.create(member=new_member, phone_number=phone)

        # ── 3. Payment record (3NF split) ─────────────────────────────────
        #    Payment core row  →  only amount / date / method
        payment = Payment.objects.create(
            amount         = plan.plan_price,
            payment_method = request.POST.get('payment_method', 'Cash'),
        )
        #    MembershipPayment junction row  →  ties payment to member + plan
        MembershipPayment.objects.create(
            payment = payment,
            member  = new_member,
            plan    = plan,
        )

        # ── 4. Build receipt data ─────────────────────────────────────────
        expiry_date = date.today() + timedelta(days=30 * plan.duration_months)

        receipt = {
            'member'      : new_member,
            'plan'        : plan,
            'payment'     : payment,
            'expiry_date' : expiry_date,
        }
        return render(request, 'membership_receipt.html', {
            'title'  : 'Membership Receipt',
            'receipt': receipt,
        })

    plans = MembershipPlan.objects.all()
    return render(request, 'become_member.html', {'plans': plans})


# ─────────────────────────────────────────
# BOOK — VISITOR  ➜  shows receipt with price
# ─────────────────────────────────────────
@login_required(login_url='login')
def book_visitor(request):
    if request.method == 'POST':
        play_unit_id = request.POST.get('play_unit')
        target_date  = request.POST.get('date')
        start_time   = request.POST.get('start_time')   
        end_time     = request.POST.get('end_time')     

        play_unit = get_object_or_404(PlayUnit, pk=play_unit_id)

        # Conflict check
        conflict = Booking.objects.filter(
            play_unit_id   = play_unit_id,
            booking_date   = target_date,
            bk_start_time__lt = end_time,
            bk_end_time__gt   = start_time,
        ).exists()
        if conflict:
            return JsonResponse({'success': False, 'error': "This time slot is already occupied!"})

        # 1. Visitor profile
        visitor = Visitor.objects.create(
            vis_first_name = request.POST.get('first_name'),
            vis_last_name  = request.POST.get('last_name'),
        )
        VisitorPhone.objects.create(visitor=visitor, phone_number=request.POST.get('phone'))

        # 2. Core booking row
        booking = Booking.objects.create(
            play_unit     = play_unit,
            booking_date  = target_date,
            bk_start_time = start_time,
            bk_end_time   = end_time,
        )

        # 3. 3NF junction: tie booking to visitor
        VisitorBooking.objects.create(booking=booking, visitor=visitor)

        # 4. Calculate price
        total_price = _calculate_price(play_unit, start_time, end_time)

        # 5. Payment record
        payment = Payment.objects.create(
            amount         = total_price,
            payment_method = request.POST.get('payment_method', 'Cash'),
        )
        BookingPayment.objects.create(payment=payment, booking=booking)

        return JsonResponse({
            'success': True,
            'booking_id': booking.booking_id,
            'message': "Your registration is completely done!"
        })

    play_units = PlayUnit.objects.filter(unit_status='Available').select_related('facility').order_by('facility__facility_name', 'unit_num')
    return render(request, 'book_visitor.html', {'play_units': play_units})


# ─────────────────────────────────────────
# BOOK — MEMBER  ➜  receipt without price
# ─────────────────────────────────────────
@login_required(login_url='login')
def book_member(request):
    current_member = Member.objects.filter(mem_email=request.user.email).first()
    if not current_member:
        return JsonResponse({'success': False, 'error': "Access Denied. You must subscribe to a plan first!"})

    if request.method == 'POST':
        play_unit_id = request.POST.get('play_unit')
        target_date  = request.POST.get('date')
        start_time   = request.POST.get('start_time')
        end_time     = request.POST.get('end_time')

        play_unit = get_object_or_404(PlayUnit, pk=play_unit_id)

        # Conflict check
        if Booking.objects.filter(
            play_unit_id      = play_unit_id,
            booking_date      = target_date,
            bk_start_time__lt = end_time,
            bk_end_time__gt   = start_time,
        ).exists():
            return JsonResponse({'success': False, 'error': "Slot already booked."})

        # 1. Core booking row
        booking = Booking.objects.create(
            play_unit     = play_unit,
            booking_date  = target_date,
            bk_start_time = start_time,
            bk_end_time   = end_time,
        )

        # 2. 3NF junction: tie booking to member
        MemberBooking.objects.create(booking=booking, member=current_member)

        return JsonResponse({
            'success': True,
            'booking_id': booking.booking_id,
            'message': "Member booking reservation successful!"
        })

    play_units = PlayUnit.objects.select_related('facility').order_by('facility__facility_name', 'unit_num')
    return render(request, 'book_member.html', {'play_units': play_units})

@login_required(login_url='login')
def member_list(request):
    query = request.GET.get('q', '').strip()
    
    # FIX: added select_related('plan') to eliminate N+1 query loops in the HTML table
    members = Member.objects.all().select_related('plan').prefetch_related('phones').order_by('-member_id')

    if query:
        clean_id_query = query.upper().replace('M-', '').lstrip('0')
        members = members.filter(
            Q(mem_first_name__icontains=query) |
            Q(mem_last_name__icontains=query)  |
            Q(mem_email__icontains=query)       |
            Q(member_id__exact=clean_id_query if clean_id_query.isdigit() else None)
        )

    context = {
        'title': 'Sports Pavilion - Management Console',
        'members': members,
        'query': query,
    }
    return render(request, 'member_list.html', context)


# ─── 2. PROFILE MANIFEST ─────────────────────────────────────────────────────
@login_required(login_url='login')
def member_profile(request, member_id):
    # Added select_related/prefetch_related optimization here as well
    member = get_object_or_404(
        Member.objects.select_related('plan').prefetch_related('phones'), 
        pk=member_id
    )
    return render(request, 'member_profile.html', {
        'title': f"Sports Pavilion - {member.full_name}",
        'member': member,
    })


# ─── 3. CREATE & UPDATE (UPSERT DATA FLOW) ──────────────────────────────────
@login_required(login_url='login')
def member_upsert(request, member_id=None):
    """Handles both creating a fresh member record and editing an existing one."""
    member = get_object_or_404(Member, pk=member_id) if member_id else None
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        plan_id = request.POST.get('plan')
        phone_num = request.POST.get('phone')

        plan = get_object_or_404(MembershipPlan, pk=plan_id) if plan_id else None

        if member:
            # Operational Update Pathway
            member.mem_first_name = first_name
            member.mem_last_name = last_name
            member.mem_email = email
            member.plan = plan
            member.save()
            
            # Sync corresponding phone record safely
            phone_obj = member.phones.first()
            if phone_obj:
                phone_obj.phone_number = phone_num
                phone_obj.save()
            else:
                MemberPhone.objects.create(member=member, phone_number=phone_num)
                
            messages.success(request, f"Profile for {member.full_name} updated successfully.")
        else:
            # Operational Insertion Pathway
            member = Member.objects.create(
                mem_first_name=first_name,
                mem_last_name=last_name,
                mem_email=email,
                plan=plan,
                mem_join_date=timezone.now().date()
            )
            MemberPhone.objects.create(member=member, phone_number=phone_num)
            messages.success(request, f"New record established for {member.full_name}.")

        return redirect('member_list')

    # GET Workflow: Render Form layout populating fields if editing
    plans = MembershipPlan.objects.all()
    current_phone = member.phones.first().phone_number if member and member.phones.exists() else ""
    
    return render(request, 'member_form.html', {
        'title': 'Modify Member Record' if member else 'Register New Member',
        'member': member,
        'plans': plans,
        'current_phone': current_phone
    })


# ─── 4. DESTRUCTION PIPELINE (DELETE) ────────────────────────────────────────
@login_required(login_url='login')
def delete_member(request, member_id):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=member_id)
        name = member.full_name
        member.delete()  # On Cascade database directives drop phone links automatically
        messages.success(request, f"Record for {name} completely purged from database.")
    return redirect('member_list')

def download_receipt(request, booking_id):
    """
    Renders an HTML layout on the server-side and converts it cleanly to a downloadable PDF.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    
    # Trace 3NF relationships to check if user is a Visitor or a Member
    visitor_link = VisitorBooking.objects.filter(booking=booking).select_related('visitor').first()
    member_link  = MemberBooking.objects.filter(booking=booking).select_related('member').first()
    
    context = {
        'booking': booking,
        'play_unit': booking.play_unit,
        'facility': booking.play_unit.facility,
    }
    
    if visitor_link:
        context['user_type'] = 'Visitor'
        context['customer_name'] = f"{visitor_link.visitor.vis_first_name} {visitor_link.visitor.vis_last_name}"
        # Extract billing info
        pay_link = BookingPayment.objects.filter(booking=booking).select_related('payment').first()
        context['amount_paid'] = pay_link.payment.amount if pay_link else 0.0
        context['payment_method'] = pay_link.payment.payment_method if pay_link else "Cash"
    else:
        context['user_type'] = 'Member'
        context['customer_name'] = f"{member_link.member.mem_first_name} {member_link.member.mem_last_name}" if member_link else "Valued Member"
        context['amount_paid'] = None # Hides price column for club members
        context['payment_method'] = "Membership Privilege Plan"

    # Convert HTML file markup cleanly into string data context
    html_string = render_to_string('receipt_pdf_template.html', context)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Receipt_B{booking.booking_id}.pdf"'
    
    # Process html content string directly into response binary file stream
    pisa_status = pisa.CreatePDF(html_string, dest=response)
    
    if pisa_status.err:
        return HttpResponse('Fatal error compilation failed within template matrix.', status=500)
    return response