from django.shortcuts import render, redirect
from django.urls import reverse
# from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.models import Category, Item, ItemTransaction, Checkin
from django.contrib.auth import authenticate, login, logout

from inventory.forms import LoginForm
from inventory.forms import RegistrationForm
from inventory.forms import CheckinForm

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

# CHECKIN VIEWS
def checkin_action(request):
    context = {}

    if request.method == 'GET':
        context['items'] = Item.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = CheckinForm()
        return render(request, 'inventory/checkin.html', context)

    form = CheckinForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        return render(request, 'inventory/checkin.html', context)

    category = form.cleaned_data['category']
    name = form.cleaned_data['name']
    price = form.cleaned_data['price']
    quantity = form.cleaned_data['quantity']

    item = Item.objects.filter(name=name).first()
    if not item:
        newItem = Item(category=category, name=name, price=price)
        newItem.save()
        item = newItem
    
    tx = ItemTransaction(item=item, quantity=quantity)
    tx.save()

    checkin = Checkin()
    checkin.save()
    # checkin = Checkin(user=request.user)
    checkin.items.add(tx)

    item.quantity += tx.quantity
    item.save()

    return redirect(reverse('Home'))