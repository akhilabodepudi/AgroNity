from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=False, max_length=15)
    first_name = forms.CharField(required=True, max_length=50)
    middle_name = forms.CharField(required=False, max_length=50)
    last_name = forms.CharField(required=True, max_length=50)
    role = forms.ChoiceField(choices=User.ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password1', 'password2',
            'phone_number', 'first_name', 'middle_name', 'last_name', 'role'
        )

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        if role in ('farmer', 'admin'):
            self.instance.is_approved = False
        else:
            self.instance.is_approved = True
        # use email as username if username left blank
        if not cleaned.get('username') and cleaned.get('email'):
            self.instance.username = cleaned['email']
        return cleaned


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email or Username")