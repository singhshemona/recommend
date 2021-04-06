"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from recommend import views as main_page_views
from users import views as user_views
# from . import views as home_views

router = routers.DefaultRouter()
router.register(r'books', main_page_views.BookView, 'book')
# router.register(r'bookclassify', main_page_views.BookClassify, 'bookclassify')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('api/', include(router.urls)),
    path('bookclassify/', main_page_views.bookClassifyView, name='search_book'),
    path('', main_page_views.home, name='home')
]
