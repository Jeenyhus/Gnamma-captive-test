from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    # Set default value for the role field to 'member'
    role = forms.ChoiceField(choices=[('guest', 'Guest'), ('member', 'Member'), ('admin', 'Admin')], initial='member')
    network_id = forms.CharField(max_length=100)
    network_name = forms.CharField(max_length=100)

class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)