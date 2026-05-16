from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login
from .models import Member
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url='login') # If anonymous, go to /login
def index(request):
    context = {'title': 'Sports Pavilion - Home'}
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