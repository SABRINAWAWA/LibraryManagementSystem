from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Bookitems, LibraryMember, Feedbacks
from .filters import BookitemsFilter
from .forms import CreateUserForm, UserUpdateForm, MemberUpdateForm, BookitemForm, FeedbackForm
from .decorators import unauthenticated_user, allowed_user, librarian_only

"""
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


"""
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
    
# Connect to Database and get all objects from bookitems table
def getAllBookitems():
    return Bookitems.objects.all()

"""
Function name: loginpage 
Function description: rendering user login page. When users submit the login form, it will search the matched username and password in the User table. After finding matched user, users will be redirected to home page.
Otherwise, users will receive message "Username/Password is incorrect". 
Note: Login Page Completed.
"""
@unauthenticated_user
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            messages.info(request, 'Username/Password is incorrect.')

    context = {}
    return render(request, 'library/login.html', context)
"""
Function name: registerpage 
Function description: rendering user register page. When users submit the register form, it will create new user in the user table and LibraryMember table.
LibraryMembers will be directed to login page.
Note: Register page needs modifications. 
"""
@unauthenticated_user
def registerpage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')
            group=Group.objects.get(name='LibraryMember')
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

"""
Function name: logoutuser 
Function description: logout users and redirect to login page after logout
"""
def logoutuser(request):
    logout(request)
    return redirect('/login/')

"""
Function name: LibraryMemberpanel 
Function description: rendering LibraryMemberpanel page. Only LibraryMembers can access to LibraryMemberpanel page and only when LibraryMembers login, they are able to access this page.
Note: LibraryMember panel page needs modifications. 
"""
#@login_required(login_url='/login/')
#@allowed_user(allowed_roles=['LibraryMember'])
def memberpanel(request):
    bookitems=[{
        'title': "Harry Potter and the Sorcerer's Stone",
        'author': 'J. K. Rowling'
    }, {
        'title': "Harry Potter and Chamber of Secrets",
        'author': 'J. K. Rowling'
    }, {
        'title': "Harry Potter and Prisoner of Azkaban",
        'author': 'J. K. Rowling'
    }, {
        'title': "Harry Potter and Goblet of Fire",
        'author': 'J. K. Rowling'
    },
    {
        'title': "Harry Potter and Order of the Phoenix",
        'author': 'J. K. Rowling'
    },
    {
        'title': "Harry Potter and Half-Blood Prince",
        'author': 'J. K. Rowling'
    },{
        'title': "Harry Potter and Deathly Hallows",
        'author': 'J. K. Rowling'
    }]
    user=request.user
    member=LibraryMember.objects.get(user=request.user.id)
    feedbacks=Feedbacks.objects.filter(member_id=member.id).filter(obs=True)
    context={'user': user,
             'member':member,
             'bookitems':bookitems,
             'feedbacks':feedbacks}
    return render(request, 'library/memberpanel.html', context)

"""
Function name: librarianpanel 
Function description: rendering librarianpanel page. Only librarian can access to librarianpanel page and only when librarian login, they are able to access this page.
Note: Librarian panel page needs modifications. 
"""
#@login_required(login_url='/login/')
#@librarian_only
def librarianpanel(request):
    context={}
    return render(request, 'library/librarianpanel.html', context)

"""
Function name: editmemberinfo 
Function description: rendering user editLibraryMemberinfo page. When users submit the update_user_info form, it will update user info user table and LibraryMember table by using 
UserUpdateForm and MemberUpdateForm. Members will be redirected to memberpanel page after they updated their info.
Note: editmemberinfo page Completed. 
"""
def editmemberinfo(request):
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
    #print(member)
    context={
        'user_form':user_form,
        'member_form':member_form
    }
    return render(request, 'library/editmemberinfo.html', context)

def bookdetails(request, book_id):
    bookitem=Bookitems.objects.get(id=book_id)
    context={
        "book":bookitem
    }
    return render(request,"library/bookdetails.html", context)

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

def deleteBook(request, book_id):
    bookitem=Bookitems.objects.get(id=book_id)
    bookitem.delete()
    messages.success(request, bookitem.title+' was deleted.')
    return redirect('/memberpanel/')

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

def deleteFeedback(request, feedback_id):
    feedback=Feedbacks.objects.get(id=feedback_id)
    feedback.obs=False
    feedback.save()
    messages.success(request, "'"+feedback.feedback_title+"'"+' was deleted.')
    return redirect('/memberpanel/')