# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import *
from forms import *
from datetime import datetime
from registration.backends.simple.views import RegistrationView

# Create your views here.

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '0'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    # if (datetime.now() - last_visit_time).days > 0:
    if datetime.now() != last_visit_time:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits

def index(request):
    # return HttpResponse('Rango says hey there partner!\
    #     <a href="/rango/about">About</a>')
    # context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy,\
    #                 cupcake!"}
    # return render(request, 'rango/index.html', context=context_dict)
    request.session.set_test_cookie()
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/index.html', context_dict)

def about(request):
    request.session.set_test_cookie()
    data = {
        'my_name': "Pradeep Sukhwani"
    }
    # return HttpResponse('Rango says here is the index page. <a href="/rango/">Index</a>')
    # if request.session.test_cookie_worked(): # Chap 4-A
    #     print "Test cookie worked"  # Chap 4-A
        # request.session.delete_test_cookie() # Chap 4-A
    visitor_cookie_handler(request)
    data['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=data)

def show_category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
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

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print user_form.errors, profile_forms.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('rango:index'))
            else:
                return HttpResponse('Your Rango account has been disabled')
        else:
            return render(request, 'rango/user_login.html', {'errors_msg': 'Username or password you provided was incorrect', 'login_form': UserProfileForm(request.POST)})
    else:
        return render(request, 'rango/user_login.html', {})

@login_required
def restricted(request):
    # my_data = {'data': data}
    return render(request, 'rango/restricted.html', {})
    # return HttpResponse('Since you are logged in, you can see this content.')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('rango:index'))

def track_url(request):
    page_id = None
    url = 'rango:index'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET.get('page_id')
            try:
                page = Page.objects.get(id=page_id)
                page.views += 1
                page.save()
                url = page.url
            except:
                pass
    return HttpResponseRedirect(url)

@login_required
def register_profile(request):
    form = UserProfileForm()
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print form.errors
    
    context_dict = {'form':form}
    return render(request, 'rango/profile_registration.html', context_dict)

class MyRegistrationView(RegistrationView):
    def get_success_url(self, user):
        return '/rango/'

@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return redirect('index')
    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'picture': userprofile.picture})
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print form.errors
        
        return render(request, 'rango/profile.html', {'userprofile': userprofile, 'selecteduser': user, 'form': form})
