from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/',views.home),
    path('searchbooks/', views.searchBooks),
    path('searchusers/', views.searchUsers),
    
    # Library member-related links
    path('login/', views.loginpage),
    path('logout/', views.logoutuser),
    path('register/', views.registerpage),
    path('editmemberinfo/', views.editmemberinfo),
    
    # Panel links
    path('memberpanel/', views.memberpanel),
    path('librarianpanel/', views.librarianpanel),
    
    # Bookitems-related features
    path('bookitems/<int:book_id>', views.bookdetails),
    path('bookitems/addbook/', views.addBook),
    path('bookitems/editBookitemInfo/<int:book_id>', views.editBookDetails),
    path('bookitems/deleteBookitem/<int:book_id>', views.deleteBook),
    
    # Feedback feature
    path('feedback/new/', views.createFeedback),
    path('feedback/update/<int:feedback_id>', views.updateFeedback),
    path('feedback/delete/<int:feedback_id>', views.deleteFeedback),
    
    #Register new Librarian and Update Librarian info
    path('register/librarian/', views.registerLibrarian),
    path('update/librarian/', views.editLibrarianInfo),
    
    #Notification Feature
    path('notification/<int:notification_id>', views.checkNotification, name="check-notification"),
    path('notification/delete/<int:notification_id>', views.deleteNotification,name="delete-notification"),
    path('notification/new/<int:user_id>', views.sendNotification, name="new-notification"),
    
    #Reset Password Feature
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="library/password_reset.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="library/password_reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="library/password_reset_form.html"), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="library/password_reset_done.html"), name="password_reset_complete"),
    
    #check-in/ check-out feature
    path('check_in/<int:user_id>', views.checkinPage),
    path('check_out/<int:user_id>', views.checkoutPage),
    
    
    #hold/release account feature
    path('holdaccount/', views.pickUser),
    path('holdaccount/hold/<int:user_id>', views.holdAccount),
    path('holdaccount/release/<int:user_id>', views.releaseAccount),

]

'''
Password reset feature:
1. Submit email form  //PasswordResetView.as_view()
2. Email sent success message //PasswordResetDoneView.as_view()
3. Link to password Reset from in email //PasswordResetConfirmView.as_view()
4. Password successfully changed message // PasswordResetCompleteView.as_view()
'''