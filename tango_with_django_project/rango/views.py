# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from models import *

# Create your views here.


def index(request):
    # return HttpResponse('Rango says hey there partner! <a href="/rango/about">About</a>')
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupcake!"}
    # return render(request, 'rango/index.html', context=context_dict)

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}

    return render(request, 'rango/index.html', context_dict)


def about(request):
    data = {
        'my_name': "Pradeep Sukhwani"
    }
    # return HttpResponse('Rango says here is the index page. <a href="/rango/">Index</a>')
    return render(request, 'rango/about.html', context=data)

def show_category(request, category_name_slug):
	context_dict = {}

	try:
		category = Category.objects.get(slug=category_name_slug)
		pages = Page.objects.filter(category=category)
		context_dict['pages'] = pages
		context_dict['category'] = category
	except Category.DoesNotExist:
		context_dict['category'] = None
		context_dict['pages'] = None

	return render(request, 'rango/category.html', context_dict)

def most_viewed_pages(request):
    pass
