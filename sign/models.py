from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username", 
                  "first_name", 
                  "last_name", 
                  "email", 
                  "password1", 
                  "password2", )
        # labels = {
        #     "username": 'Имя', 
        #     "first_name": 'Имя', 
        #     "last_name": 'Фвмилия', 
        #     "email": 'email', 
        #     "password1": 'Пароль', 
        #     "password2": 'Пароль', 
        # }

class BasicSignupForm(SignupForm):
    
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='Common')
        common_group.user_set.add(user)
        return user

