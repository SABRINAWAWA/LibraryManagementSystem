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
    path('editmemberinfo/', views.editmemberinfo)
]