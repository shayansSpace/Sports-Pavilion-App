from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import logout, authenticate, login
from .models import Member


# Create your views here.
def index(request):
    # if request.user.is_anonymous:
    #     return redirect('/login')
    context = {'title': 'Sports Pavilion - Home'}
    return render(request, 'index.html', context)

def services(request):
    context = {'title': 'Sports Pavilion - Services'}
    return render(request, 'services.html', context)

def about(request):
    context = {'title': 'Sports Pavilion - About Us'}
    return render(request, 'about.html', context)

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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
    
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            context = {'title': 'Login'}
            return render(request, 'login.html', context)
    context = {'title': 'Login'}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('/login')