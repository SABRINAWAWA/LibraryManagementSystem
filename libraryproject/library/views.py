from django.shortcuts import render

# Create your views here.
from .models import Bookitems
from .filters import BookitemsFilter


def index(request):
    popularBooks = [
        {'id':1,'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9781982164881.jpg', 'title': 'Vince Flynn: Enemy At the Gates',
            'description': 'By Kyle Mills. Picking up where the “tour de force” (The Providence Journal) Total Power left off, the next thriller in the #1 New York Times bestselling Mitch Rapp series follows the CIA’s top operative as he searches for a high-level mole with the power to rewrite the world order.', 
            'genre': 'Genre: Fiction, Thrillers & Suspense'},
        {'id':2,'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9781982173616.jpg', 'title': 'Bill Summer',
            'description': 'By, Stephen King. Billy Summers is a man in a room with a gun. He’s a killer for hire and the best in the business. But he’ll do the job only if the target is a truly bad guy. And now Billy wants out. But first there is one last hit. Billy is among the best snipers in the world, a decorated Iraq war vet, a Houdini when it comes to vanishing after the job is done. So what could possibly go wrong?', 
            'genre': 'Genre: Fiction, Action & Adventure'},
        {'id':3,'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9781501135972.jpg', 'title': 'AMERICAN MARXISM',
            'description': 'By Mark R. Levin. In American Marxism, Levin explains how the core elements of Marxist ideology are now pervasive in American society and culture—from our schools, the press, and corporations, to Hollywood, the Democratic Party, and the Biden presidency—and how it is often cloaked in deceptive labels like “progressivism,” “democratic socialism,” “social activism,” and more.', 
            'genre': 'Genre: Politics and Government'},
        {'id':4,'imageUrl':'https://storage.googleapis.com/du-prd/books/images/9780735211292.jpg', 'title': 'ATOMIC HABITS', 
         'description':'By James Clear. If you are having trouble changing your habits, the problem is not you. The problem is your system. Bad habits repeat themselves again and again not because you do not want to change, but because you have the wrong system for change. You do not rise to the level of your goals. You fall to the level of your systems. Here, you will get a proven system that can take you to new heights.', 
         'genre': 'Genre: Psychology and Counseling'},
        {'id':5,'imageUrl':'https://storage.googleapis.com/du-prd/books/images/9780375899881.jpg', 'title': 'Wonder', 
         'description':'By R. J. Palacio. August Pullman was born with a facial difference that, up until now, has prevented him from going to a mainstream school. Starting 5th grade at Beecher Prep, he wants nothing more than to be treated as an ordinary kid—but his new classmates can’t get past Auggie’s extraordinary face.', 
         'genre': 'Genre: Fiction, Children'}
    ]
    news=[
        {'id':1, 'title': 'New Books Donated by the City College of San Francisco', 
         'details': 'CCSF Library provide quality books to public school and community libraries where the majority of students live at or below the poverty line. Since 1999, with the help of volunteers, we’ve refurbished over 300 libraries and donated more than 1.7 million books. We also collaborate with partners to host fun, literacy experiences for families in communities throughout San Francisco.',
         'image': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1170&q=80'},
        {'id':2, 'title': 'Adding Search Catalog Feature', 
         'details': 'One of our tech members, Sabrina, designed and implemented the Search Catalog feature for our website. This web page is up and running. Members can access this feature through the `search` link on the right top corner.',
         'image':None},
        {'id': 3, 'title': 'New Check-in and Check-out Feature Will be Published Within Three Weeks',
         'details': 'During next three or four weeks, our tech team will work on design and implement the Check-in and Check-out functions and improve our member and librarian system in our library management system.',
          'image':None}
    ]
    return render(request, 'library/homepage.html', {
        'popularBooks': popularBooks,
        'news':news
    })


def search(request):
    searchedbook = []
    bookitems = Bookitems.objects.all()
    bookFilter = BookitemsFilter(request.GET, queryset=bookitems)
    if bookFilter.is_valid():
        searchedbook = bookFilter.qs
    return render(request, 'library/search-catalog.html', {
        'bookitems': bookitems,
        'bookFilter': bookFilter,
        'searchedbook': searchedbook
    })
