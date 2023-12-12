from django import forms
from users.models import CustomUser
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'username', 'email')

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'username', 'tg_username', 'phone_number', 'avatar')






