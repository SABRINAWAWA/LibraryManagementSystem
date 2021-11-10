import django_filters
from django_filters import CharFilter
 
from .models import *

"""[summary]
Class name: BookitemsFilter
Class purpose: this filter is used to search book based on title, authors, and isbn.
"""
class BookitemsFilter(django_filters.FilterSet):
    title=CharFilter(field_name='title', lookup_expr='icontains')
    authors=CharFilter(field_name='authors', lookup_expr='icontains')
    
    class Meta:
        model= Bookitems
        fields=['title', 'authors', 'isbn']
        
"""[summary]
Class name: UserFilter
Class purpose: this filter is used to search user based on username, email and id.
"""
class UserFilter(django_filters.FilterSet):
    email=CharFilter(field_name='email',lookup_expr='icontains')
    username=CharFilter(field_name='username',lookup_expr='icontains')
    class Meta:
        model= User
        fields=['id','email','username']