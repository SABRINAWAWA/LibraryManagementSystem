from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Feedbacks, LibraryMember, Bookitems, Librarian, Notification, Review
from django.forms import Textarea

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
        
class BookitemForm(forms.ModelForm):
    title=forms.CharField(max_length=225)
    authors=forms.CharField(max_length=200)
    average_rating=forms.CharField(max_length=200)
    isbn=forms.CharField(max_length=50)
    format=forms.CharField(max_length=100)
    description=forms.CharField(max_length=10000, widget=forms.Textarea(attrs={'cols': 40, 'rows': 5}))
    edition=forms.CharField(max_length=100)
    genres=forms.CharField(max_length=100)
    img_url=forms.CharField(max_length=1000)
    stock_quantity=forms.IntegerField(min_value=0)
    available_quantity=forms.IntegerField(min_value=0)
    class Meta:
        model=Bookitems
        fields = ('title', 'authors', 'average_rating', 'isbn', 'format', 
                'description', 'edition', 'genres', 'img_url', 'stock_quantity', 
                'available_quantity')

class FeedbackForm(forms.ModelForm):
    feedback_title=forms.CharField(max_length=255)
    feedback_content=forms.Textarea()
    class Meta:
        model=Feedbacks
        fields = ['feedback_content', 'feedback_title']

position_choices =(
    ("Librarian", "Librarian"),
    ("Library Technician", "Library Technician"),
    ("Library Assistant", "Library Assistant"),
    ("Library Director", "Library Director"),
)

class LibarianUpdateForm(forms.ModelForm):
    phone=forms.CharField(max_length=20)
    address=forms.CharField(max_length=100)
    birthdate=forms.DateField()
    position=forms.CharField(widget=forms.Select(choices=position_choices))
    logo=forms.CharField(max_length=200)
    class Meta:
        model=Librarian
        fields=['phone', 'address', 'birthdate','position','logo']
        
class NotificationForm(forms.ModelForm):
    Title=forms.CharField(max_length=255)
    content=forms.CharField(max_length=1000, widget=forms.Textarea(attrs={'cols': 40, 'rows': 10}))
    class Meta:
        model=Notification
        fields=['Title', 'content']

class ReviewForm(forms.ModelForm):
    author=forms.CharField(max_length=200)
    content=forms.Textarea()

    class Meta:
        model=Review
        fields=['author', 'content']    