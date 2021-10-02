from django.contrib import admin

# Register your models here.

from .models import Bookitems, LibraryMember

class BookitemsAdmin(admin.ModelAdmin):
    list_display=('title', 'authors', 'isbn')
    

admin.site.register(Bookitems, BookitemsAdmin)
admin.site.register(LibraryMember)