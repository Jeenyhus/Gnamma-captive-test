from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm
from .meraki_utils import authenticate_with_meraki, create_meraki_guest_user
import logging


logger = logging.getLogger(__name__)

def splash(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            if authenticate_with_meraki(email, password):
                user = authenticate(request, email=email)
                if user is not None:
                    login(request, user)
                    return redirect('success')
                else:
                    messages.error(request, "Django authentication failed.")
            else:
                messages.error(request, "Invalid Meraki credentials.")
    else:
        form = LoginForm()

    return render(request, 'splash.html', {'form': form})


def signup(request):
    success_message = ''
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            try:
                create_meraki_guest_user(user)
                success_message = 'An email with your credentials has been sent. Please check your inbox.'
                messages.success(request, success_message)
            except Exception as e:
                error_message = f'Failed to create Meraki guest user: {e}'
                messages.error(request, error_message)
                logger.error(error_message)
    else:
        form = SignupForm()

    return render(request, 'sign_up.html', {'form': form, 'success_message': success_message})

def success(request):
    return render(request, 'success.html')
