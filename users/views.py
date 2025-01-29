from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from users.forms import RegisterForm, CustomRegitrationForm
from django.contrib.auth import login, authenticate, logout

def home(request):
    return render(request, 'registration/home.html')

def sign_up(request):
    form = CustomRegitrationForm()
    if request.method == 'POST':
        form = CustomRegitrationForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print('Form is not valid')
    return render(request, 'registration/register.html', {"form":form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Doc", username, password)
        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'registration/login.html') 

def sign_out(request):
    if request.method == 'POST':
        logout(request)
        return redirect('sign_in')    