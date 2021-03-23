"""flp URL Configuration

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
from django.urls import path
from inventory import views

urlpatterns = [
    path('', views.home, name="Home"),
    path('about/', views.about, name="About"),  
    path('login/', views.login_action, name='Login'),
    path('logout/', views.logout_action, name='Logout'),
    path('register/', views.register_action, name='Register'),
    path('admin/', admin.site.urls),
    path('families/index/', views.families_index, name="Families"),
    path('categories/index/', views.categories_index, name="Categories"),
    path('items/index/', views.items_index, name="Items"),
    path('checkins/index/', views.checkins_index, name="Checkins"),
    path('checkouts/index/', views.checkouts_index, name="Checkouts"),
]
