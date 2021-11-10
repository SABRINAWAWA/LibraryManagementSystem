from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Feedbacks, LibraryMember, Bookitems, Librarian, Notification, Review
from django.forms import Textarea


"""[summary]
Class name: CreateUserForm
Class purpose: CreateUserForm is used to create a new user. It contains fields: first_name, last_name, username, password1, and password2
"""
class CreateUserForm(UserCreationForm):
    last_name=forms.CharField(max_length=100)
    first_name=forms.CharField(max_length=100)

    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
       
"""[summary]
Class name: UserUpdateForm
Class purpose: UserUpdateForm is used to update a exist user information. 
""" 
class UserUpdateForm(forms.ModelForm):
    last_name=forms.CharField(max_length=100)
    first_name=forms.CharField(max_length=100)
    username=forms.CharField(max_length=50)
    email=forms.EmailField(max_length=100)
    class Meta:
        model=User
        fields=['first_name', 'last_name', 'username', 'email']
       
"""[summary]
Class name: MemberUpdateForm
Class purpose: MemberUpdateForm is used to create a new member. It contains fields: phone, address, and birthdate.
""" 
class MemberUpdateForm(forms.ModelForm):
    phone=forms.CharField(max_length=20)
    address=forms.CharField(max_length=100)
    birthdate=forms.DateField()
    
    class Meta:
        model=LibraryMember
        fields=['phone', 'address', 'birthdate']

"""[summary]
Class name: BookitemForm
Class purpose:BookitemForm is used to create a new bookitem object. It contains fields: 'title', 'authors', 'average_rating', 'isbn', 'format', 
                'description', 'edition', 'genres', 'img_url', 'stock_quantity', 
                'available_quantity'.
"""
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

"""[summary]
Class name: FeedbackForm
Class purpose: FeedbackForm is used to create a new Feedback. It contains fields: content and title. 
"""
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

"""[summary]
Class name: LibarianUpdateForm
Class purpose: LibarianUpdateForm is used to create a new librarian. It contains fields: phone, address, birthdate, position and logo.
"""
class LibarianUpdateForm(forms.ModelForm):
    phone=forms.CharField(max_length=20)
    address=forms.CharField(max_length=100)
    birthdate=forms.DateField()
    position=forms.MultipleChoiceField(choices = position_choices)
    logo=forms.CharField(max_length=200)
    class Meta:
        model=Librarian
        fields=['phone', 'address', 'birthdate','position','logo']

"""[summary]
Class name: NotificationForm
Class purpose: NotificationForm is used to create a new Notification. It contains fields: title and content.
"""   
class NotificationForm(forms.ModelForm):
    Title=forms.CharField(max_length=255)
    content=forms.Textarea()
    class Meta:
        model=Notification
        fields=['Title', 'content']

"""[summary]
Class name: ReviewForm
Class purpose: review form is used to create a new Notification. It contains fields: author and content.
"""
class ReviewForm(forms.ModelForm):
    author=forms.CharField(max_length=200)
    content=forms.Textarea()

    class Meta:
        model=Review
        fields=['author', 'content']        