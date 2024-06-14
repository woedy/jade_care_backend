"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from mysite.views import welcome_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", welcome_page, name="welcome_page"),

    path("home/",  include('home_page.urls', 'home_page')),
    path("accounts/",  include('accounts.urls', 'accounts')),
    path("user_profile/", include('user_profile.urls', 'user_profile')),
    path("posts/", include('posts.urls', 'posts')),
    path("search/", include('search.urls', 'search')),
    path("appointments/", include('appointments.urls', 'appointments')),
    path("general_checkup/", include('general_checkup.urls', 'general_checkup')),
    path("prescriptions/", include('prescriptions.urls', 'prescriptions')),
    path("medical_centers/", include('medical_centers.urls', 'medical_centers')),
    path("communications/", include('communications.urls', 'communications')),
    path("financials/", include('financials.urls', 'financials')),

    # REST-framework
    path('api/accounts/', include('accounts.api.urls', 'accounts_api')),




]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)