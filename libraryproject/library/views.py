from django.shortcuts import render

# Create your views here.
from .models import Bookitems
from .filters import BookitemsFilter

def index(request):
    searchedbook=[]
    bookitems = Bookitems.objects.all()
    bookFilter=BookitemsFilter(request.GET, queryset=bookitems)
    if bookFilter.is_valid():
        searchedbook=bookFilter.qs
    return render(request, 'library/search-catalog.html',{
        'bookitems':bookitems,
        'bookFilter':bookFilter,
        'searchedbook':searchedbook
    })
