from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _
from django.contrib.auth.models import User

# Bookitems class defines the bookitems model/table
class Bookitems(models.Model):
    title=models.CharField(_('title'), max_length=255, default='NoTitle')
    authors=models.CharField(_('authors'), max_length=200, default='NoAuthor')
    average_rating=models.CharField(_('average rating'), max_length=200, default='0.0')
    isbn=models.CharField(_('isbn'), max_length=50, default='000000000', null=False, unique=True)
    format=models.CharField(_("format"), max_length=100, default='NoFormat')
    description=models.CharField(_("description"), max_length=10000, default='NoDescription')
    edition=models.CharField(_("edition"), max_length=100, default='NoEdition')
    genres=models.CharField(_("genres"), max_length=100, default='NoGenre')
    img_url=models.CharField(_("images"), max_length=1000, default='NoImage')
    stock_quantity=models.IntegerField(_("Stock Quantity"), default=0)
    available_quantity=models.IntegerField(_("Available Quantity"), default=0)
    obs=models.BooleanField(_('OBS'), default=True)
    class Meta:
        ordering = ( 'title', 'authors', 'average_rating', 'isbn', 'format', 'description', 'edition', 'genres', 'img_url', 'stock_quantity', 'available_quantity','obs' )

    def __str__(self):
        return f'{self.title}-{self.authors}'

# LibraryMember class defines the library member model/table
class LibraryMember(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone=models.CharField(max_length=200, null=True)
    address=models.CharField(max_length=200, null=True)
    birthdate=models.DateField(null=True)
    date_created=models.DateTimeField(auto_now_add=True, null=True)
    hold=models.BooleanField(_('hold'), default=False)
    
    def __str__(self):
        return self.user.username

# Librarian class defines the librarian model/table
class Librarian(models.Model):
    user=models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    phone=models.CharField(max_length=200, null=True) 
    address=models.CharField(_('address'), max_length=200, null=True)
    birthdate=models.DateField(null=True)
    position=models.CharField(max_length=200, null=True)
    logo=models.CharField(_("Logo"), max_length=200, null=True, default="https://images.unsplash.com/photo-1509021436665-8f07dbf5bf1d?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1374&q=80")
    date_created=models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.user.username
    
# Rented_books class defines the Rented_books model/table
class Rented_books(models.Model):    
    book=models.ForeignKey(Bookitems, null=True, on_delete=models.PROTECT)
    title=models.CharField(_('title'), max_length=255, default='NoTitle')
    member=models.ForeignKey(LibraryMember, null=False, on_delete=models.PROTECT)
    rented_date=models.DateField(_('Rented Date'), default="YYYY-MM-DD", null=True)
    return_date=models.DateField(_('Returned Date'), default="YYYY-MM-DD", null=True)
    obs=models.BooleanField(_('OBS'), default=True)
    lateReturn=models.BooleanField(_('Late Return'), default=False)
    def __str__(self):
        return self.title
    
# hist_rented_books class defines the hist_rented_books model/table
class hist_rented_books(models.Model):    
    book=models.ForeignKey(Bookitems, null=True, on_delete=models.PROTECT)
    title=models.CharField(_('title'), max_length=255, default='NoTitle')
    member=models.ForeignKey(LibraryMember, null=False, on_delete=models.PROTECT)
    rented_date=models.DateField(_('Rented Date'), default="YYYY-MM-DD", null=True)
    return_date=models.DateField(_('Returned Date'), default="YYYY-MM-DD", null=True)
    obs=models.BooleanField(_('OBS'), default=True)
    def __str__(self):
        return self.title
    
# reserved_books class defines the Reserved_books model/table
class Reserved_books(models.Model): 
    book=models.ForeignKey(Bookitems, null=True, on_delete=models.PROTECT)
    title=models.CharField(_('title'), max_length=255, default='NoTitle')
    member=models.ForeignKey(LibraryMember, null=False, on_delete=models.PROTECT)
    reserved_date=models.DateField(_('Reserved Date'), default="YYYY-MM-DD", null=True)
    deadline=models.DateField(_('Deadline'), default="YYYY-MM-DD", null=True)
    available_rent_date=models.DateField(_('Available Rent Date'), default="YYYY-MM-DD", null=True)
    obs=models.BooleanField(_('OBS'), default=True)
    canReserve=models.BooleanField(_('Can Reserve'), default=False)
    
    def __str__(self):
        return self.title
    
# Feedbacks class defines the feedbacks model/table
class Feedbacks(models.Model):    
    member=models.ForeignKey(LibraryMember, null=False, on_delete=models.CASCADE)
    feedback_title=models.CharField(_('Feedback Title'), max_length=255, default='NoFeedbackTitle')
    feedback_content=models.TextField(_('Feedback'), max_length=2000, default='NoFeedback')
    feedback_datetime=models.DateTimeField(_('Feedbak Datetime'), auto_now_add=True, null=True)
    obs=models.BooleanField(_('OBS'), default=True)
    def __str__(self):
        return f'{self.member.user.username}'
 
# Notification class defines the notifications model/table   
class Notification(models.Model):
    # 1=returned book, 2=reserved book, 3=rented book
    notification_type=models.IntegerField(_('Notification Type'))
    to_member=models.ForeignKey(LibraryMember, related_name='notification_to', on_delete=models.CASCADE, null=True)
    from_Librarian=models.ForeignKey(Librarian, related_name='notification_from', on_delete=models.CASCADE, null=True)
    Title=models.CharField(max_length=255)
    content=models.TextField(max_length=255)
    reservedBook=models.ForeignKey(Reserved_books,blank=True, on_delete=models.CASCADE,null=True)
    rentedBook=models.ForeignKey(Rented_books,blank=True,on_delete=models.CASCADE, null=True)
    date=models.DateTimeField(default=timezone.now, null=True)
    user_has_seen=models.BooleanField(default=False)
    
    
# Review class defines the review model/table
class Review(models.Model):
    book = models.ForeignKey('Bookitems', on_delete=models.PROTECT)
    author = models.CharField(max_length=200)
    content = models.TextField(max_length=1000)
    created_date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.text