from django.urls import path

from search.api.views import search_view

app_name = 'search_api'

urlpatterns = [
    path('search-list/', search_view, name="search-list"),

]