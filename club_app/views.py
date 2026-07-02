from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import transaction
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
    Member,          MembershipPlan,    MemberPhone,
    PlayUnit,        Visitor,           VisitorPhone,
    Booking,         VisitorBooking,    MemberBooking,
    Payment,         BookingPayment,    MembershipPayment,
    SportsFacility, Staff, GymEquipment, GymTrainer
)


# ─────────────────────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────────────────────

def _calculate_price(play_unit, start_time_str, end_time_str):
    fmt   = "%H:%M"
    start = datetime.strptime(start_time_str, fmt)
    end   = datetime.strptime(end_time_str,   fmt)
    hours = Decimal(str((end - start).seconds / 3600))
    rate  = play_unit.facility.sp_hourly_rate
    return (rate * hours).quantize(Decimal("0.01"))


# ─────────────────────────────────────────────────────────────────────────────
# HOME
# ─────────────────────────────────────────────────────────────────────────────

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


# ─────────────────────────────────────────────────────────────────────────────
# AUTH
# ─────────────────────────────────────────────────────────────────────────────

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
    return redirect('home')


def about(request):
    return render(request, 'about.html', {'title': 'Sports Pavilion - About Us'})


# ─────────────────────────────────────────────────────────────────────────────
# BECOME A MEMBER
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def become_member(request):
    # Guard clause: already a member → bounce them out immediately
    if Member.objects.filter(mem_email=request.user.email).exists():
        messages.info(request, "You are already recorded as an active member!")
        return redirect('home')
 
    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        phone   = request.POST.get('phone')
        plan    = get_object_or_404(MembershipPlan, pk=plan_id)

        with transaction.atomic():
            # 1. Create Member row
            new_member = Member.objects.create(
                plan_id        = plan_id,
                mem_first_name = request.POST.get('first_name'),
                mem_last_name  = request.POST.get('last_name'),
                mem_email      = request.user.email, 
                mem_join_date  = date.today(),
            )
    
            # 2. Link phone number
            MemberPhone.objects.create(member=new_member, phone_number=phone)
    
            # 3. Payment record
            payment = Payment.objects.create(
                amount = plan.plan_price,
                payment_method = request.POST.get('payment_method', 'Cash'),
            )
            MembershipPayment.objects.create(
                payment = payment,
                member  = new_member,
                plan    = plan,
            )
 
        messages.success(request, f"Welcome, {new_member.mem_first_name}! Your membership is now active.")
        return redirect('home')
 
    plans = MembershipPlan.objects.all()
    return render(request, 'become_member.html', {'plans': plans})


# ─────────────────────────────────────────────────────────────────────────────
# BOOK — VISITOR
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def book_visitor(request):
    if request.method == 'POST':
        play_unit_id = request.POST.get('play_unit')
        target_date  = request.POST.get('date')
        start_time   = request.POST.get('start_time')
        end_time     = request.POST.get('end_time')

        play_unit = get_object_or_404(PlayUnit, pk=play_unit_id)

        conflict = Booking.objects.filter(
            play_unit_id      = play_unit_id,
            booking_date      = target_date,
            bk_start_time__lt = end_time,
            bk_end_time__gt   = start_time,
        ).exists()
        if conflict:
            return JsonResponse({'success': False, 'error': "This time slot is already occupied!"})

        with transaction.atomic():
            visitor = Visitor.objects.create(
                vis_first_name = request.POST.get('first_name'),
                vis_last_name  = request.POST.get('last_name'),
            )
            VisitorPhone.objects.create(visitor=visitor, phone_number=request.POST.get('phone'))

            booking = Booking.objects.create(
                play_unit     = play_unit,
                booking_date  = target_date,
                bk_start_time = start_time,
                bk_end_time   = end_time,
            )
            VisitorBooking.objects.create(booking=booking, visitor=visitor)

            total_price = _calculate_price(play_unit, start_time, end_time)

            payment = Payment.objects.create(
                amount         = total_price,
                payment_method = request.POST.get('payment_method', 'Cash'),
            )
            BookingPayment.objects.create(payment=payment, booking=booking)

        return JsonResponse({
            'success'    : True,
            'booking_id' : booking.booking_id,
            'total_price': str(total_price),   # ← JS uses this to fill the PDF receipt
            'message'    : "Your registration is completely done!",
        })

    play_units = (
        PlayUnit.objects
        .filter(unit_status='Available')
        .select_related('facility')
        .order_by('facility__facility_name', 'unit_num')
    )
    return render(request, 'book_visitor.html', {'play_units': play_units})


# ─────────────────────────────────────────────────────────────────────────────
# BOOK — MEMBER
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def book_member(request):
    current_member = Member.objects.filter(mem_email=request.user.email).first()
    if not current_member:
        messages.error(request, "Access Denied. You must subscribe to a plan first!")
        return redirect('home')
    if request.method == 'POST':
        play_unit_id = request.POST.get('play_unit')
        target_date  = request.POST.get('date')
        start_time   = request.POST.get('start_time')
        end_time     = request.POST.get('end_time')

        play_unit = get_object_or_404(PlayUnit, pk=play_unit_id)

        if Booking.objects.filter(
            play_unit_id      = play_unit_id,
            booking_date      = target_date,
            bk_start_time__lt = end_time,
            bk_end_time__gt   = start_time,
        ).exists():
            messages.error(request, "Slot already booked.")
            return redirect('book_member')

        with transaction.atomic():
            booking = Booking.objects.create(
                play_unit     = play_unit,
                booking_date  = target_date,
                bk_start_time = start_time,
                bk_end_time   = end_time,
            )
            MemberBooking.objects.create(booking=booking, member=current_member)

        messages.success(request, "Member booking reservation successful!")
        return redirect('home')

    play_units = (
        PlayUnit.objects
        .select_related('facility')
        .order_by('facility__facility_name', 'unit_num')
    )
    return render(request, 'book_member.html', {'play_units': play_units})


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN — MEMBER LIST
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def member_list(request):
    query   = request.GET.get('q', '').strip()
    members = (
        Member.objects
        .all()
        .select_related('plan')
        .prefetch_related('phones')
        .order_by('-member_id')
    )

    if query:
        clean_id_query = query.upper().replace('M-', '').lstrip('0')
        members = members.filter(
            Q(mem_first_name__icontains = query) |
            Q(mem_last_name__icontains  = query) |
            Q(mem_email__icontains      = query) |
            Q(member_id__exact = clean_id_query if clean_id_query.isdigit() else None)
        )

    context = {
        'title'  : 'Sports Pavilion - Management Console',
        'members': members,
        'query'  : query,
    }
    return render(request, 'member_list.html', context)


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN — MEMBER PROFILE
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def member_profile(request, member_id):
    member = get_object_or_404(
        Member.objects.select_related('plan').prefetch_related('phones'),
        pk=member_id,
    )
    return render(request, 'member_profile.html', {
        'title' : f"Sports Pavilion - {member.full_name}",
        'member': member,
    })


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN — MEMBER UPSERT (CREATE / EDIT)
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def member_upsert(request, member_id=None):
    member = get_object_or_404(Member, pk=member_id) if member_id else None

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name  = request.POST.get('last_name')
        email      = request.POST.get('email')
        plan_id    = request.POST.get('plan')
        phone_num  = request.POST.get('phone')
        plan       = get_object_or_404(MembershipPlan, pk=plan_id) if plan_id else None

        if member:
            member.mem_first_name = first_name
            member.mem_last_name  = last_name
            member.mem_email      = email
            member.plan           = plan
            member.save()

            phone_obj = member.phones.first()
            if phone_obj:
                phone_obj.phone_number = phone_num
                phone_obj.save()
            else:
                MemberPhone.objects.create(member=member, phone_number=phone_num)

            messages.success(request, f"Profile for {member.full_name} updated successfully.")
        else:
            member = Member.objects.create(
                mem_first_name = first_name,
                mem_last_name  = last_name,
                mem_email      = email,
                plan           = plan,
                mem_join_date  = timezone.now().date(),
            )
            MemberPhone.objects.create(member=member, phone_number=phone_num)
            messages.success(request, f"New record established for {member.full_name}.")

        return redirect('member_list')

    plans         = MembershipPlan.objects.all()
    current_phone = member.phones.first().phone_number if member and member.phones.exists() else ""

    return render(request, 'member_form.html', {
        'title'        : 'Modify Member Record' if member else 'Register New Member',
        'member'       : member,
        'plans'        : plans,
        'current_phone': current_phone,
    })


# ─────────────────────────────────────────────────────────────────────────────
# ADMIN — DELETE MEMBER
# ─────────────────────────────────────────────────────────────────────────────

@login_required(login_url='login')
def delete_member(request, member_id):
    if request.method == 'POST':
        member = get_object_or_404(Member, pk=member_id)
        name   = member.full_name
        member.delete()
        messages.success(request, f"Record for {name} completely deleted from database.")
    return redirect('member_list')

# ─────────────────────────────────────────────────────────────────────────────
# ADMIN — CRUD OPERATIONS FOR STAFF, PLAY UNITS, TRAINERS
# ─────────────────────────────────────────────────────────────────────────────
@login_required
def staff_list(request):
    # Ensure only staff/admins can access this
    if not request.user.is_staff:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    query = request.GET.get('q', '').strip()
    staff_members = Staff.objects.all().order_by('-staff_id') # Adjust ID field if necessary

    if query:
        staff_members = staff_members.filter(
            Q(staff_first_name__icontains=query) |
            Q(staff_last_name__icontains=query)  |
            Q(staff_role__icontains=query)
        )

    context = {
        'title': 'Manage Staff - Sports Pavilion',
        'staff_members': staff_members,
        'query': query,
    }
    return render(request, 'staff_list.html', context)


@login_required
def staff_create(request):
    if not request.user.is_staff:
        return redirect('home')

    if request.method == 'POST':
        # Safely pull values directly from raw HTML input name attributes
        first_name = request.POST.get('staff_first_name', '').strip()
        last_name = request.POST.get('staff_last_name', '').strip()
        role = request.POST.get('staff_role', '').strip()
        salary = request.POST.get('staff_salary', '0.00').strip()

        # Simple validation check
        if first_name and last_name and role:
            # Instantiate and map directly to your models.py column names
            new_staff = Staff(
                staff_first_name=first_name,
                staff_last_name=last_name,
                staff_role=role,
                staff_salary=salary if salary else 0.00
            )
            new_staff.save() # Commit changes straight to your database
            
            messages.success(request, "New staff member added successfully!")
            return redirect('staff_list')
        else:
            messages.error(request, "Please fill out all required fields.")

    context = {
        'title': 'Add New Staff'
    }
    return render(request, 'staff_create.html', context)


@login_required
def staff_update(request, staff_id):
    if not request.user.is_staff:
        return redirect('home')

    staff_member = get_object_or_404(Staff, pk=staff_id)
    
    if request.method == 'POST':
        # Overwrite the instance attributes using incoming raw template inputs
        staff_member.staff_first_name = request.POST.get('staff_first_name', '').strip()
        staff_member.staff_last_name = request.POST.get('staff_last_name', '').strip()
        staff_member.staff_role = request.POST.get('staff_role', '').strip()
        
        salary_val = request.POST.get('staff_salary', '0.00').strip()
        staff_member.staff_salary = salary_val if salary_val else 0.00
        
        if staff_member.staff_first_name and staff_member.staff_last_name:
            staff_member.save() # Run SQL UPDATE query statement automatically
            messages.success(request, f"Staff member '{staff_member.staff_first_name}' updated successfully!")
            return redirect('staff_list')
        else:
            messages.error(request, "First and Last names cannot be blank.")

    context = {
        'title': 'Edit Staff Member',
        'staff': staff_member # Pass object to pre-fill the value attribute fields
    }
    return render(request, 'staff_update.html', context)


@login_required
def staff_delete(request, staff_id):
    if not request.user.is_staff:
        return redirect('home')

    staff_member = get_object_or_404(Staff, pk=staff_id)
    
    # Deletes the record and immediately redirects to the list with a success message
    staff_member.delete()
    messages.success(request, "Staff member removed from the database.")
    return redirect('staff_list')