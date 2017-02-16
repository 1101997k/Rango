from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#import category model
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from datetime import datetime
# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        #update the last visit cookie now that we have updated the count
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        # set the last visit cookie
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    # Obtain our Response object early so we can add cookie information.
    # Call function to handle the cookies
    visitor_cookie_handler(request)
    context_dict = {'categories': category_list,
                    'pages': page_list,
                    'visits': request.session['visits']}

    response = render(request, 'rango/index.html', context_dict)
    # Return response back to the user, updating any cookies that need changed.
    return response

def about(request):
    visitor_cookie_handler(request)

    context_dict = {'visits': request.session['visits']}
    return render(request, 'rango/about.html', context_dict)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        #does category exist with given slug, if not DoesNotExist exception
        category = Category.objects.get(slug=category_name_slug)

        #retrieve all associated pages
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        #get here if category was not found, template display no category
        context_dict['category'] = None
        context_dict['pages'] = None

    #render response and return to client
    return render(request, 'rango/category.html', context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    #a HTTP post
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            #provided with valid form, save new category to database
            form.save(commit=True)
            return index(request)
        else:
            #supplied form contained errors, print to terminal
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form':form})

#function to add a page
@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context_dict)

# register form
def register(request):
    # boolean value, was reg successful
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # if two forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # save data to DB
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # sort out UserProfile instance, commit=False delays saving model
            # until we are ready
            profile = profile_form.save(commit=False)
            profile.user = user
             # Did the user provide a profile picture?
             # If so, we need to get it from the input form and #put it in the UserProfile model.
            if 'picture' in request.FILES:
                 profile.picture = request.FILES['picture']
            # Now we save the UserProfile model instance.
            profile.save()
            # Update our variable to indicate that the template
            # registration was successful.
            registered = True

        else:
            # invalid form, print problems to terminal
            print(user_form.errors, profile_form.errors)

    else:
        # not a HTTP post, render form
        user_form = UserForm()
        profile_form = UserProfileForm()

    # render template
    return render(request, 'rango/register.html',
                    {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # use django authentication, User object returned if valid
        user = authenticate(username=username, password=password)

        # if we have user object, details are correct
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")

        else:
            print("Invalid login details: {0}, {1}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        # user has not tried to login, show form
        return render(request, 'rango/login.html', {})

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
