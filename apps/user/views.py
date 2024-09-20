from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'Successfully logged in.')
                return redirect('dashboard')  # Redirect to the dashboard after login
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'user/auth/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'user/auth/register.html', {'form': form})



def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out.')
    return redirect('index')  # Redirect to the index page after logout
