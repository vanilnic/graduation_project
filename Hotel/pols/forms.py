from django import  forms
from django.forms import ModelForm
from .models import User
from django.core.exceptions import ValidationError


class SignUpForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class SignInForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

# def clean_username(self):
    #     username = self.cleaned_data.get('username')
    #     User = get_user_model()
    #     if User.objects.filter(username=username).exists():
    #         raise forms.ValidationError('This username is already taken.')
    #     return username

class AddFavorite(ModelForm):
    class Meta:
        model = User
        fields = ['favorites_hotel']