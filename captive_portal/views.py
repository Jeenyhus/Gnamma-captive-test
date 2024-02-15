from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SplashForm
from .models import UserProfile
from .forms import UserProfileForm
import requests
import os
from dotenv import load_dotenv

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

            if authenticate_with_meraki(username, password):
                user = UserProfile.objects.get_or_create(username=username, email=email)[0]
                login(request, user) 
                return redirect('captive_portal:success')
            else:
                form.add_error(None, 'Invalid credentials. Please try again.')
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

def authenticate_with_meraki(username, email):
    """
    Authenticates the user with the Meraki API using the provided username and email.

    Args:
        username (str): The username of the user.
        email (str): The email address of the user.

    Returns:
        bool: True if the authentication is successful, False otherwise.
    """
    load_dotenv()

    meraki_api_url = 'https://api.meraki.com/api/v0/some/endpoint'
    meraki_api_key = os.getenv('MERAKI_API_KEY')

    headers = {'X-Cisco-Meraki-API-Key': meraki_api_key}
    payload = {'username': username, 'password': email}

    response = requests.post(meraki_api_url, headers=headers, data=payload)

    return response.status_code == 200