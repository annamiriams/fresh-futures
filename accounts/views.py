from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import RegisterUserForm

# Create your views here
def registerView(request):
    # If the form is submitted then the code below will run
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        
        if form.is_valid():
            # print("Form is valid")
            # form.save()
            # return redirect('login')
            user = form.save(commit=False)
            user.has_completed_onboarding = False
            user.save()
            return redirect('login')
        else:
            print("Form is not valid")
            messages.error(request, form.errors)
            return redirect('register')
        
    # Handle the registration logic here
    form = RegisterUserForm()
    context = {
        'form': form
    } 
    return render(request, 'accounts/register.html', context)

# Login User (View)
def loginView(request):
    # If the form is submitted then the code below will run
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # If the user is defined, means user exists and logs the user in
        if user is not None:
            # If the user is authenticated, log them in
            login(request, user)
            return redirect('home')
        else: # Invalid credentials
            # If authentication fails, show an error message
            messages.error(request, 'Invalid username or password.')
            return redirect('login')
    return render(request, 'accounts/login.html')

# Logout User (View)
def logoutView(request):
    logout(request)
    return redirect("home")