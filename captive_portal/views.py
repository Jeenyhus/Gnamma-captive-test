from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SplashForm, UserProfileForm
from .models import UserProfile
from .meraki_utils import authenticate_with_meraki
from django.contrib.auth.decorators import login_required

@login_required
def success(request):
    """
    Renders the success page.
    """
    redirect_url = request.session.pop('redirect_url', '/')
    return redirect(redirect_url)

def splash_page(request):
    """
    Renders the splash page and handles form submission.
    If the form is valid and the user is authenticated, redirects to the success page.
    If the form is invalid or the user is not authenticated, renders the splash page with appropriate error messages.
    """
    if request.method == 'POST':
        form = SplashForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            user = authenticate_with_meraki(username, email)
            if user:
                login(request, user)
                return redirect('captive_portal:success')
            else:
                form.add_error(None, 'Invalid credentials. Please try again.')
    else:
        form = SplashForm()

    # Store the URL the user was trying to access before being redirected to the splash page
    request.session['redirect_url'] = request.GET.get('next', '/')

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
