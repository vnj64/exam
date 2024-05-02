from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput()
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password1',
            'password2',
        )


class AddBalanceForm(forms.ModelForm):
    balance = forms.IntegerField(
        widget=forms.TextInput()
    )

    class Meta:
        model = Profile
        fields = ('balance',)
