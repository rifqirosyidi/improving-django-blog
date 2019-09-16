from django.contrib.auth import (
    login,
    logout,
    authenticate,
    get_user_model
)
from django import forms
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("username doesn't exist")
        if not user.check_password(password):
            raise forms.ValidationError("incorrect password")
        if not user.is_active:
            raise forms.ValidationError("user is not active")
        
        return super(UserLoginForm, self).clean()


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('password2')

        if password != confirm_password:
            raise forms.ValidationError("Password didn't Match")

        return password, confirm_password


