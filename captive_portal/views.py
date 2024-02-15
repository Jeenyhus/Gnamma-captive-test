from django.shortcuts import render, redirect
from .forms import SplashForm
from .models import UserProfile
from .forms import UserProfileForm

def splash_page(request):
    """
    Renders the splash page and handles form submission.
    If the form is valid and the user already exists, redirects to the success page.
    If the form is valid and the user does not exist, redirects to the signup page.
    """
    if request.method == 'POST':
        form = SplashForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            agreed_to_terms = form.cleaned_data['agreed_to_terms']

            # Check if user already exists
            user = UserProfile.objects.filter(username=username, email=email).first()

            if user:
                return redirect('captive_portal:success')
            else:
                return redirect('captive_portal:sign_up')
    else:
        form = SplashForm()
    return render(request, 'captive_portal/splash.html', {'form': form})

def sign_up(request):
    """
    Renders the signup page and handles form submission.
    If the form is valid, saves the form data and redirects to the success page.
    """
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            form.save() 
            return redirect('captive_portal:success')
    else:
        form = UserProfileForm()
    return render(request, 'captive_portal/sign_up.html', {'form': form})


def success(request):
    """
    Renders the success page.
    """
    return render(request, 'captive_portal/success.html')
