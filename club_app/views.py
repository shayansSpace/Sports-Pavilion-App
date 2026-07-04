from django.shortcuts import render, redirect, get_object_or_404 #display pages and navigate
from django.contrib.auth.models import User #django's built in user model
from django.db.models import Q # For OR Queries
from django.contrib.auth import logout, authenticate, login #authentication functions
from django.contrib import messages #messages framework
from django.contrib.auth.decorators import login_required #login required decorator
from django.http import JsonResponse # To return asynchronous AJAX background data
#import tables from models.py
from .models import Member
from .models import MembershipPlan, Member, MemberPhone, PlayUnit, Visitor, VisitorPhone, Booking, VisitorBooking, MemberBooking
from datetime import date

# @login_required(login_url='login') # If anonymous, go to /login
def index(request):
    is_member = False
    has_gym = False
    if request.user.is_authenticated:
        member_profile = Member.objects.filter(mem_email=request.user.email).first()
        if member_profile:
            is_member = True
            # Safely check if their plan covers gym access
            if member_profile.plan and member_profile.plan.gym_access:
                has_gym = True
    context = {'title': 'Sports Pavilion - Home', 'is_member': is_member, 'has_gym': has_gym}
    return render(request, 'index.html', context)

def registerUser(request):
    if request.method == 'POST':
        u_name = request.POST.get('username')
        email = request.POST.get('email')
        p_word = request.POST.get('password')
        
        # 1. Validation: Check if username already exists
        if User.objects.filter(username=u_name).exists():
            messages.error(request, "Username is already taken!")
            return redirect('login') # Sends them back to try again
            
        # 2. Magic Creation: create_user automatically hashes the password safely
        user = User.objects.create_user(username=u_name, email=email, password=p_word)
        user.save()
        
        # 3. Seamless UX: Log them in instantly right after registration
        login(request, user)
        
        # 4. Set the 2-week cookie persistence you requested
        request.session.set_expiry(1209600) 
        
        messages.success(request, f"Welcome to Sports Pavilion, {user.username}! Your account is ready.")
        return redirect('home') # Standard users go to the index page
        
    return redirect('login')

def about(request):
    context = {'title': 'Sports Pavilion - About Us'}
    return render(request, 'about.html', context)

@login_required(login_url='login') # If anonymous, go to /login
def member_list(request):
    # 1. Catch the text from your HTML form (name="q")
    query = request.GET.get('q', '').strip()
    
    #Fetch all members ordered by member_id descending (newest first)
    members = Member.objects.all().prefetch_related('phones').order_by('-member_id')

    # 3. Apply the filter ONLY if the user typed something
    if query:
        # The Engineering Trick: Handling the "M-001" ID format
        # If they type "M-005", we strip the "M-" to just search the integer "5"
        clean_id_query = query.upper().replace('M-', '').lstrip('0')
        
        # 4. The SQL "OR" Logic
        members = members.filter(
            Q(mem_first_name__icontains=query) | 
            Q(mem_last_name__icontains=query) |
            Q(mem_email__icontains=query) |
            Q(member_id__icontains=clean_id_query if clean_id_query else query)
        )
    context = {'title': 'Sports Pavilion - Member List',
               'members': members, # This is what the {% for m in members %} loop uses
               'query': query
               }
    return render(request, 'member_list.html', context)

def member_profile(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    context = {
        'title': f"Sports Pavilion - {member.full_name}",
        'member': member,
    }
    return render(request, 'member_profile.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        u_name = request.POST.get('username').strip()
        p_word = request.POST.get('password')
        user = authenticate(username=u_name, password=p_word)
    
        if user is not None:
            login(request, user)
            request.session.set_expiry(1209600) # 2 weeks in seconds

            if user.is_staff:
                return redirect('member_list') # Redirect Admin to /members
            else:
                messages.success(request, f"Welcome {user.username}!")
                return redirect('home') #return to index page for regular users 
        else:
            context = {'title': 'Login'}
            messages.error(request, "Invalid username or password")
            return render(request, 'login.html', context)
        
    context = {'title': 'Login'}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login')


@login_required(login_url='login')
def become_member(request):
    # Security check: Match user email to see if they already have a member profile
    if Member.objects.filter(mem_email=request.user.email).exists():
        messages.info(request, "You are already recorded as an active member!")
        return redirect('home')

    if request.method == 'POST':
        plan_id = request.POST.get('plan')
        phone = request.POST.get('phone')
        
        # 1. Create the Member entry
        new_member = Member.objects.create(
            plan_id=plan_id,
            mem_first_name=request.POST.get('first_name'),
            mem_last_name=request.POST.get('last_name'),
            mem_email=request.user.email,
            mem_join_date=date.today()
        )
        
        # 2. Create the Multi-valued attribute entry (Phone table)
        MemberPhone.objects.create(member=new_member, phone_number=phone)
        
        messages.success(request, "Membership activated successfully!")
        return redirect('home')

    plans = MembershipPlan.objects.all()
    return render(request, 'become_member.html', {'plans': plans})


@login_required(login_url='login')
def book_visitor(request):
    if request.method == 'POST':
        play_unit_id = request.POST.get('play_unit')
        target_date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Conflict Check
        conflict = Booking.objects.filter(
            play_unit_id=play_unit_id,
            booking_date=target_date,
            bk_start_time__lt=end_time,
            bk_end_time__gt=start_time
        ).exists()

        if conflict:
            # CHANGED: Return JSON error statement because frontend uses Javascript fetch() tracking
            return JsonResponse({'success': False, 'error': 'This time slot is already occupied!'})

        # Step 1: Create the Visitor profile
        visitor = Visitor.objects.create(
            vis_first_name=request.POST.get('first_name'),
            vis_last_name=request.POST.get('last_name')
        )
        # Step 2: Save visitor phone
        VisitorPhone.objects.create(visitor=visitor, phone_number=request.POST.get('phone'))

        # Step 3: Create the core Booking transaction 
        booking = Booking.objects.create(
            play_unit_id=play_unit_id,
            booking_date=target_date,
            bk_start_time=start_time,
            bk_end_time=end_time
        )

        # Step 4: Link booking to visitor via 3NF split table
        VisitorBooking.objects.create(booking=booking, visitor=visitor)

        # Calculate a mock/sample total price for the PDF script matching (e.g. rate or placeholder flat rate)
        rate = booking.play_unit.facility.sp_hourly_rate if booking.play_unit else 1000
        total_calculated = f"Rs. {rate}"

        # CHANGED: Return complete JsonResponse containing parameters needed for the PDF template generator
        return JsonResponse({
            'success': True,
            'booking_id': booking.booking_id,
            'total_price': total_calculated,
            'message': 'Your walk-in guest reservation is completely secured!'
        })
    
    # --- GET REQUEST LOGIC ---
    target_date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    play_units = PlayUnit.objects.filter(unit_status='Available')
    
    if target_date and start_time and end_time:
        conflicting_unit_ids = Booking.objects.filter(
            booking_date=target_date,
            bk_start_time__lt=end_time,
            bk_end_time__gt=start_time
        ).values_list('play_unit_id', flat=True)
        
        play_units = play_units.exclude(unit_id__in=conflicting_unit_ids)

        # CHANGED: If background AJAX is pulling available arrays, send back clean JSON elements
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            units_data = [
                {
                    'unit_id': u.unit_id,
                    'unit_num': u.unit_num,
                    'facility_name': u.facility.facility_name,
                    'hourly_rate': str(u.facility.sp_hourly_rate)
                } for u in play_units
            ]
            return JsonResponse(units_data, safe=False)

    context = {
        'play_units': play_units,
        'date': target_date,
        'start_time': start_time,
        'end_time': end_time
    }
    return render(request, 'book_visitor.html', context)


@login_required(login_url='login')
def book_member(request):
    current_member = Member.objects.filter(mem_email=request.user.email).first()
    if not current_member:
        messages.error(request, "Access Denied. You must subscribe to a plan first!")
        return redirect('become_member')

    if request.method == 'POST':
        play_unit_id = request.POST.get('play_unit')
        target_date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        # Conflict check
        if Booking.objects.filter(play_unit_id=play_unit_id, booking_date=target_date, bk_start_time__lt=end_time, bk_end_time__gt=start_time).exists():
            # CHANGED: Return JSON structure if you move book_member over to the fetch layout
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
                return JsonResponse({'success': False, 'error': 'Slot already booked.'})
            messages.error(request, "Slot already booked.")
            return redirect('book_member')

        # Step 1: Create transaction record
        booking = Booking.objects.create(
            play_unit_id=play_unit_id,
            booking_date=target_date,
            bk_start_time=start_time,
            bk_end_time=end_time
        )

        # Step 2: Link to member
        MemberBooking.objects.create(booking=booking, member=current_member)

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'booking_id': booking.booking_id,
                'total_price': "Included in Membership Plan",
                'message': f"Slot booked under Member ID: {current_member.member_id}"
            })

        messages.success(request, f"Slot booked under Member ID: {current_member.member_id}")
        return redirect('home')

    # --- CHANGED: Added dynamic timeframe filter system to matching member paths ---
    target_date = request.GET.get('date')
    start_time = request.GET.get('start_time')
    end_time = request.GET.get('end_time')

    play_units = PlayUnit.objects.filter(unit_status='Available')
    
    if target_date and start_time and end_time:
        conflicting_unit_ids = Booking.objects.filter(
            booking_date=target_date,
            bk_start_time__lt=end_time,
            bk_end_time__gt=start_time
        ).values_list('play_unit_id', flat=True)
        
        play_units = play_units.exclude(unit_id__in=conflicting_unit_ids)

        # AJAX Interceptor: Returns structured arrays if background listener triggers query refresh
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            units_data = [
                {
                    'unit_id': u.unit_id,
                    'unit_num': u.unit_num,
                    'facility_name': u.facility.facility_name,
                    'hourly_rate': str(u.facility.sp_hourly_rate)
                } for u in play_units
            ]
            return JsonResponse(units_data, safe=False)

    context = {
        'play_units': play_units,
        'date': target_date,
        'start_time': start_time,
        'end_time': end_time
    }
    return render(request, 'book_member.html', context)

# =========================================================================
# === ADMIN DASHBOARD PLACEHOLDERS (Add to the bottom of views.py) ======
# =========================================================================

@login_required(login_url='login')
def member_upsert(request, member_id=None):
    """Handles both adding a new member and editing an existing one."""
    if member_id:
        return JsonResponse({'status': 'placeholder', 'message': f'Editing Member {member_id}'})
    return JsonResponse({'status': 'placeholder', 'message': 'Adding a New Member'})

@login_required(login_url='login')
def delete_member(request, member_id):
    """Handles removing a member profile record from the database."""
    return JsonResponse({'status': 'placeholder', 'message': f'Deleting Member {member_id}'})

@login_required(login_url='login')
def staff_list(request):
    """Displays directory of staff and management profiles."""
    return JsonResponse({'status': 'placeholder', 'message': 'Staff Directory List'})

@login_required(login_url='login')
def staff_create(request):
    """Onboards a new staff user profile."""
    return JsonResponse({'status': 'placeholder', 'message': 'Onboarding New Staff'})

@login_required(login_url='login')
def staff_update(request, staff_id):
    """Modifies access or detail records for a specific staff ID."""
    return JsonResponse({'status': 'placeholder', 'message': f'Updating Staff {staff_id}'})

@login_required(login_url='login')
def staff_delete(request, staff_id):
    """Removes a staff profile from active directories."""
    return JsonResponse({'status': 'placeholder', 'message': f'Removing Staff {staff_id}'})