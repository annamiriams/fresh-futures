from django.shortcuts import render, redirect
from .forms import RegisterUserForm
# Create your views here.
def registerView(request):
    # if the form is submitted
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
       
        # Handle the registration logic here
       
    return render(request, 'accounts/register.html')

def loginView(request):
    return render(request, 'accounts/login.html')

# Change this
def logoutView(request):
    return render(request, 'accounts/logout.html')