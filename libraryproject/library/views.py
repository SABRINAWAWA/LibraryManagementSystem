import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views import View
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User

from .models import Bookitems, LibraryMember, Feedbacks, Librarian, Notification, Reserved_books, Rented_books
from .filters import BookitemsFilter, UserFilter
from .forms import CreateUserForm, UserUpdateForm, MemberUpdateForm, BookitemForm, FeedbackForm, LibarianUpdateForm, NotificationForm
from .decorators import unauthenticated_user, allowed_user, librarian_only

"""[summary]
Function name: home
Function description: rendering homepage
Note: Futher modification needs to import the bookitems from bookitems table and add librarian info
"""
def home(request):
    popularBooks = [
        {'id': 1, 'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9781982164881.jpg', 'title': 'Vince Flynn: Enemy At the Gates',
            'description': 'By Kyle Mills. Picking up where the “tour de force” (The Providence Journal) Total Power left off, the next thriller in the #1 New York Times bestselling Mitch Rapp series follows the CIA’s top operative as he searches for a high-level mole with the power to rewrite the world order.',
            'genre': 'Genre: Fiction, Thrillers & Suspense'},
        {'id': 2, 'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9781982173616.jpg', 'title': 'Bill Summer',
            'description': 'By, Stephen King. Billy Summers is a man in a room with a gun. He’s a killer for hire and the best in the business. But he’ll do the job only if the target is a truly bad guy. And now Billy wants out. But first there is one last hit. Billy is among the best snipers in the world, a decorated Iraq war vet, a Houdini when it comes to vanishing after the job is done. So what could possibly go wrong?',
            'genre': 'Genre: Fiction, Action & Adventure'},
        {'id': 3, 'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9781501135972.jpg', 'title': 'AMERICAN MARXISM',
            'description': 'By Mark R. Levin. In American Marxism, Levin explains how the core elements of Marxist ideology are now pervasive in American society and culture—from our schools, the press, and corporations, to Hollywood, the Democratic Party, and the Biden presidency—and how it is often cloaked in deceptive labels like “progressivism,” “democratic socialism,” “social activism,” and more.',
            'genre': 'Genre: Politics and Government'},
        {'id': 4, 'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9780735211292.jpg', 'title': 'ATOMIC HABITS',
         'description': 'By James Clear. If you are having trouble changing your habits, the problem is not you. The problem is your system. Bad habits repeat themselves again and again not because you do not want to change, but because you have the wrong system for change. You do not rise to the level of your goals. You fall to the level of your systems. Here, you will get a proven system that can take you to new heights.',
         'genre': 'Genre: Psychology and Counseling'},
        {'id': 5, 'imageUrl': 'https://storage.googleapis.com/du-prd/books/images/9780375899881.jpg', 'title': 'Wonder',
         'description': 'By R. J. Palacio. August Pullman was born with a facial difference that, up until now, has prevented him from going to a mainstream school. Starting 5th grade at Beecher Prep, he wants nothing more than to be treated as an ordinary kid—but his new classmates can’t get past Auggie’s extraordinary face.',
         'genre': 'Genre: Fiction, Children'}
    ]
    news = [
        {'id': 1, 'title': 'New Books Donated by the City College of San Francisco',
         'details': 'CCSF Library provide quality books to public school and community libraries where the majority of students live at or below the poverty line. Since 1999, with the help of volunteers, we’ve refurbished over 300 libraries and donated more than 1.7 million books. We also collaborate with partners to host fun, literacy experiences for families in communities throughout San Francisco.',
         'image': 'https://images.unsplash.com/photo-1463320726281-696a485928c7?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1170&q=80'},
        {'id': 2, 'title': 'Adding Search Catalog Feature',
         'details': 'One of our tech LibraryMembers, Sabrina, designed and implemented the Search Catalog feature for our website. This web page is up and running. LibraryMembers can access this feature through the `search` link on the right top corner.',
         'image': None},
        {'id': 3, 'title': 'New Check-in and Check-out Feature Will be Published Within Three Weeks',
         'details': 'During next three or four weeks, our tech team will work on design and implement the Check-in and Check-out functions and improve our LibraryMember and librarian system in our library management system.',
          'image': None}
    ]
    return render(request, 'library/homepage.html', {
        'popularBooks': popularBooks,
        'news': news
    })

"""[summary]
Function name: search 
Function description: rendering search catalog page
Note: Using BookitemsFilter class in filters.py to generate the filter result. 
"""
def search(request):
    searchedbook = []
    bookitems = getAllBookitems() 
    bookFilter = BookitemsFilter(request.GET, queryset=bookitems)
    if bookFilter.is_valid():
        searchedbook = bookFilter.qs
    return render(request, 'library/search-catalog.html', {
        'bookitems': bookitems,
        'bookFilter': bookFilter,
        'searchedbook': searchedbook
    })
    
"""[summary]
Function name: is_valid_params
Function description: check if input variable is null or empty string. Return true if input variable is not null and is not empty string, otherwise, return false.
"""
def is_valid_params(param):
    return param !='' and param is not None

"""[summary]
Function name: searchbooks
Function description: search all bookitems in the database depending on the title, author, isbn, and category. 
"""
def searchBooks(request):
    # Get all bookitems from bookitems table
    bookitems = getAllBookitems()
    # preset searchedbook to an empty string
    searchedbook=''
    # getting all search input from the form
    title_contains_query=request.GET.get('title_contains')
    author_contains_query=request.GET.get('author_contains')
    isbn_exact_query=request.GET.get('isbn_exact')
    category_contains_query=request.GET.get('category_contains')
    # check all possiblilities of search bookitems
    # when all fields input fulfills out
    if is_valid_params(title_contains_query) and is_valid_params(author_contains_query) and is_valid_params(isbn_exact_query) and is_valid_params(category_contains_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) & Q(authors__icontains=author_contains_query) & Q(isbn=isbn_exact_query) & Q(genres__icontains=category_contains_query)).distinct()
    # when three of four inputs fulfill out
    # genres, authors, and isbn
    elif is_valid_params(author_contains_query) and is_valid_params(isbn_exact_query) and is_valid_params(category_contains_query):
        searchedbook=bookitems.filter( Q(authors__icontains=author_contains_query) & Q(isbn=isbn_exact_query) & Q(genres__icontains=category_contains_query)).distinct()
    # title, authors, and isbn
    elif is_valid_params(title_contains_query) and is_valid_params(author_contains_query) and is_valid_params(isbn_exact_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) & Q(isbn=isbn_exact_query) & Q(authors__icontains=author_contains_query)).distinct()
    # title, isbn, and genres
    elif is_valid_params(title_contains_query) and is_valid_params(isbn_exact_query) and is_valid_params(category_contains_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) & Q(isbn=isbn_exact_query) & Q(genres__icontains=category_contains_query)).distinct()
    # title, authors, and genres
    elif is_valid_params(title_contains_query) and is_valid_params(author_contains_query) and is_valid_params(category_contains_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) & Q(authors__icontains=author_contains_query) & Q(genres__icontains=category_contains_query)).distinct()
    
    # when two of four inputs fulfill out
    # title and authors
    elif is_valid_params(title_contains_query) and is_valid_params(author_contains_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) | Q(authors__icontains=author_contains_query)).distinct()
    # title and isbn
    elif is_valid_params(title_contains_query) and is_valid_params(isbn_exact_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) | Q(isbn=isbn_exact_query)).distinct()
    # title and genres
    elif is_valid_params(title_contains_query) and is_valid_params(category_contains_query):
        searchedbook=bookitems.filter( Q(title__icontains=title_contains_query) | Q(genres__icontains=category_contains_query)).distinct()
    # author and genres
    elif is_valid_params(author_contains_query) and is_valid_params(category_contains_query):
        searchedbook=bookitems.filter( Q(authors__icontains=author_contains_query) | Q(genres__icontains=category_contains_query)).distinct()
    # author and isbn
    elif is_valid_params(author_contains_query) and is_valid_params(isbn_exact_query):
        searchedbook=bookitems.filter( Q(authors__icontains=author_contains_query) | Q(isbn=isbn_exact_query)).distinct()
    # isbn and genres
    elif is_valid_params(category_contains_query) and is_valid_params(isbn_exact_query):
        searchedbook=bookitems.filter( Q(genres__icontains=category_contains_query) | Q(isbn=isbn_exact_query)).distinct()
        
    # when only one of four input fulfills out
    elif is_valid_params(title_contains_query):
        searchedbook=bookitems.filter(title__icontains=title_contains_query)
    elif is_valid_params(author_contains_query):
        searchedbook=bookitems.filter(authors__icontains=author_contains_query)
    elif is_valid_params(isbn_exact_query):
        searchedbook=bookitems.filter(isbn=isbn_exact_query)
    elif is_valid_params(category_contains_query):
        searchedbook=bookitems.filter(genres__icontains=category_contains_query)
    context={
        'searchedbook':searchedbook
    }
    return render(request, 'library/search-books.html', context)
    
# Connect to Database and get all objects from bookitems table
def getAllBookitems():
    return Bookitems.objects.all()

"""[summary]
Function name: searchUsers
Function description: search all users in the database depending on the username and email. 
"""
def searchUsers(request):
    users=User.objects.filter(groups__name='member');
    searchedUser=''
    username_contains_query=request.GET.get('username_contains')
    email_exact_query=request.GET.get('email_exact')
    
    if is_valid_params(username_contains_query) and is_valid_params(email_exact_query):
        searchedUser=users.filter(Q(username__icontains=username_contains_query) & Q(email=email_exact_query))
    elif is_valid_params(username_contains_query):
        searchedUser=users.filter(Q(username__icontains=username_contains_query))
    elif is_valid_params(email_exact_query):
        searchedUser=users.filter(Q(email=email_exact_query))
    context={
        'searchedUser':searchedUser
    }
    return render(request, 'library/search-users.html', context)

"""[summary]
Function name: loginpage 
Function description: rendering user login page. When users submit the login form, it will search the matched username and password in the User table. After finding matched user, users will be redirected to home page.
Otherwise, users will receive message "Username/Password is incorrect". 
"""
@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.groups.all()[0].name=="member":
                member=LibraryMember.objects.get(user=user);
                if member.hold==True:
                    return redirect('/warning/')
                else:
                    login(request, user)
                    return redirect('/home/')
            else:
                login(request, user)
                return redirect('/home/')
        else:
            messages.info(request, 'Username/Password is incorrect.')

    context = {}
    return render(request, 'library/login.html', context)

"""[summary]
Function name: warning 
Function description: rendering warning page. 
"""
def warning(request):
    return render(request, 'library/warning.html')

"""[summary]
Function name: registerpage 
Function description: rendering user register page. When users submit the register form, it will create new user in the user table and LibraryMember table.
LibraryMembers will be directed to login page.
"""
@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            group=Group.objects.get(name='member')
            user.groups.add(group)
            LibraryMember.objects.create(
                user=user,
            )
            messages.success(request, 'Account was created for ' + username)
            return redirect('/login/')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'library/register.html', context)

"""[summary]
Function name: logoutuser 
Function description: logout users and redirect to login page after logout
"""
def logoutuser(request):
    logout(request)
    return redirect('/login/')

"""[summary]
Function name: LibraryMemberpanel 
Function description: rendering LibraryMemberpanel page. Only LibraryMembers can access to LibraryMemberpanel page and only when LibraryMembers login, they are able to access this page.
Note: LibraryMember panel page needs modifications. 
"""
@login_required(login_url='/login/')
#@allowed_user(allowed_roles=['LibraryMember'])
def memberpanel(request):
    #Getting user info
    user=request.user
    member=LibraryMember.objects.get(user=request.user.id)
    
    #Getting returned books and coutting the number of books according to the genres
    bookDict=getReturnedBook(member)

    # If member returns at least one book, we can return a recommendation book list 
    # else, we return the top 5 rating books. 
    if len(bookDict)>0:
        favoriteGenre=getFavoriteGenre(bookDict)
        recomBooks=getRecomBooks(favoriteGenre)
    else:
        recomBooks=getTopFiveBooks()
        
    #Getting books info 
    rentedBook=Rented_books.objects.filter(Q(member_id=member.id) & Q(obs=True))
    returnedBooks=Rented_books.objects.filter(Q(member_id=member.id) & Q(obs=False))
    reservedBooks=Reserved_books.objects.filter(Q(member_id=member.id) & Q(obs=True))
    
    #Getting number of books
    numOfRentedBooks=len(rentedBook)
    numOfReturnedBooks=len(returnedBooks)
    numOfReservedBooks=len(reservedBooks)
    
    #Getting feedbacks and reviews
    feedbacks=Feedbacks.objects.filter(member_id=member.id).filter(obs=True).order_by('-id')[:5]
    
    context={'user': user,
             'member':member,
             'rentedBook':rentedBook,
             'returnedBooks':returnedBooks,
             'reservedBooks':reservedBooks,
             'numOfRentedBooks':numOfRentedBooks,
             'numOfReturnedBooks':numOfReturnedBooks,
             'numOfReservedBooks':numOfReservedBooks,
             'recomBooks':recomBooks,
             'feedbacks':feedbacks}
    
    return render(request, 'library/memberpanel.html', context)

"""[summary]
Function name: getReturnedBook 
Function description: getting all returned books, counting the number of each genres, and returning the book count dictionary.
"""
def getReturnedBook(member):
    # Getting the returned books of this member
    returnBooks=Rented_books.objects.filter(Q(member=member))
    # Counting the genres and books 
    countBooks={}
    for book in returnBooks:
        # Getting genres 
        oneBookGenres=book.book.genres.split('|')
        # Counting genres and storing in the dict
        for bookGenres in oneBookGenres:
            if bookGenres in countBooks:
                countBooks[bookGenres] = countBooks[bookGenres]+1
            else:
                countBooks[bookGenres]=1
    #print(countBooks)
    return countBooks

"""[summary]
Function name: getFavoriteGenre 
Function description: getting the book counting dictionary and then finding the max counting of the genre, returning that genre.
"""

def getFavoriteGenre(bookDict):
    # get max count of books
    favoriteGenre=""
    maxCount=0
    for genre in bookDict:
        if bookDict[genre]>maxCount:
            favoriteGenre=genre
            maxCount=bookDict[genre]
    #print(favoriteGenre)
    return favoriteGenre

"""[summary]
Function name: getRecomBooks 
Function description: getting the favorite genre and then processing the bookitem tables to get a list of books that contain that genre, 
and ordering these books by average rating, returning the highest 5 books.
"""
def getRecomBooks(genre):
    books=Bookitems.objects.filter(Q(genres__icontains=genre))
    recomBooks=books.order_by('average_rating').reverse()[:5]
    #print(recomBooks)
    return recomBooks

"""[summary]
Function name: getTopFiveBooks 
Function description: push recommdated books to new members(member who does not rent a book yet), push the top 5 rating books.
"""
def getTopFiveBooks():
    # Get highest rating from bookitem table
    topFiveBooks=Bookitems.objects.all().order_by('average_rating').reverse()[:5]
    #print(topFiveBooks)
    return topFiveBooks

"""[summary]
Function name: returnedBooks 
Function description: rendering returnedBook page, getting returned books from rented_book table based on the member and user id.
"""
def returnedBooks(request):
    user=User.objects.get(id=request.user.id)
    member=LibraryMember.objects.get(user=user)
    returnedBookList=Rented_books.objects.filter(Q(member=member)&Q(obs=False))
    context={"returnedBooks":returnedBookList}
    return render(request, 'library/returnedBook.html', context)

"""[summary]
Function name: librarianpanel 
Function description: rendering librarianpanel page. Only librarian can access to librarianpanel page and only when librarian login, they are able to access this page.
Note: Librarian panel page needs modifications. 
"""
@login_required(login_url='/login/')
#@librarian_only
def librarianpanel(request):
    user=request.user
    librarian=Librarian.objects.get(user=request.user.id)
    feedback=Feedbacks.objects.all();
    context={'user':user, 
             'feedback':feedback,
             'librarian':librarian}
    return render(request, 'library/librarianpanel.html', context)

"""[summary]
Function name: editmemberinfo 
Function description: rendering user editLibraryMemberinfo page. When users submit the update_user_info form, it will update user info user table and LibraryMember table by using 
UserUpdateForm and MemberUpdateForm. Members will be redirected to memberpanel page after they updated their info.
"""
@login_required(login_url='/login/')
def editmemberinfo(request):
    checkUser=User.objects.filter(id=request.user.id)
    if checkUser[0].groups.all()[0].name=="member": 
        user_form = UserUpdateForm()
        if request.method=='POST':
            user_form=UserUpdateForm(request.POST,instance=request.user)
            member=LibraryMember.objects.get(user=request.user.id)
            member_form=MemberUpdateForm(request.POST, instance=member)
            if user_form.is_valid() and member_form.is_valid():
                user_form.save()
                member_form.save()
                messages.success(request,'Your account information has been updated!')
                return redirect('/memberpanel/')
        else:
            user_form=UserUpdateForm(instance=request.user)
            member=LibraryMember.objects.get(user=request.user.id)
            member_form=MemberUpdateForm(instance=member)
        
        context={
            'user_form':user_form,
            'member_form':member_form
        }
    elif checkUser[0].groups.all()[0].name=="librarian":
        userid_query=request.GET.get('userid')
        selectedUser=User.objects.get(id=userid_query)
        user_form = UserUpdateForm()
        if request.method=='POST':
            user_form=UserUpdateForm(request.POST,instance=selectedUser)
            member=LibraryMember.objects.get(user=userid_query)
            member_form=MemberUpdateForm(request.POST, instance=member)
            if user_form.is_valid() and member_form.is_valid():
                user_form.save()
                member_form.save()
                message=str(selectedUser.username)+'-'+str(selectedUser.email)+' account information has been updated!'
                messages.success(request,message)
                return redirect('/searchusers/')
        else:
            user_form=UserUpdateForm(instance=selectedUser)
            member=LibraryMember.objects.get(user=userid_query)
            member_form=MemberUpdateForm(instance=member)
        
        context={
            'user_form':user_form,
            'member_form':member_form
        }
    return render(request, 'library/editmemberinfo.html', context)

"""[summary]
Function name: bookdetails 
Function description: rendering bookdetails page, passing in all bookdetails stored in the bookitems table in the database.
"""
def bookdetails(request, book_id):
    bookitem=Bookitems.objects.get(id=book_id)
    context={
        "book":bookitem
    }
    return render(request,"library/bookdetails.html", context)

"""[summary]
Function name: editBookDetails 
Function description: rendering editbookdetails form, saving any changes of the bookitems, rendering page to bookdetail page after saving.
"""
@login_required(login_url='/login/')
#@librarian_only
def editBookDetails(request, book_id):
    bookitem=Bookitems.objects.get(id=book_id)
    if request.method=='POST':
        editbook_form=BookitemForm(request.POST, instance=bookitem)
        if editbook_form.is_valid():
            editbook_form.save()
            messages.success(request,'Book information has been updated!')
            return redirect('/bookitems/'+ str(book_id))
    else:
        editbook_form=BookitemForm(instance=bookitem)
    #print(bookitem)
    context={
        'editbook_form':editbook_form,
        'bookitem': bookitem
    }
    return render(request,"library/editbookdetails.html", context)

"""[summary]
Function name: addBook 
Function description: rendering addbook form, saving new bookitem to the bookitems table, rendering page to bookdetail page after saving.
"""
@login_required(login_url='/login/')
#@librarian_only
def addBook(request):
    book_form = BookitemForm()
    if request.method == 'POST':
        book_form = BookitemForm(request.POST)
        if book_form.is_valid():
            bookitem=book_form.save()
            messages.success(request, 'New Book was created ' + bookitem.title)
            return redirect('/bookitems/addbook/')
    else:
        book_form = BookitemForm(request.POST)
    context = {'form': book_form}
    return render(request, "library/addbook.html", context)

"""[summary]
Function name: deleteBook 
Function description: delete bookitems from the bookitems table.
"""
@login_required(login_url='/login/')
#@librarian_only
def deleteBook(request, book_id):
    bookitem=Bookitems.objects.get(id=book_id)
    bookitem.delete()
    messages.success(request, bookitem.title+' was deleted.')
    return redirect('/memberpanel/')

"""[summary]
Function name: createFeedback 
Function description:  rendering createFeedback form, saving new feedback to the feedbacks table, rendering page to memberpanel page after saving.
"""
@login_required(login_url='/login/')
def createFeedback(request):
    form=FeedbackForm()
    if request.method == 'POST':
        form=FeedbackForm(request.POST)
        if form.is_valid():
            member=LibraryMember.objects.get(user=request.user)
            feedback=form.save(commit=False)
            feedback.member_id=member.id
            feedback.save()
            return redirect('/memberpanel/')    
    context={'form':form}
    return render(request, 'library/createFeedback.html', context)

"""[summary]
Function name: updateFeedback 
Function description:  rendering updateFeedback form, updating exist feedback in the feedbacks table, rendering page to memberpanel page after saving changes.
"""
@login_required(login_url='/login/')
def updateFeedback(request, feedback_id):
    feedback=Feedbacks.objects.get(id=feedback_id)
    if request.method=='POST':
        form=FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request,'Feedback has been updated!')
            return redirect('/memberpanel/')
    else:
        form=FeedbackForm(instance=feedback)

    context={
        'form':form,
        'feedback': feedback
    }
    return render(request,"library/updatefeedback.html", context)

"""[summary]
Function name: deleteFeedback 
Function description: delete feedback from the feedbacks table.
"""
@login_required(login_url='/login/')
def deleteFeedback(request, feedback_id):
    feedback=Feedbacks.objects.get(id=feedback_id)
    feedback.obs=False
    feedback.save()
    messages.success(request, "'"+feedback.feedback_title+"'"+' was deleted.')
    return redirect('/memberpanel/')

"""[summary]
Function name: viewAllFeedback 
Function description: rendering allfeedback page, displaying all feedbacks that the login member created or all feedbacks for librarians.
"""
@login_required(login_url='/login/')
def viewAllFeedback(request):
    user=User.objects.get(id=request.user.id)
    if user.groups.all()[0].name=="member":
        member=LibraryMember.objects.get(user=user)
        feedbacks=Feedbacks.objects.filter(Q(member=member.id)&Q(obs=True))
    context={
        'feedbacks':feedbacks,
    }
    return render(request, 'library/allfeedback.html', context)

"""[summary]
Function name: registerLibrarian 
Function description: rendering librarian register page. When librarian submits the registerlibrarian form, it will create new librarian in the librarian and user tables.
librarian will be directed to login page.
"""
@login_required(login_url='/login/')
#@librarian_only
def registerLibrarian(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            group=Group.objects.get(name='librarian')
            user.groups.add(group)
            Librarian.objects.create(
                user=user,
            )
            messages.success(request, 'Librarian Account was created for ' + username)
            return redirect('/login/')
    else:
        form = CreateUserForm()
    context = {'form': form}
    return render(request, 'library/registerLibrarian.html', context)

"""[summary]
Function name: editLibrarianInfo 
Function description: rendering user editLibraryinfo page. When users submit the update_librarian_info form, it will update user info user table and librarian table by using 
UserUpdateForm and LibarianUpdateForm. Librarian will be redirected to librarian panel page after they updated their info.
"""
@login_required(login_url='/login/')
#@librarian_only
def editLibrarianInfo(request):
    user_form = UserUpdateForm()
    if request.method=='POST':
        user_form=UserUpdateForm(request.POST,instance=request.user)
        librarian=Librarian.objects.get(user=request.user.id)
        librarian_form=LibarianUpdateForm(request.POST, instance=librarian)
        if user_form.is_valid() and librarian_form.is_valid():
            user_form.save()
            librarian_form.save()
            messages.success(request,'Your account information has been updated!')
            return redirect('/librarianpanel/')
    else:
        user_form=UserUpdateForm(instance=request.user)
        librarian=Librarian.objects.get(user=request.user.id)
        librarian_form=LibarianUpdateForm(instance=librarian)

    context={
        'user_form':user_form,
        'librarian_form':librarian_form
    }
    return render(request, 'library/editLibrarianInfo.html', context)
    
"""[summary]
Function name: checkNotification 
Function description: rendering user's viewNotification page, displaying notification information and change the user_has_seen property to True.
"""
@login_required(login_url='/login/')
def checkNotification(request, notification_id):
    # Get notification item from table notification by notification primary key -- id
    notification=Notification.objects.get(id=notification_id)
    # Set user_has_been to true so it won't show up in the notification badge
    notification.user_has_seen=True
    notification.save()
    # Sent the argument to html file
    context={
        "notification":notification
    }
    return render(request,"library/viewNotification.html", context)

"""[summary]
Function name: deleteNotification 
Function description: delete notification by finding the notification and change the user_has_seen to True.
"""
@login_required(login_url='/login/')
def deleteNotification(request, notification_id):
    notification=Notification.objects.get(pk=notification_id)
    notification.user_has_seen=True
    notification.save()
    return redirect(request.META.get('HTTP_REFERER'))

"""[Summary]
Function name: sendNotification 
Function description: rendering sendNotification page. Only librarian can access to this page and only when librarian login, they are able to access this page. This function will pass in
the current librarian and selected member accounts info. The notification form will insert new notification data to the Notification table.   
"""
"""
Notification Type: 
1. Member reserved a book
2. Member unserved a book
3. Member can rent a book now
4. Librarian to Member Notification  
"""
@login_required(login_url='/login/')
#@librarian_only
def sendNotification(request, user_id):
    form=NotificationForm()
    from_Librarian=Librarian.objects.get(user=request.user)
    to_member=LibraryMember.objects.get(user=user_id)
    if request.method == 'POST':
        form=NotificationForm(request.POST)
        if form.is_valid():
            notification=form.save(commit=False)
            notification.from_Librarian=from_Librarian
            notification.to_member=to_member
            notification.notification_type=4
            notification.save()
            message='Notication sent to '+str(to_member.user.username)+ ' successfully!'
            messages.info(request, message)
            return redirect('/searchusers/') 
        #request.META.get('HTTP_REFERER') -- redirect to previous page
    context={'form':form, 'librarian':from_Librarian, 'member':to_member}
    return render(request, "library/sendNotification.html", context)

"""[Summary]
Function name: checkinPage 
Function description: rendering check-in page. Only librarian can access to this page and only when librarian login, they are able to access this page. This function will pass in
the selected user and member, and rented books.  
"""
@login_required(login_url='/login/')
#@librarian_only
def checkinPage(request, user_id):
    selectedUser=User.objects.get(id=user_id)
    selectedMember=LibraryMember.objects.get(user=user_id)
    rentedBooks=Rented_books.objects.filter(Q(member=selectedMember.id) & Q(obs=True))
    nowdate=datetime.datetime.now().date()
    for book in rentedBooks:
        if nowdate>book.return_date:
            #print(book.book.title, '+', book.return_date, '+ Return Late' )
            book.lateReturn=True
            book.save()
        else:
            pass
            #print(book.book.title, '+', book.return_date, '+ Good Status' )
    #print(selectedUser)
    
    context={'selectedUser':selectedUser, 'selectedMember':selectedMember, 'rentedBooks':rentedBooks, 'nowdate':nowdate}
    return render(request, "library/check-in.html", context)
    
"""[Summary]
Function name: checkoutPage 
Function description: rendering check-out page. Only librarian can access to this page and only when librarian login, they are able to access this page. This function will pass in
the selected user and member, and reserved books. 
""" 
@login_required(login_url='/login/')
#@librarian_only
def checkoutPage(request, user_id):
    selectedUser=User.objects.get(id=user_id)
    selectedMember=LibraryMember.objects.get(user=user_id)
    reservedBooks=Reserved_books.objects.filter(Q(member=selectedMember.id) & Q(obs=True))
    nowdate=datetime.datetime.now().date()
    for book in reservedBooks:
        if nowdate>book.deadline:
            #print(book.book.title, '+ Dealine: ', book.deadline, '+ Reserve Period Over, Cannnot rent now' )
            if book.canReserve==True:
                book.canReserve=False
        elif nowdate<book.deadline and nowdate>=book.available_rent_date:
            #print(book.book.title, '+ Dealine: ', book.deadline, '+ Available Rent Date', book.available_rent_date,'+ Ready to be rented' )
            if book.canReserve==False:
                book.canReserve=True
            book.save()
        elif nowdate<book.available_rent_date:
            pass
            #print(book.book.title, '+ Dealine: ', book.deadline, '+ book is not yet ready' )
    
    context={'selectedUser':selectedUser, 'selectedMember':selectedMember, 'reservedBooks':reservedBooks}
    return render(request, "library/check-out.html", context)

"""[Summary]
Function name: hold
Function description: rendering hold-account page
Note: Using usFilter class in filters.py to generate the filter result. 
"""  
@login_required(login_url='/login/')
#@librarian_only 
def pickUser(request):
    searchedmember = []
    member = getAllMember() 
    usFilter = UserFilter(request.GET, queryset=member)
    if usFilter.is_valid():
        searchedmember = usFilter.qs

    return render(request, 'library/hold-account.html', {
        'searchedmember': searchedmember,
        'usFilter': usFilter,
        'member': member,
    })

# Connect to Database and get all non-staff users from auth-user table
def getAllMember():
    return User.objects.select_related('librarymember').all().filter(is_staff=False)

"""[Summary]
Function name: holdAccount
Function description: hold member account by changing the hold to True
"""   
@login_required(login_url='/login/')
#@librarian_only
def holdAccount(request, user_id):
    selectedUser=User.objects.get(id=user_id)
    member=LibraryMember.objects.get(user=selectedUser)
    member.hold=True
    member.save()
    return redirect('/holdaccount/')

"""[Summary]
Function name: releaseAccount
Function description: release member account by changing the hold to False
"""   
@login_required(login_url='/login/')
#@librarian_only
def releaseAccount(request, user_id):
    selectedUser=User.objects.get(id=user_id)
    member=LibraryMember.objects.get(user=selectedUser)
    member.hold=False
    member.save()
    return redirect('/holdaccount/')

"""[Summary]
Function name: checkin
Function description: checkin function find the corresponging rented book in the rented_book table to unobservable, add 1 back to the available quantity of the book in the bookitems table.
check if the user returns the book late.
"""   
@login_required(login_url='/login/')
#@librarian_only
def checkin(request, user_id, book_id):
    # Find corresponding uesr, member and book
    user=User.objects.get(id=user_id)
    book=Bookitems.objects.get(id=book_id)
    member=LibraryMember.objects.get(user=user)
    # Define current date
    nowdate=datetime.datetime.now().date()
    # Find the rented book record and change it to unobservable
    rentdBookRecords=Rented_books.objects.filter(Q(member=member) & Q(book=book) & Q(obs=True))
    rentdBookRecord=rentdBookRecords[0];
    rentdBookRecord.obs=False
    # When returning book, add 1 to the available_quantity of that book
    book.available_quantity+=1
    book.save()
    # Determine if the return is late or not.
    if (nowdate>rentdBookRecord.return_date):
        rentdBookRecord.lateReturn=True
    else:
        rentdBookRecord.lateReturn=False
    rentdBookRecord.save()
    return redirect('/check_in/'+str(user_id))

"""[Summary]
Function name: checkout
Function description: checkout function calculate the rent date and return date for member, and create new rented_book object and save it in the rented_book table. 
Then change the corresponging reserved book in the reserved_book table to unobservable. 
"""   
@login_required(login_url='/login/')
#@librarian_only
def checkout(request, user_id, book_id):
    # Find corresponding uesr, member and book
    user=User.objects.get(id=user_id)
    book=Bookitems.objects.get(id=book_id)
    member=LibraryMember.objects.get(user=user)
    # Define current date
    nowdate=datetime.datetime.now().date()
    # Define return date which is 21 days away from the current date
    returndate=nowdate+datetime.timedelta(days=21)
    # Create a new rented book table record
    rentedBookRecord=Rented_books(book=book, title=book.title, member=member, rented_date=nowdate, return_date=returndate)
    rentedBookRecord.save()
    # Find the corresponding reserved Book Record
    reservedBookRecords=Reserved_books.objects.filter(Q(member=member) & Q(book=book) & Q(obs=True))
    reservedBookRecord=reservedBookRecords[0];
    reservedBookRecord.obs=False
    reservedBookRecord.save()
    rentSussess=book.title+" is rented successfully."
    messages.success(request, rentSussess)
    return redirect('/check_out/'+str(user_id))

"""[Summary]
Function name: reserveBook
Function description: reserveBook function check if the user already rent 10 books, if so, it won't allow the user to reserve book. If not, then it will create new reserve book record and save it 
in the reserveBook table, decrease the book's available quantity by 1.
"""   
@login_required(login_url='/login/')
def reserveBook(request, book_id):
    # Find corresponding uesr, member and book
    user=request.user
    member=LibraryMember.objects.get(user=user)
    selectedBook=Bookitems.objects.get(id=book_id)
    reservedBookRecordList=Reserved_books.objects.filter(Q(member=member) & Q(obs=True))
    #print(reservedBookRecordList)
    if (len(reservedBookRecordList)<10):
        # if there are books available to be rented then allow users to reserve the book
        if (selectedBook.available_quantity>0):
            # Define current date
            nowdate=datetime.datetime.now().date()
            # Define the deadline to rent this book
            deadline=nowdate+datetime.timedelta(days=10)
            # create records in reserved book table
            reservedBookRecord=Reserved_books(book=selectedBook, title=selectedBook.title, member=member,reserved_date=nowdate, deadline=deadline, available_rent_date=nowdate, canReserve=True)
            reservedBookRecord.save()
            # reserve book for users, decrease book's available quantity by 1
            selectedBook.available_quantity=selectedBook.available_quantity-1
            selectedBook.save()
            reserveSussess=selectedBook.title+" is reserved successfully."
            messages.info(request, reserveSussess)
        elif (selectedBook.available_quantity==0):
            # Define current date
            nowdate=datetime.datetime.now().date()
            # Search for rented book records
            rentedBookRecords=Rented_books.objects.filter(Q(book=selectedBook) & Q(obs=True))
            # Find the book that has the closest return_date
            rentedBookRecord=rentedBookRecords[0]
            for i in range(len(rentedBookRecords)):
                if (rentedBookRecords[i].return_date<rentedBookRecord.return_date):
                    rentedBookRecord=rentedBookRecords[i]
            #print(rentedBookRecord)
            # Set the deadline for the reserved book 
            deadline=rentedBookRecord.rented_date+datetime.timedelta(days=10)
            # Create records in reserved book table
            reservedBookRecord=Reserved_books(book=selectedBook, title=selectedBook.title, member=member,reserved_date=nowdate, deadline=deadline, available_rent_date=rentedBookRecord.return_date, canReserve=False)
            reservedBookRecord.save()
            reserveSussess=reservedBookRecord.book.title+" is reserved successfully."
            messages.info(request, reserveSussess)
    else:
        errorSent="Dear member, you already reserved 10 books. Please rent some books you reserved before reserving more books!"
        messages.info(request, errorSent)
    return redirect('/searchbooks/')

"""[Summary]
Function name: unreserveBook
Function description: unreservebook function finds the corresponding record in the reserved book table and then if canReserve is true, then it will add 1 back to the available quantity of that book 
and change the record of reserved book record to unobservable and save the change.
"""   
@login_required(login_url='/login/')
def unreserveBook(request, book_id):
    user=request.user
    member=LibraryMember.objects.get(user=user)
    selectedBook=Bookitems.objects.get(id=book_id)
    reservedBookRecords=Reserved_books.objects.filter(Q(member=member) & Q(book=selectedBook) & Q(obs=True))
    reservedBookRecord=reservedBookRecords[0]
    if (reservedBookRecord.canReserve==True):
        selectedBook.available_quantity+=1
        selectedBook.save()
        reservedBookRecord.obs=False
        reservedBookRecord.save()
    else:
        reservedBookRecord.obs=False
        reservedBookRecord.save()
    return redirect('/memberpanel/')
    


    