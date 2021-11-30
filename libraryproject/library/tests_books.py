from django.test import TestCase, Client
from django.urls import reverse
from library.models import *
from library.forms import *
from library.views import *
from django.contrib.auth.models import User


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.addBook_url = reverse('addBook')
        self.user = User.objects.create_user(username='abc', password='abc')
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
        
        
        book = Bookitems.objects.all()
        print(book)
        self.assertEqual(response.status_code, 302) 