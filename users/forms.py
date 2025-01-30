from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 
import re
from events.forms import StyleFormMixin
from django.contrib.auth.forms import AuthenticationForm

class RegisterForm(UserCreationForm): #here i use usercreation form
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


#custom resigtration form
class CustomRegitrationForm(StyleFormMixin, forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'confirm_password', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()
        if email_exists:
            raise forms.ValidationError("Email all ready exists!")
        return email
    
    def clean_password(self):
        password = self.cleaned_data.get('password')
        errors = []

        if len(password) < 8:
            errors.append('Password must be at least 8 character long')

        if not re.search(r'[A-Z]', password):
            errors.append(
                'Password must include at least one uppercase letter.')

        if not re.search(r'[a-z]', password):
            errors.append(
                'Password must include at least one lowercase letter.')

        if not re.search(r'[0-9]', password):
            errors.append('Password must include at least one number.')

        if not re.search(r'[@#$%^&+=]', password):
            errors.append(
                'Password must include at least one special character.')

        if errors:
            raise forms.ValidationError(errors)

        return password
    
    def clean(self):  # non field error
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password do not match")

        return cleaned_data
    
class LoginForm(AuthenticationForm):
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)