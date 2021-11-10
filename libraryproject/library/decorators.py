from django.http import HttpResponse
from django.shortcuts import redirect

"""[summary]
Function name: unauthenticated_user
Function description: this function check if the user is authenticated, if not, then the function will redirect to the home page.
"""
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/home/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

"""[summary]
Function name: allowed_user
Function description: this function takes in allowed roles name and then check if the groups that the user belongs to is 
contained in the inputted parameter. If yes, then we can allow the user to access that page, otherwise the user will be 
warned that he or she is not allowed to access that page.
"""
def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

"""[summary]
Function name: librarian_only
Function description: this function check if the user is a librarian or not, if not, then will redirected to home page. 
Otherwise, the librarian can access the web page.
"""
def librarian_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name
        if group=='member':
            return redirect('/home/')
        if group =='librarian':
            return view_func(request, *args, **kwargs)
    return wrapper_func