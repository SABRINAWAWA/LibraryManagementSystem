from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import LibraryMember

class CreateUserForm(UserCreationForm):
    last_name=forms.CharField(max_length=100)
    first_name=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        
class UserUpdateForm(forms.ModelForm):
    last_name=forms.CharField(max_length=100)
    first_name=forms.CharField(max_length=100)
    username=forms.CharField(max_length=50)
    email=forms.EmailField(max_length=100)
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email']
        
class MemberUpdateForm(forms.ModelForm):
    phone=forms.CharField(max_length=20)
    address=forms.CharField(max_length=100)
    birthdate=forms.DateField()
    
    class Meta:
        model=LibraryMember
        fields=['phone', 'address', 'birthdate']