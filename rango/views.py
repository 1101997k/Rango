from django.shortcuts import render
from django.http import HttpResponse
#import category model
from rango.models import Category, Page

def index(request):
    #query database for list of all categories currently stored
    #order by number of likes in descending order, retrieve top 5 only
    #and place list in context_dict dictionary that will be passed to template

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context_dict)

def about(request):
    return render(request, 'rango/about.html')

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
