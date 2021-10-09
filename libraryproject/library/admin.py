from django.contrib import admin

# Register your models here.

from .models import Bookitems, Feedbacks, Librarian, LibraryMember, Rented_books, Reserved_books, hist_rented_books

class BookitemsAdmin(admin.ModelAdmin):
    list_display=('title', 'authors', 'isbn')
    

admin.site.register(Bookitems, BookitemsAdmin)
admin.site.register(LibraryMember)
admin.site.register(Librarian)
admin.site.register(Rented_books)
admin.site.register(hist_rented_books)
admin.site.register(Reserved_books)
admin.site.register(Feedbacks)
