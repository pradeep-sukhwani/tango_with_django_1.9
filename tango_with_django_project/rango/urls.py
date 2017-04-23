from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', show_category, name='show_category'),
    url(r'^add_category', add_category, name='add_category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$', add_page, name='add_page'),
    url(r'^register/$', register, name='register'),
    url(r'^login/', user_login, name='user_login'),
    url(r'^logout/$', user_logout, name='user_logout'),
]
