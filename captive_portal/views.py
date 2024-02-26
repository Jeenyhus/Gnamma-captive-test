from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import SplashForm, SignUpForm
from .meraki_utils import get_organization_id, get_network_id, authenticate_meraki_user, grant_network_access

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
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            organization_id = get_organization_id()
            network_name = 'Gnamma Tech AP1'  # Replace with your network name
            network_id = get_network_id(organization_id, network_name)

            if network_id:
                if authenticate_meraki_user(network_id, email, password):
                    user = authenticate(email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('captive_portal:success')
                    else:
                        form.add_error(None, 'User authentication failed.')
                else:
                    form.add_error(None, 'Meraki authentication failed. Please try again.')
            else:
                form.add_error(None, 'Failed to fetch network ID.')
    else:
        form = SplashForm()

    request.session['redirect_url'] = request.GET.get('next', '/')
    return render(request, 'captive_portal/splash.html', {'form': form})

def sign_up_mk(request):
    """
    Renders the signup page and handles form submission.
    If the form is valid, saves the form data and redirects to the success page.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # Grant network access to the user
            network_name = 'Gnamma Tech AP1'  # Replace with your network name
            if not grant_network_access({'email': email, 'name': user.username, 'password': password}, network_name):
                form.add_error(None, 'Failed to grant network access.')
                return render(request, 'captive_portal/sign_up.html', {'form': form})

            # Authenticate user and redirect to success page
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('captive_portal:success')
            else:
                form.add_error(None, 'User authentication failed.')
    else:
        form = SignUpForm()

    return render(request, 'captive_portal/sign_up.html', {'form': form})
