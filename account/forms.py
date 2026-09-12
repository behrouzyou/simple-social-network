from typing import Any

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from account.models import Profile


class UserRegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 =forms.CharField(label='password',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 =forms.CharField(label='confirm password',widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if not email:
            raise ValidationError('user must have email')
        if user:
            raise ValidationError('email has already exists')
        return email

    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()
        if not username:
            raise ValidationError('user must have username')
        if user:
            raise ValidationError('username has already exists')
        return username
    def clean(self) -> dict[str, Any] | None:
        cd=super().clean()
        p1=cd.get('password1')
        p2=cd.get('password2')
        if p1 and p2 and p1 != p2 :
            raise ValidationError('password dont match')

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EditUserForm(forms.ModelForm):
    email= forms.EmailField()
    class Meta:
        model=Profile
        fields =('age','address')