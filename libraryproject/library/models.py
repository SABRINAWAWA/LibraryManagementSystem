from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

class Bookitems(models.Model):
    title=models.CharField(_('title'), max_length=255, default='NoTitle')
    authors=models.CharField(_('authors'), max_length=200, default='NoAuthor')
    average_rating=models.CharField(_('average rating'), max_length=200, default='0.0')
    isbn=models.CharField(_('isbn'), max_length=50, default='000000000', null=False, unique=True)
    isbn13=models.CharField(_('isbn 13'), max_length=50, default='000000000', null=False)
    language_code=models.CharField(_("language code"), max_length=50, default='eng')
    num_pages=models.CharField(_("number of pages"), max_length=50, null=False, default='0')
    ratings_count=models.CharField(_("rating count"), max_length=50, default='0')
    text_reviews_count=models.CharField(_("text review count"), max_length=50, default='0')
    publication_date=models.CharField(_("publication date"), max_length=50, default="01/01/1800")
    publisher=models.CharField(_("publisher"), max_length=100, default='NoPublisher')

    class Meta:
        ordering = ( 'title', 'authors', 'average_rating', 'isbn', 'isbn13', 'language_code', 'num_pages', 'ratings_count', 
                    'text_reviews_count', 'publication_date', 'publisher')

    def __str__(self):
        return f'{self.title}-{self.authors}'
    
class LibraryMember(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone=models.CharField(max_length=200, null=True)
    address=models.CharField(max_length=200, null=True)
    birthdate=models.DateField(null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.user.username