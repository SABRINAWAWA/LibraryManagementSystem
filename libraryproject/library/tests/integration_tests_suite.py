from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from library.models import *
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User, Group
from datetime import date
import time

class TestLibrarianPortal(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestLibrarianPortal, cls).setUpClass()
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install())

    def setUp(self):
        self.user = User.objects.create_user(username='corinne', password='librarian001') # creating a user
        self.group = Group(name="librarian") # creating librarian group
        self.group.save() # saving librarian group
        self.user.groups.add(self.group) # adding the created user to the librarian group
        Librarian.objects.create(user=self.user)
        self.user.is_staff=True
        self.user.save()

        self.user2 = User.objects.create_user(username='dima', password='librarymember001') # creating a user
        self.group2 = Group(name="member") # creating librarymember group
        self.group2.save() # saving librarymember group
        self.user2.groups.add(self.group2) # adding the created user to the librarmember group
        LibraryMember.objects.create(
                user=self.user2,
            )
        self.user2.is_staff=False
        self.user2.save()

        print(User.objects.all())
        print(Librarian.objects.all())
        print(LibraryMember.objects.all())

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        log_in_username = self.selenium.find_element_by_name('username')
        log_in_password = self.selenium.find_element_by_name('password')
        submit = self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('corinne')
        log_in_password.send_keys('librarian001')
        submit.send_keys(Keys.RETURN)

        print(User.objects.all())
        print(Librarian.objects.all())

        time.sleep(1)

    
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TestLibrarianPortal, cls).tearDownClass()

    def test_1_editLibrarianInfo(self):

        librarianpanel =  self.selenium.find_element_by_link_text('Librarian Portal')
        librarianpanel.send_keys(Keys.RETURN)
        time.sleep(5)

        edit_librarian = self.selenium.find_element_by_link_text('Edit Librarian Info')
        edit_librarian.send_keys(Keys.RETURN)
        edit_first_name = self.selenium.find_element_by_name('first_name')
        edit_first_name.send_keys('Corinne')
        edit_last_name = self.selenium.find_element_by_name('last_name')
        edit_last_name.send_keys('Huang')
        edit_email = self.selenium.find_element_by_name('email')
        edit_email.send_keys('chuan215@mail.ccsf.edu')
        edit_phone_number = self.selenium.find_element_by_name('phone')
        edit_phone_number.send_keys('4151231234')
        edit_address = self.selenium.find_element_by_name('address')
        edit_address.send_keys('library street')
        edtit_birthday = self.selenium.find_element_by_name('birthdate')
        birthday = date(2000,1,1).isoformat()
        submit = self.selenium.find_element_by_class_name('btn')

        edtit_birthday.send_keys(birthday)
        submit.send_keys(Keys.RETURN)
        time.sleep(5)

        assert 'chuan215@mail.ccsf.edu' in self.selenium.page_source

    def searchBook(self):
        # search the test book before adding and after adding

        search = self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)
        search_title = self.selenium.find_element_by_name('title_contains')
        search_title.send_keys('Harry Potter and the Order of the Phoenix (Harry Potter  #5)')
        time.sleep(2)
        search_book = self.selenium.find_element_by_class_name('btn')
        search_book.send_keys(Keys.RETURN)
        time.sleep(1)

        if not self.selenium.page_source.__contains__('Harry Potter and the Order of the Phoenix (Harry Potter  #5)'):
            execu = '''
            var scr = document.createElement('script');
            scr.type = 'text/javascript';
            scr.text = 'alert("No book matches. You can add test book now.")';
            document.head.appendChild(scr);
            '''
            self.selenium.execute_script(execu)
            a = self.selenium.switch_to.alert
            time.sleep(5)
            a.accept()

    def test_2_addbook(self):

        self.searchBook()
        librarianpanel =  self.selenium.find_element_by_link_text('Librarian Portal')
        librarianpanel.send_keys(Keys.RETURN)
        add_book = self.selenium.find_element_by_link_text('Add Book')
        add_book.send_keys(Keys.RETURN)
        add_title = self.selenium.find_element_by_name('title')
        add_title.send_keys('Harry Potter and the Order of the Phoenix (Harry Potter  #5)')
        add_authors = self.selenium.find_element_by_name('authors')
        add_authors.send_keys('J.K. Rowling/Mary GrandPré')
        add_average_rating = self.selenium.find_element_by_name('average_rating')
        add_average_rating.send_keys('4.49')
        add_ISBN = self.selenium.find_element_by_name('isbn')
        add_ISBN.send_keys('0439358078')
        add_format = self.selenium.find_element_by_name('format')
        add_format.send_keys('Paperback')
        add_imageURL = self.selenium.find_element_by_name('img_url')
        add_imageURL.send_keys(
            'https://upload.wikimedia.org/wikipedia/en/e/e7/Harry_Potter_and_the_Order_of_the_Phoenix_poster.jpg')
        add_edition = self.selenium.find_element_by_name('edition')
        add_edition.send_keys('4th Edition')
        add_genres = self.selenium.find_element_by_name('genres')
        add_genres.send_keys('Classical')
        add_stock_quantity = self.selenium.find_element_by_name('stock_quantity')
        add_stock_quantity.send_keys('5')
        add_availability = self.selenium.find_element_by_name('available_quantity')
        add_availability.send_keys('3')
        add_discription = self.selenium.find_element_by_name('description')
        add_discription.send_keys('Harry Potter and the Order of the Phoenix is a fantasy novel '
                                  'written by British author J. K. Rowling and the fifth novel in the'
                                  ' Harry Potter series. ')
        add = self.selenium.find_element_by_class_name('btn')
        add.send_keys(Keys.RETURN)
        time.sleep(2)
        self.searchBook()
        time.sleep(5)

    def test_3_register_librarian(self):

        librarianpanel =  self.selenium.find_element_by_link_text('Librarian Portal')
        librarianpanel.send_keys(Keys.RETURN)

        time.sleep(5)

        add_librarian =  self.selenium.find_element_by_link_text('Add New Librarian')
        add_librarian.send_keys(Keys.RETURN)

        register_username =  self.selenium.find_element_by_name('username')
        register_first_name =  self.selenium.find_element_by_name('first_name')
        register_last_name =  self.selenium.find_element_by_name('last_name')
        register_email =  self.selenium.find_element_by_name('email')
        register_password1 =  self.selenium.find_element_by_name('password1')
        register_password2 =  self.selenium.find_element_by_name('password2')
        submit = self.selenium.find_element_by_class_name('btn')

        register_username.send_keys('andid1973')
        register_first_name.send_keys('Andrey')
        register_last_name.send_keys('Didkovsky')
        register_email.send_keys('adidkovs@mail.ccsf.edu')
        register_password1.send_keys('123Test!')
        register_password2.send_keys('123Test!')
        submit.send_keys(Keys.RETURN)


        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('andid1973')
        log_in_password.send_keys('123Test!')
        submit.send_keys(Keys.RETURN)

        print(User.objects.all())
        print(Librarian.objects.all())

        time.sleep(5)

        assert 'andid1973' in  self.selenium.page_source

    def test_4_register_member(self):
      
        librarianpanel =  self.selenium.find_element_by_link_text('Librarian Portal')
        librarianpanel.send_keys(Keys.RETURN)

        time.sleep(5)

        add_librarian =  self.selenium.find_element_by_link_text('Add New Member')
        add_librarian.send_keys(Keys.RETURN)

        register_name =self.selenium.find_element_by_name('username')
        register_first_name = self.selenium.find_element_by_name('first_name')
        register_last_name = self.selenium.find_element_by_name('last_name')
        register_email = self.selenium.find_element_by_name('email')
        register_password1 = self.selenium.find_element_by_name('password1')
        register_password2 = self.selenium.find_element_by_name('password2')

        submit = self.selenium.find_element_by_class_name('btn')
        

        register_name.send_keys('Test')
        register_first_name.send_keys('Test1')
        register_last_name.send_keys('1tset')
        register_email.send_keys('Test@test.com')
        register_password1.send_keys('4321Andrey!')
        register_password2.send_keys('4321Andrey!')

        submit.send_keys(Keys.RETURN)

        time.sleep(5)


        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')



        log_in_username.send_keys('Test')
        log_in_password.send_keys('4321Andrey!')
        submit.send_keys(Keys.RETURN)


        print(User.objects.all())
        print(Librarian.objects.all())
        print(LibraryMember.objects.all())


        time.sleep(5)

        assert 'Test' in self.selenium.page_source

    def test_5_review_edit(self):

        self.book = Bookitems.objects.create(title = 'The Hunger Games',
            authors = 'Suzanne Collins',
            average_rating = '4.33',
            isbn = '9780440000000.0',
            format = 'hardcover',
            description = "Winning will make you famous. Losing means certain death.The nation of Panem, formed from a post-apocalyptic North America, is a country that consists of a wealthy Capitol region surrounded by 12 poorer districts. Early in its history, a rebellion led by a 13th district against the Capitol resulted in its destruction and the creation of an annual televised event known as the Hunger Games. In punishment, and as a reminder of the power and grace of the Capitol, each district must yield one boy and one girl between the ages of 12 and 18 through a lottery system to participate in the games. The 'tributes' are chosen during the annual Reaping and are forced to fight to the death, leaving only one survivor to claim victory.When 16-year-old Katniss's young sister, Prim, is selected as District 12's female representative, Katniss volunteers to take her place. She and her male counterpart Peeta, are pitted against bigger, stronger representatives, some of whom have trained for this their whole lives. , she sees it as a death sentence. But Katniss has been close to death before. For her, survival is second nature.",
            edition = 'First Edition',
            genres = 'fiction',
            img_url = 'https://images.gr-assets.com/books/1447303603l/2767052.jpg',
            stock_quantity = 5,
            available_quantity = 5
        ) # creating a bookitem
        self.review = Review.objects.create(book = self.book, author = 'abracadabrier', content = 'Great abracadabra!') # creating a review

        search =  self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('title_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('The Hunger Games')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)
        
        view =  self.selenium.find_element_by_link_text('View')
        view.send_keys(Keys.RETURN)

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        review =  self.selenium.find_element_by_link_text('Read The Reviews')
        review.send_keys(Keys.RETURN)

        time.sleep(2)

        edit =  self.selenium.find_element_by_link_text('Edit')
        edit.send_keys(Keys.RETURN)

        time.sleep(2)

        reviewer = self.selenium.find_element_by_name('author')
        text = self.selenium.find_element_by_name('content')
        submit =  self.selenium.find_element_by_class_name('btn')

        time.sleep(2)

        reviewer.clear()
        time.sleep(2)
        reviewer.send_keys('Dmitriy')
        time.sleep(2)
        text.clear()
        time.sleep(2)
        text.send_keys('The book is awesome. I highly recommend it!')
        time.sleep(2)
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        time.sleep(2)

        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('dima')
        log_in_password.send_keys('librarymember001')
        submit.send_keys(Keys.RETURN)
        
        time.sleep(2)

        search =  self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('title_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('The Hunger Games')
        submit.send_keys(Keys.RETURN)
        
        time.sleep(2)

        view =  self.selenium.find_element_by_link_text('View')
        view.send_keys(Keys.RETURN)

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        review =  self.selenium.find_element_by_link_text('Read The Reviews')
        review.send_keys(Keys.RETURN)

        time.sleep(2)

        assert 'The book is awesome. I highly recommend it!' in self.selenium.page_source





class TestMemberPortal(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(TestMemberPortal, cls).setUpClass()
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install())
        cls.selenium.implicitly_wait(15)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(TestMemberPortal, cls).tearDownClass()

    def test5_6_editMemberInfo(self):
        self.user = User.objects.create_user(username='corinne1', password='member001') # creating a user
        self.group = Group(name="member") # creating member group
        self.group.save() # saving member group
        self.user.groups.add(self.group) # adding the created user to the member group
        LibraryMember.objects.create(user=self.user)
        self.user.is_staff=False
        self.user.save()

        print(User.objects.all())
        print(LibraryMember.objects.all())

        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit = self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('corinne1')
        log_in_password.send_keys('member001')
        submit.send_keys(Keys.RETURN)
        time.sleep(2)


        print(User.objects.all())
        print(LibraryMember.objects.all())

        memberpanel = self.selenium.find_element_by_link_text('Member Portal')
        memberpanel.send_keys(Keys.RETURN)

        time.sleep(5)

        edit_member = self.selenium.find_element_by_link_text('Edit Member Info')
        edit_member.send_keys(Keys.RETURN)
        edit_first_name = self.selenium.find_element_by_name('first_name')
        edit_first_name.send_keys('Corinne')
        edit_last_name = self.selenium.find_element_by_name('last_name')
        edit_last_name.send_keys('Huang')
        edit_email = self.selenium.find_element_by_name('email')
        edit_email.send_keys('chuan215@mail.ccsf.edu')
        edit_phone_number = self.selenium.find_element_by_name('phone')
        edit_phone_number.send_keys('4151231234')
        edit_address = self.selenium.find_element_by_name('address')
        edit_address.send_keys('library street')
        edtit_birthday = self.selenium.find_element_by_name('birthdate')
        birthday = date(2000,1,1).isoformat()
        submit = self.selenium.find_element_by_class_name('btn')
        time.sleep(5)

        edtit_birthday.send_keys(birthday)
        submit.send_keys(Keys.RETURN)
        time.sleep(5)

        assert 'chuan215@mail.ccsf.edu' in self.selenium.page_source

    def test_7_register(self):

        user = User.objects.create_user(username='Aaron', password='librarimember002') # creating a user
        group = Group(name="member") # creating librarymember group
        group.save() # saving librarymember group
        user.groups.add(group) # adding the created user to the librarian group
        LibraryMember.objects.create(
                user=user,
            )
        user.is_staff=False
        user.save()

        self.selenium.get(('%s%s' % (self.live_server_url, '/register/')))

        register_name =self.selenium.find_element_by_name('username')
        register_first_name = self.selenium.find_element_by_name('first_name')
        register_last_name = self.selenium.find_element_by_name('last_name')
        register_email = self.selenium.find_element_by_name('email')
        register_password1 = self.selenium.find_element_by_name('password1')
        register_password2 = self.selenium.find_element_by_name('password2')

        submit = self.selenium.find_element_by_class_name('btn')
        

        register_name.send_keys('Test')
        register_first_name.send_keys('Test1')
        register_last_name.send_keys('1tset')
        register_email.send_keys('Test@test.com')
        register_password1.send_keys('4321Andrey!')
        register_password2.send_keys('4321Andrey!')

        submit.send_keys(Keys.RETURN)

        time.sleep(5)


        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('Test')
        log_in_password.send_keys('4321Andrey!')
        submit.send_keys(Keys.RETURN)


        print(User.objects.all())
        print(LibraryMember.objects.all())


        time.sleep(5)

        assert 'Test' in self.selenium.page_source

    def test_8_ReviewCreate(self):

        self.user = User.objects.create_user(username='dima', password='librarymember001') # creating a user
        self.group = Group(name="member") # creating librarymember group
        self.group.save() # saving librarymember group
        self.user.groups.add(self.group) # adding the created user to the librarmember group
        LibraryMember.objects.create(
                user=self.user,
            )
        self.user.is_staff=False
        self.user.save()

        self.book = Bookitems.objects.create(title = 'The Hunger Games',
            authors = 'Suzanne Collins',
            average_rating = '4.33',
            isbn = '9780440000000.0',
            format = 'hardcover',
            description = "Winning will make you famous. Losing means certain death.The nation of Panem, formed from a post-apocalyptic North America, is a country that consists of a wealthy Capitol region surrounded by 12 poorer districts. Early in its history, a rebellion led by a 13th district against the Capitol resulted in its destruction and the creation of an annual televised event known as the Hunger Games. In punishment, and as a reminder of the power and grace of the Capitol, each district must yield one boy and one girl between the ages of 12 and 18 through a lottery system to participate in the games. The 'tributes' are chosen during the annual Reaping and are forced to fight to the death, leaving only one survivor to claim victory.When 16-year-old Katniss's young sister, Prim, is selected as District 12's female representative, Katniss volunteers to take her place. She and her male counterpart Peeta, are pitted against bigger, stronger representatives, some of whom have trained for this their whole lives. , she sees it as a death sentence. But Katniss has been close to death before. For her, survival is second nature.",
            edition = 'First Edition',
            genres = 'fiction',
            img_url = 'https://images.gr-assets.com/books/1447303603l/2767052.jpg',
            stock_quantity = 5,
            available_quantity = 5
        ) # creating a bookitem
        self.review = Review.objects.create(book = self.book, author = 'abracadabrier', content = 'Great abracadabra!') # creating a review
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        
        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('dima')
        log_in_password.send_keys('librarymember001')
        submit.send_keys(Keys.RETURN)

        time.sleep(5)

        search =  self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)

        time.sleep(5)

        title = self.selenium.find_element_by_name('title_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('The Hunger Games')
        submit.send_keys(Keys.RETURN)

        view =  self.selenium.find_element_by_link_text('View')
        view.send_keys(Keys.RETURN)
        
        

        time.sleep(5)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        review =  self.selenium.find_element_by_link_text('Review This Book')
        review.send_keys(Keys.RETURN)
        

        reviewer = self.selenium.find_element_by_name('author')
        text = self.selenium.find_element_by_name('content')
        submit =  self.selenium.find_element_by_class_name('btn')

        
        reviewer.send_keys('Dmitriy')
        text.send_keys('The book is awesome. I highly recommend it!')
        time.sleep(5)
        submit.send_keys(Keys.RETURN)
        time.sleep(5)

        assert 'Thank you very much, Dmitriy!' in self.selenium.page_source

    def test_9_ViewReviews(self):

        self.user = User.objects.create_user(username='dima', password='librarymember001') # creating a user
        self.group = Group(name="member") # creating librarymember group
        self.group.save() # saving librarymember group
        self.user.groups.add(self.group) # adding the created user to the librarmember group
        LibraryMember.objects.create(
                user=self.user,
            )
        self.user.is_staff=False
        self.user.save()

        self.user2 = User.objects.create_user(username='lena', password='librarymember002') # creating a user
        self.user2.groups.add(self.group) # adding the created user to the librarmember group
        LibraryMember.objects.create(
                user=self.user2,
            )
        self.user2.is_staff=False
        self.user2.save()


        self.book = Bookitems.objects.create(title = 'The Hunger Games',
            authors = 'Suzanne Collins',
            average_rating = '4.33',
            isbn = '9780440000000.0',
            format = 'hardcover',
            description = "Winning will make you famous. Losing means certain death.The nation of Panem, formed from a post-apocalyptic North America, is a country that consists of a wealthy Capitol region surrounded by 12 poorer districts. Early in its history, a rebellion led by a 13th district against the Capitol resulted in its destruction and the creation of an annual televised event known as the Hunger Games. In punishment, and as a reminder of the power and grace of the Capitol, each district must yield one boy and one girl between the ages of 12 and 18 through a lottery system to participate in the games. The 'tributes' are chosen during the annual Reaping and are forced to fight to the death, leaving only one survivor to claim victory.When 16-year-old Katniss's young sister, Prim, is selected as District 12's female representative, Katniss volunteers to take her place. She and her male counterpart Peeta, are pitted against bigger, stronger representatives, some of whom have trained for this their whole lives. , she sees it as a death sentence. But Katniss has been close to death before. For her, survival is second nature.",
            edition = 'First Edition',
            genres = 'fiction',
            img_url = 'https://images.gr-assets.com/books/1447303603l/2767052.jpg',
            stock_quantity = 5,
            available_quantity = 5
        ) # creating a bookitem
        self.review = Review.objects.create(book = self.book, author = 'abracadabrier', content = 'Great abracadabra!') # creating a review
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        
        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('dima')
        log_in_password.send_keys('librarymember001')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        search =  self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('title_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('The Hunger Games')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)
        
        view =  self.selenium.find_element_by_link_text('View')
        view.send_keys(Keys.RETURN)

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        review =  self.selenium.find_element_by_link_text('Review This Book')
        review.send_keys(Keys.RETURN)

        time.sleep(2)

        reviewer = self.selenium.find_element_by_name('author')
        text = self.selenium.find_element_by_name('content')
        submit =  self.selenium.find_element_by_class_name('btn')

        reviewer.send_keys('Dmitriy')
        text.send_keys('The book is awesome. I highly recommend it!')
        time.sleep(2)
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        time.sleep(2)

        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('lena')
        log_in_password.send_keys('librarymember002')
        submit.send_keys(Keys.RETURN)
        
        time.sleep(2)

        search =  self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('title_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('The Hunger Games')
        submit.send_keys(Keys.RETURN)
        
        time.sleep(2)

        view =  self.selenium.find_element_by_link_text('View')
        view.send_keys(Keys.RETURN)

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        review =  self.selenium.find_element_by_link_text('Read The Reviews')
        review.send_keys(Keys.RETURN)

        time.sleep(2)

        print(User.objects.all())
        print(LibraryMember.objects.all())

        assert 'The book is awesome. I highly recommend it!' in self.selenium.page_source
        assert 'Great abracadabra!' in self.selenium.page_source

    def test_10_reserve_check_in_out_book(self):
        
        #Member
        user = User.objects.create_user(username='Aaron', password='librarimember001') # creating a user
        group = Group(name="member") # creating librarymember group
        group.save() # saving librarymember group
        user.groups.add(group) # adding the created user to the librarian group
        LibraryMember.objects.create(
                user=user,
            )
        user.is_staff=False
        user.save()

        #librarian
        self.user2 = User.objects.create_user(username='LibTest', password='LibrarianTest001') # creating a user
        self.group2 = Group(name="librarian") # creating librarymember group
        self.group2.save() # saving librarian group
        self.user2.groups.add(self.group2) # adding the created user to the librarian group
        Librarian.objects.create(
                user=self.user2,
            )
        self.user2.is_staff=True
        self.user2.save()

        self.book = Bookitems.objects.create(title = 'A Game of Thrones',
            authors = 'George R.R. Martin',
            average_rating = '4.45',
            isbn = '9780550000000.0',
            format = 'Mass Market Paperback',
            description = "Here is the first volume in George R. R. Martin’s magnificent cycle of novels that includes A Clash of Kings and A Storm of Swords. As a whole, this series comprises a genuine masterpiece of modern fantasy, bringing together the best the genre has to offer. Magic, mystery, intrigue, romance, and adventure fill these pages and transport us to a world unlike any we have ever experienced. Already hailed as a classic, George R. R. Martin’s stunning series is destined to stand as one of the great achievements of imaginative fiction.A GAME OF THRONESLong ago, in a time forgotten, a preternatural event threw the seasons out of balance. In a land where summers can last decades and winters a lifetime, trouble is brewing. The cold is returning, and in the frozen wastes to the north of Winterfell, sinister and supernatural forces are massing beyond the kingdom’s protective Wall. At the center of the conflict lie the Starks of Winterfell, a family as harsh and unyielding as the land they were born to. Sweeping from a land of brutal cold to a distant summertime kingdom of epicurean plenty, here is a tale of lords and ladies, soldiers and sorcerers, assassins and bastards, who come together in a time of grim omens.Here an enigmatic band of warriors bear swords of no human metal; a tribe of fierce wildlings carry men off into madness; a cruel young dragon prince barters his sister to win back his throne; and a determined woman undertakes the most treacherous of journeys. Amid plots and counterplots, tragedy and betrayal, victory and terror, the fate of the Starks, their allies, and their enemies hangs perilously in the balance, as each endeavors to win that deadliest of conflicts: the game of thrones.source: georgerrmartin.com",
            edition = 'Edition ',
            genres = 'fiction',
            img_url = 'https://images.gr-assets.com/books/1436732693l/13496.jpg',
            stock_quantity = 5,
            available_quantity = 5
        ) # creating a bookitem

        #Reserve Book
        self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
        
        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('Aaron')
        log_in_password.send_keys('librarimember001')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        search =  self.selenium.find_element_by_link_text('Search')
        search.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('title_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('A Game of Thrones')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        reserve =  self.selenium.find_element_by_link_text('Reserve')
        reserve.send_keys(Keys.RETURN)
        
        assert 'A Game of Thrones is reserved successfully.' in self.selenium.page_source
        
        time.sleep(2)

        member_portal =  self.selenium.find_element_by_link_text('Member Portal')
        member_portal.send_keys(Keys.RETURN)

        assert 'A Game of Thrones' in self.selenium.page_source

        time.sleep(2)

        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        time.sleep(2)

        #Check - Out Book
        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('LibTest')
        log_in_password.send_keys('LibrarianTest001')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        librarian_portal =  self.selenium.find_element_by_link_text('Librarian Portal')
        librarian_portal.send_keys(Keys.RETURN)

        time.sleep(2)

        check_out =  self.selenium.find_element_by_link_text('Check-Out')
        check_out.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('username_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        time.sleep(2)

        title.send_keys('Aaron')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        check_out =  self.selenium.find_element_by_link_text('Check-out (Rent Book)')
        check_out.send_keys(Keys.RETURN)

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        time.sleep(2)

        rent =  self.selenium.find_element_by_link_text('Rent')
        rent.send_keys(Keys.RETURN)

        assert 'A Game of Thrones is rented successfully.' in self.selenium.page_source

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[0])

        time.sleep(2)

        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        time.sleep(2)

        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('Aaron')
        log_in_password.send_keys('librarimember001')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        member_portal =  self.selenium.find_element_by_link_text('Member Portal')
        member_portal.send_keys(Keys.RETURN)

        assert 'A Game of Thrones' in self.selenium.page_source

        time.sleep(2)

        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        time.sleep(2)

        #Check - In Book
        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('LibTest')
        log_in_password.send_keys('LibrarianTest001')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        librarian_portal =  self.selenium.find_element_by_link_text('Librarian Portal')
        librarian_portal.send_keys(Keys.RETURN)

        time.sleep(2)

        check_in =  self.selenium.find_element_by_link_text('Check-In')
        check_in.send_keys(Keys.RETURN)

        time.sleep(2)

        title = self.selenium.find_element_by_name('username_contains')
        submit =  self.selenium.find_element_by_class_name('btn')

        title.send_keys('Aaron')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        check_in =  self.selenium.find_element_by_link_text('Check-in (Return Book)')
        check_in.send_keys(Keys.RETURN)

        time.sleep(2)

        wHandles = self.selenium.window_handles

        self.selenium.switch_to.window(wHandles[1])

        time.sleep(2)

        return_book =  self.selenium.find_element_by_link_text('Return')
        return_book.send_keys(Keys.RETURN)

        time.sleep(2)

        log_out =  self.selenium.find_element_by_link_text('Log out')
        log_out.send_keys(Keys.RETURN)

        time.sleep(2)

        log_in_username =  self.selenium.find_element_by_name('username')
        log_in_password =  self.selenium.find_element_by_name('password')
        submit =  self.selenium.find_element_by_class_name('btn')

        log_in_username.send_keys('Aaron')
        log_in_password.send_keys('librarimember001')
        submit.send_keys(Keys.RETURN)

        time.sleep(2)

        member_portal =  self.selenium.find_element_by_link_text('Member Portal')
        member_portal.send_keys(Keys.RETURN)

        time.sleep(2)

        return_details =  self.selenium.find_element_by_link_text('Details')
        return_details.send_keys(Keys.RETURN)

        assert 'A Game of Thrones' in self.selenium.page_source

        time.sleep(2)



  

















