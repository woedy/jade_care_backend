from django.db import models
from django.urls import path

from search.views import admin_search_view, admin_search_ajax, AdminSearchView

app_name = 'search'

urlpatterns = [
    #path('', admin_search_view, name='search_view'),
    path('', AdminSearchView.as_view(), name='search_view'),
    path('admin_search_ajax/', admin_search_ajax, name='admin_search_ajax'),
]