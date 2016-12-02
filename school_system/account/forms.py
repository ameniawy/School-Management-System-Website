from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate

from django.shortcuts import get_object_or_404,Http404


class User_login_form(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self ,*args ,**kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Username or Password is incorrect")
        return super(User_login_form, self).clean(*args,**kwargs)
