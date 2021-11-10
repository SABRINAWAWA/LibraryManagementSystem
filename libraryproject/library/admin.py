from django.contrib import admin

# Register models in admin page
from .models import Bookitems, Feedbacks, Librarian, LibraryMember, LibraryMember, Rented_books, Reserved_books, hist_rented_books, Notification

# Register Bookitem model in the admin page to display id, title, authors, and isbn.
class BookitemsAdmin(admin.ModelAdmin):
    list_display=('id','title', 'authors', 'isbn')
    
# Register Member model in the admin page to display id and user.
class MembersAdmin(admin.ModelAdmin):
    list_display=('id','user')
    
# Register Feedback model in the admin page to display id, member, and feedback_title.
class FeedbacksAdmin(admin.ModelAdmin):
    list_display=('id','member', 'feedback_title')
    
# Register Librarian model in the admin page to display id and user.
class LibrarianAdmin(admin.ModelAdmin):
    list_display=('id','user')
    
# Register Notification model in the admin page to display id, notification_type, title and date.
class NotificationAdmin(admin.ModelAdmin):
    list_display=('id','notification_type', 'Title','date')
    
# Register models in admin page
admin.site.register(Bookitems, BookitemsAdmin)
admin.site.register(LibraryMember, MembersAdmin)
admin.site.register(Librarian, LibrarianAdmin)
admin.site.register(Rented_books)
admin.site.register(hist_rented_books)
admin.site.register(Reserved_books)
admin.site.register(Feedbacks, FeedbacksAdmin)
admin.site.register(Notification, NotificationAdmin)