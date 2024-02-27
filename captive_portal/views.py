from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SignUpForm, AuthenticationForm
from .meraki_utils import create_user, authenticate_user_in_network
from django.http import HttpResponse
from .models import UserProfile, User


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
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            network_id = form.cleaned_data['network_id']

            # Authenticate user using Meraki API
            if authenticate_user_in_network(username, password, network_id):
                # Authentication successful, redirect to success page
                return redirect('success')  # Replace 'success_url' with the actual URL
            else:
                # Authentication failed, render the splash page with an error message
                return render(request, 'splash_page.html', {'form': form, 'error_message': 'Invalid credentials'})

    else:
        # If request method is not POST, render the splash page with the authentication form
        form = AuthenticationForm()
    
    return render(request, 'captive_portal/splash.html', {'form': form})

def sign_up_mk(request):
    """
    Renders the signup page and handles form submission.
    If the form is valid, saves the form data and redirects to the success page.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Process the form data
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            role = form.cleaned_data.get('role')
            network_id = form.cleaned_data.get('network_id')
            network_name = form.cleaned_data.get('network_name')

            # Call function to handle user sign-up and Meraki API interaction
            create_user(username, password, role, network_id, network_name)

            return HttpResponse("User created successfully")
    else:
        form = SignUpForm()
    
    return render(request, 'captive_portal/sign_up.html', {'form': form})
