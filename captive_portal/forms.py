from django import forms
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')  # Include necessary fields for signup

class SplashForm(forms.Form):
    email = forms.EmailField()  # Add email field
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if not email or not password:
            raise forms.ValidationError("Email and password are required.")

    def authenticate_user(self):
        """
        Authenticates the user using provided email and password.
        """
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError("Invalid email or password.")
        return user
