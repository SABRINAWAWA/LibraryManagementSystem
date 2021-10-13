from django.contrib import admin

# Register your models here.

from .models import Bookitems, Feedbacks, Librarian, LibraryMember, LibraryMember, Rented_books, Reserved_books, hist_rented_books

class BookitemsAdmin(admin.ModelAdmin):
    list_display=('id','title', 'authors', 'isbn')
    
class MembersAdmin(admin.ModelAdmin):
    list_display=('id','user')
    
class FeedbacksAdmin(admin.ModelAdmin):
    list_display=('id','member', 'feedback_title')
    
admin.site.register(Bookitems, BookitemsAdmin)
admin.site.register(LibraryMember, MembersAdmin)
admin.site.register(Librarian)
admin.site.register(Rented_books)
admin.site.register(hist_rented_books)
admin.site.register(Reserved_books)
admin.site.register(Feedbacks, FeedbacksAdmin)