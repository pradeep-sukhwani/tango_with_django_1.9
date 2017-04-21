# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from models import *
from forms import *


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

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=True)
            # print category, category.slug
            return index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()
        return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print form.errors
    else:
        context_dict = {'category': category, 'form': form}
        return render(request, 'rango/add_page.html', context_dict)
