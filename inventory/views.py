from django.shortcuts import render, redirect
from django.urls import reverse
# from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.models import Family, Category, Item, Checkin, Checkout
from django.contrib.auth import authenticate, login, logout

from inventory.forms import LoginForm
from inventory.forms import RegistrationForm

# BASIC VIEWS
def home(request): 
	return render(request, 'inventory/home.html')

def about(request):
	return render(request, 'inventory/about.html')

# AUTH VIEWS
def login_action(request):
    context = {}

    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'inventory/login.html', context)

    form = LoginForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'inventory/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('Home'))

def logout_action(request):
    logout(request)
    return redirect(reverse('Login'))

def register_action(request):
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'inventory/register.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'inventory/register.html', context)

    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password1'])

    login(request, new_user)
    return redirect(reverse('Home'))

# DATABASE VIEWS

def families_index(request):
    # sort in alphabetical order
    families_data = { "families" : Family.objects.order_by('name')}
    return render(request, 'inventory/families/index.html', families_data)

def categories_index(request):
    # sort in alphabetical order
    categories_data = { "categories" : Category.objects.order_by('name')}
    return render(request, 'inventory/categories/index.html', categories_data)

def items_index(request):
    return render(request, 'inventory/items/index.html', { "items" : Item.objects.all()})

def checkins_index(request):
    # sort in reverse chronological order
    checkins_data = { "checkins" : Checkin.objects.order_by('-datetime')}
    return render(request, 'inventory/checkins/index.html', checkins_data)

def checkouts_index(request):
    # sort in reverse chronological order
    checkouts_data = { "checkouts" : Checkout.objects.order_by('-datetime')}
    return render(request, 'inventory/checkouts/index.html', checkouts_data)
