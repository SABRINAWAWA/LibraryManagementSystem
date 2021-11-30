from django.test import TestCase, Client
from django.urls import reverse
from django.db import models
from datetime import date
from django.contrib.auth.models import User, Group
from library.models import Bookitems,LibraryMember,Librarian,Rented_books
from library.views import *
from library.forms import *


class ModelTest(TestCase):
    def setUp(self):
        title = 'Harry Potter and the Order of the Phoenix (Harry Potter  #5)'
        authors='J.K. Rowling/Mary GrandPré'
        self.book = Bookitems.objects.create(title=title, authors=authors)

    def test_bookitems_table(self):
        self.assertTrue(isinstance(self.book, Bookitems))
        self.assertEqual("Harry Potter and the Order of the Phoenix (Harry Potter  #5)-J.K. Rowling/Mary GrandPré",
                         str(self.book))

    def creat_library_member(self):
        member = LibraryMember.objects.create()
        member.user = User()
        member.user.username = 'Anita'
        return member

    def test_library_member_table(self):
        member = self.creat_library_member()
        self.assertTrue(isinstance(member,LibraryMember))
        self.assertEqual('Anita', str(member))

    def creat_librarian(self):
        librarian = Librarian.objects.create()
        librarian.user = User()
        librarian.user.username = 'Kitty'
        return librarian

    def test_librarian_table(self):
        librarian = self.creat_librarian()
        self.assertTrue(isinstance(librarian,Librarian))
        self.assertEqual('Kitty',str(librarian))

    def create_rented_book(self):
        book = self.book
        title = book.title
        member = self.creat_library_member()
        rented_date = date(2021,11,1).isoformat()
        return_date = date(2021,11,20).isoformat()
        rented_book = Rented_books.objects.create(book=book,title=title,member=member,rented_date=rented_date,
                                                  return_date=return_date)
        return rented_book

    def test_rented_books(self):
        rented_book = self.create_rented_book()
        self.assertTrue(isinstance(rented_book,Rented_books))
        self.assertEqual("Harry Potter and the Order of the Phoenix (Harry Potter  #5)",str(rented_book))


class ViewsTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.addBook_url = reverse('addBook')
        self.user = User.objects.create_user(username='abc', password='abc') # creating a user
        self.group = Group(name="librarian") # creating librarian group
        self.group.save() # saving librarian group
        self.user.groups.add(self.group) # adding the created user to the librarian group

    def test_home(self):
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, 200)

    def test_search_accesible_by_name(self):
        response = self.client.get(reverse(searchBooks))
        self.assertEqual(response.status_code, 200)


    def test_add_book(self):
         self.client.login(username='abc', password='abc')
         response = self.client.post(self.addBook_url, data={
             'title': 'abracadabra',
             'authors': 'abracadbrier, writer',
             'average_rating': '4.75',
             'isbn': '9000450655600',
             'format': 'hardcover',
            'description': 'Very interesting abracadabra!',
             'edition': 'First Edition',
             'genres': 'fiction',
             'img_url': 'http://images.abracadabra',
             'stock_quantity': 5,
             'available_quantity': 5})
    
         book = Bookitems.objects.all().values()
         print(book)
         self.assertEqual(response.status_code, 302)
    
    
class TestForms(TestCase):
    def test_create_user_form_valid_data(self):
        #filled out form validation
        form = CreateUserForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'JohnD123',
            'email': 'johnD123@gmail.com',
            'password1': 'JDoe12345!',
            'password2': 'JDoe12345!'
        })

        self.assertTrue(form.is_valid())

    def test_create_user_form_no_data(self):
        #empty form validation
        form = CreateUserForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_user_update_form_valid_data(self):
        #filled out form validation
        form = UserUpdateForm(data={
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'JohnD123',
            'email': 'johnD123@gmail.com'
        })

        self.assertTrue(form.is_valid())

    def test_user_update_form_no_data(self):
        #empty form validation
        form = UserUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)

    def test_member_update_form_valid_data(self):
        #filled out form validation
        form = MemberUpdateForm(data={
            'phone': '415123456',
            'address': '745 Avenue',
            'birthdate': '01/17/2000'
        })

        self.assertTrue(form.is_valid())

    def test_member_update_form_no_data(self):
        #empty form validation
        form = MemberUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 3)

    def test_bookitem_form_valid_data(self):
        #filled out form validation
        form = BookitemForm(data={
            'title': 'abracadabra',
            'authors': 'abracadbrier, writer',
            'average_rating': '4.75',
            'isbn': '9000450655600',
            'format': 'hardcover',
            'description': 'Very interesting abracadabra!',
            'edition': 'First Edition',
            'genres': 'fiction',
            'img_url': 'http://images.abracadabra',
            'stock_quantity': 5,
            'available_quantity': 5
        })

        self.assertTrue(form.is_valid())

    def test_bookitem_form_no_data(self):
        #empty form validation
        form = BookitemForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 11)

    def test_feedback_form_valid_data(self):
        #filled out form validation
        form = FeedbackForm(data={'feedback_title': 'abracadabra','feedback_content': 'abracadabra'})
        self.assertTrue(form.is_valid())

    def test_feedback_form_no_data(self):
         #empty form validation
         form = FeedbackForm(data={})
         self.assertFalse(form.is_valid())
         self.assertEquals(len(form.errors), 2)

    def test_librarian_update_form_valid_data(self):
        #filled out form validation
        form = LibarianUpdateForm(data={
            'phone': '415123456',
            'address': '745 Avenue',
            'birthdate': '01/17/2000',
            'position': 'librarian',
            'logo': 'http://images.absd'
        })

        self.assertTrue(form.is_valid())

    def test_librarian_update_form_no_data(self):
        #empty form validation
        form = LibarianUpdateForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 5)

    def test_notification_form_valid_data(self):
        #filled out form validation
        form = NotificationForm(data={
            'Title': 'abracadabra',
            'content': 'abracadabra'
        })

        self.assertTrue(form.is_valid())

    def test_notification_form_no_data(self):
        #empty form validation
        form = NotificationForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)

    def test_review_form_valid_data(self):
        #filled out form validation
        form = ReviewForm(data={
            'author': 'abracadabrier',
            'content': 'abracadabra'
        })

        self.assertTrue(form.is_valid())

    def test_review_form_no_data(self):
         #empty form validation
         form = ReviewForm(data={})
         self.assertFalse(form.is_valid())
         self.assertEquals(len(form.errors), 2)


