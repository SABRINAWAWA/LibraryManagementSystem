from django.urls import path

from . import views

urlpatterns = [
    path('home/',views.home),
    path('searchcatalog/', views.search),
    path('login/', views.loginpage),
    path('logout/', views.logoutuser),
    path('register/', views.registerpage),
    path('memberpanel/', views.memberpanel),
    path('librarianpanel/', views.librarianpanel),
    path('editmemberinfo/', views.editmemberinfo),
    path('bookitems/<int:book_id>', views.bookdetails),
    path('bookitems/addbook/', views.addBook),
    path('bookitems/editBookitemInfo/<int:book_id>', views.editBookDetails),
    path('bookitems/deleteBookitem/<int:book_id>', views.deleteBook),
    path('feedback/new/', views.createFeedback),
    path('feedback/update/<int:feedback_id>', views.updateFeedback),
    path('feedback/delete/<int:feedback_id>', views.deleteFeedback)
]