from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
# from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from inventory.models import Category, Item, ItemTransaction, Checkin, Checkout
from django.contrib.auth import authenticate, login, logout

from inventory.forms import LoginForm
from inventory.forms import RegistrationForm
from inventory.forms import AddItemForm, AddItemOutForm

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
def additem_action(request):
    context = {}

    if request.method == 'GET':
        return redirect(reverse('Checkin'))

    if request.method == 'POST':
        form = AddItemForm(request.POST)
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
    
        tx = serializers.serialize("json", [ ItemTransaction(item=item, quantity=quantity), ])
        if not 'transactions' in request.session or not request.session['transactions']:
            request.session['transactions'] = [tx]
        else:
            saved_list = request.session['transactions']
            saved_list.append(tx)
            request.session['transactions'] = saved_list

        return redirect(reverse('Checkin'))


def checkin_action(request):
    context = {}
        
    # Create transactions if they don't exist
    if not 'transactions' in request.session or not request.session['transactions']:
        request.session['transactions'] = []

    # Deserialize transactions 
    serialized_transactions = request.session['transactions']
    transactions = []
    for tx in serialized_transactions:
        for deserialized_transaction in serializers.deserialize("json", tx):
            transactions.append(deserialized_transaction.object)

    if request.method == 'GET':
        context['items'] = Item.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = AddItemForm()
        context['transactions'] = transactions
        return render(request, 'inventory/checkin.html', context)

    checkin = Checkin()
    checkin.save()

    for tx in transactions:
        tx.save()

        checkin.items.add(tx)

        tx.item.quantity += tx.quantity
        tx.item.save()

    del request.session['transactions']
    request.session.modified = True

    return redirect(reverse('Home'))

# CHECKOUT VIEWS
def additemout_action(request):
    context = {}

    if request.method == 'GET':
        return redirect(reverse('Checkout'))

    if request.method == 'POST':
        form = AddItemOutForm(request.POST)
        context['form'] = form

        if not form.is_valid():
            return render(request, 'inventory/checkout.html', context)

        category = form.cleaned_data['category']
        name = form.cleaned_data['name']
        price = form.cleaned_data['price']
        quantity = form.cleaned_data['quantity']
        # family = form.cleaned_data['family']

        item = Item.objects.filter(name=name).first()
        if not item:
            newItem = Item(category=category, name=name, price=price)
            newItem.save()
            item = newItem
    
        tx = serializers.serialize("json", [ ItemTransaction(item=item, quantity=quantity), ])
        if not 'transactions' in request.session or not request.session['transactions']:
            request.session['transactions'] = [tx]
        else:
            saved_list = request.session['transactions']
            saved_list.append(tx)
            request.session['transactions'] = saved_list

        return redirect(reverse('Checkout'))


def checkout_action(request):
    context = {}
        
    # Create transactions if they don't exist
    if not 'transactions' in request.session or not request.session['transactions']:
        request.session['transactions'] = []

    # Deserialize transactions 
    serialized_transactions = request.session['transactions']
    transactions = []
    for tx in serialized_transactions:
        for deserialized_transaction in serializers.deserialize("json", tx):
            transactions.append(deserialized_transaction.object)

    if request.method == 'GET':
        context['items'] = Item.objects.all()
        context['categories'] = Category.objects.all()
        context['form'] = AddItemOutForm()
        context['transactions'] = transactions
        return render(request, 'inventory/checkout.html', context)

    checkout = Checkout()
    checkout.save()

    for tx in transactions:
        tx.save()

        checkout.items.add(tx)

        tx.item.quantity += tx.quantity
        tx.item.save()

    del request.session['transactions']
    request.session.modified = True

    return redirect(reverse('Home'))