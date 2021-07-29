from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from . import models


class RegistForm(UserCreationForm):
    fullname = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Fullname',
                   'class': 'c-form form-control'}),
        max_length=150,
        label="Fullname"
    )

    email = forms.EmailField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'class': 'c-form form-control'}),
        max_length=254,
        label="Email"
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'c-form form-control'}),
        label="Password"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirm Password',
                   'class': 'c-form form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = models.BlogUser
        fields = ('fullname', 'email')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Email',
                   'class': 'c-form form-control'}),
        max_length=254,
        label="Email"
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password',
                   'class': 'c-form form-control'}),
        label="Password"
    )


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = models.UserDetail
        fields = '__all__'
