from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from users.forms import RegisterForm, CustomRegitrationForm, LoginForm, AssignRoleForm, CreateGroupForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Prefetch
from events.models import Event, RSVP

def is_admin(user):
    return user.groups.filter(name='admin').exists()


def sign_up(request):
    form = CustomRegitrationForm()
    if request.method == 'POST':
        form = CustomRegitrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.is_active = False
            user.save()
            messages.success(request, "A Confirmation mail send. Please check your email!")
            return redirect('sign_up')
        else:
            print('Form is not valid')
    return render(request, 'registration/register.html', {"form":form})


def sign_in(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home_page')
    return render(request, 'registration/login.html', {"form": form}) 

@login_required
def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home_page') 


def activate_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('sign_in')
        else:
            return HttpResponse('Invalid Id or token')

    except User.DoesNotExist:
        return HttpResponse('User not found') 

@user_passes_test(is_admin, login_url='no_permission')
def admin_dashboard(request):
    users = User.objects.prefetch_related(
        Prefetch('groups', queryset=Group.objects.all(), to_attr='all_groups')
    ).all()
    for user in users:
        if user.all_groups:
            user.group_name = user.all_groups[0].name
        else:
            user.group_name = "No group assigned"
    return render(request, 'admin/admin_dashboard.html', {"users": users})

@user_passes_test(is_admin, login_url='no_permission')
def assign_role(request, user_id):
    user = User.objects.get(id=user_id)
    form = AssignRoleForm()
    if request.method == 'POST':
        form = AssignRoleForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user.groups.clear()  # Remove old roles
            user.groups.add(role)
            messages.success(request, f"User {user.username} has been assigned to the {role.name} role")
            return redirect('assign_role', user_id)

    return render(request, 'admin/assign_role.html', {"form": form})

@user_passes_test(is_admin, login_url='no_permission')
def create_group(request):
    form = CreateGroupForm()
    if request.method == "POST":
        form = CreateGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            messages.success(request, f"Group {group.name} has been created successfully")
            return redirect('create_group')
    return render(request, 'admin/create_group.html', {"form":form})

@user_passes_test(is_admin, login_url='no_permission')
def group_list(request):
    groups = Group.objects.prefetch_related('permissions').all()
    return render(request, 'admin/group_list.html', {"groups": groups})

#RSVP 
@login_required
def rsvp_event(request, id):
    event = Event.objects.prefetch_related('rsvps').select_related('category').get(id=id)
    if request.method == "POST":
        if not event.rsvps.filter(user=request.user).exists():
            RSVP.objects.create(user=request.user, event=event)
            messages.success(request, "You have successfully RSVP'd to the event!")
        else:
            messages.warning(request, "You have already RSVP'd to this event.")
    return redirect('view_detail', id=event.id)

@login_required
def cancel_rsvp(request, id):
    event = Event.objects.prefetch_related('rsvps').select_related('category').get(id=id)
    
    if request.method == "POST":
        rsvp = RSVP.objects.filter(user=request.user, event=event)
        if rsvp.exists():
            rsvp.delete()
            messages.success(request, "Your RSVP has been canceled.")
        else:
            messages.warning(request, "You have not RSVP'd to this event.")
    return redirect('view_detail', id=event.id)
