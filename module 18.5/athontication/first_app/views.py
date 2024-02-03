from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

# Create your views here.

def Home(request):
    return render(request, 'home.html')


def Singup(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            register_form = RegistrationForm(request.POST)
            if register_form.is_valid():
                messages.success(request, 'Account created Successfuly')
                register_form.save()
                print(register_form.cleaned_data)
        else:
            register_form = RegistrationForm()
        return render(request, 'singup.html', {'form' : register_form})
    else:
        return redirect('profile')


def Login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                name = form.cleaned_data['username']
                userpass = form.cleaned_data['password']
                user = authenticate(username = name, password = userpass)
                if user is not None:
                    login(request, user)
                    return redirect('profile')
        else:
            form = AuthenticationForm()
        return render(request, 'login.html', {'form' : form})
    else:
        return redirect('profile')
    

def Profile(request):
    if request.user.is_authenticated:
        return render(request, 'profile.html', {'user': request.user})
    else:
        return redirect('login')

def singn_out(request):
    logout(request)
    return redirect('login')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                # update_session_auth_hash(request, form.cleaned_data['user'])
                return redirect('profile')
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'passchange.html', {'form': form})
    else:
        return redirect('login')