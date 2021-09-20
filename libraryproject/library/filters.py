import django_filters
from django_filters import CharFilter
 
from .models import *

class BookitemsFilter(django_filters.FilterSet):
    title=CharFilter(field_name='title', lookup_expr='icontains')
    authors=CharFilter(field_name='authors', lookup_expr='icontains')
    
    class Meta:
        model= Bookitems
        fields=['title', 'authors', 'isbn']