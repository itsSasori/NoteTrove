from django.forms import ModelForm
from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import  User
from .models import Room


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2']


class NoteForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']



