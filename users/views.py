from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, LoginForm
from base.models import Profile


#register a user
def register(request):

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            var = form.save()
            username = form.cleaned_data.get('username')
            profile = Profile.objects.create(user=var)
            message = messages.success(request, f'Your account has been created! You can now log in')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


#login a user
def loginUser(request):
    message = None
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user != None:
                login(request, user)
                return redirect('home')
            else:
                message = messages.warning(request, 'invalid credentials')
        else:
            message = messages.warning(request, 'Error in validating form!')
    
    form = LoginForm()
    context = {'form': form, 'message': message}
    return render(request, 'users/login.html', context)


#logout the user
def logoutUser(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')