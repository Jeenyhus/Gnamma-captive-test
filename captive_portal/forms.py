from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'

        
class SplashForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'agreed_to_terms']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'agreed_to_terms': forms.CheckboxInput(),
        }

    def clean_agreed_to_terms(self):
        """
        Custom validation method for the 'agreed_to_terms' field.
        Raises a ValidationError if the user has not agreed to the terms.
        """
        agreed_to_terms = self.cleaned_data['agreed_to_terms']
        if not agreed_to_terms:
            raise forms.ValidationError("You must agree to the terms to proceed.")
        return agreed_to_terms
