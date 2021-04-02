
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.http import JsonResponse
from django_tables2 import SingleTableView
from .tables import FamilyTable, CategoryTable, ItemTable, CheckinTable, CheckoutTable

from django.contrib import messages
from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from inventory.models import Family, Category, Item, Checkin, Checkout, ItemTransaction
from inventory.forms import LoginForm, RegistrationForm, AddItemForm, AddItemOutForm, CheckOutForm

from datetime import date, datetime, timedelta
import csv

DEFAULT_PAGINATION_SIZE = 25


######################### BASIC VIEWS #########################

def home(request): 
	return render(request, 'inventory/home.html')

def about(request):
	return render(request, 'inventory/about.html')


######################### AUTH VIEWS ##########################

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


######################### REPORT GENERATION #########################
@login_required
def generate_report(request):
    context = {}

    if 'start-date' in request.POST \
        and 'end-date' in request.POST \
        and 'tx-type' in request.POST \
        and (request.POST['tx-type'] in ['Checkin', 'Checkout']):

        context['endDate'] = request.POST['end-date']
        context['startDate'] = request.POST['start-date']
        context['tx'] = request.POST['tx-type']

        endDatetime = datetime.strptime('{} 23:59:59'.format(context['endDate']), '%Y-%m-%d %H:%M:%S')

        if request.POST['tx-type'] == 'Checkin':
            context['results'] = Checkin.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()
        else:
            context['results'] = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()

        context['totalValue'] = 0 
        for result in context['results']:
            context['totalValue'] = result.getValue() + context['totalValue']

        if 'export' in request.POST:
            qs = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=context['endDate']).all()
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=data.csv'
            writer = csv.writer(response)
            if qs is not None:
                writer.writerow(["date", "family", "item", "quantity", "price", "total value"])
                for c in qs:
                    for tx in c.items.all():
                        writer.writerow([
                            c.datetime,
                            c.family,
                            tx.item.name,
                            tx.quantity,
                            tx.item.price, 
                            0 if tx.item.price is None else tx.quantity*tx.item.price
                        ])
            return response

        if 'export_table' in request.POST:
            qs = context['results']
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=data.csv'
            writer = csv.writer(response)

            if len(qs) != 0:
                field_names = [f.name for f in qs.model._meta.get_fields()]
                writer.writerow(field_names)
                for i in qs:
                    row = []
                    for f in field_names:
                        if f == "items":
                            txs = ''.join([str(tx) for tx in i.items.all()])
                            row.append(txs)
                        else:
                            row.append(getattr(i, f))
                    writer.writerow(row)
            return response

        context['results'] = getPagination(request, context['results'], DEFAULT_PAGINATION_SIZE)
        return render(request, 'inventory/generate_report.html', context)

    today = date.today()
    weekAgo = today - timedelta(days=7)
    context['endDate'] = today.strftime('%Y-%m-%d')
    context['startDate'] = weekAgo.strftime('%Y-%m-%d')
    return render(request, 'inventory/generate_report.html', context)

######################### REPORT GENERATION #########################
@login_required
def analytics(request):
    context = {}

    context['results'] = Checkout.objects.all()

    return render(request, 'inventory/analytics.html', context)

    if 'start-date' in request.POST \
        and 'end-date' in request.POST \
        and 'tx-type' in request.POST \
        and (request.POST['tx-type'] in ['Checkin', 'Checkout']):

        context['endDate'] = request.POST['end-date']
        context['startDate'] = request.POST['start-date']
        context['tx'] = request.POST['tx-type']

        endDatetime = datetime.strptime('{} 23:59:59'.format(context['endDate']), '%Y-%m-%d %H:%M:%S')

        if request.POST['tx-type'] == 'Checkin':
            context['results'] = Checkin.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()
        else:
            context['results'] = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()

        context['totalValue'] = 0 
        for result in context['results']:
            context['totalValue'] = result.getValue() + context['totalValue']

        if 'export' in request.POST:
            qs = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=context['endDate']).all()
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=data.csv'
            writer = csv.writer(response)
            if qs is not None:
                writer.writerow(["date", "family", "item", "quantity", "price", "total value"])
                for c in qs:
                    for tx in c.items.all():
                        writer.writerow([
                            c.datetime,
                            c.family,
                            tx.item.name,
                            tx.quantity,
                            tx.item.price, 
                            0 if tx.item.price is None else tx.quantity*tx.item.price
                        ])
            return response

        if 'export_table' in request.POST:
            qs = context['results']
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=data.csv'
            writer = csv.writer(response)

            if len(qs) != 0:
                field_names = [f.name for f in qs.model._meta.fields]
                writer.writerow(field_names)
                for i in qs:
                    row = []
                    for f in field_names:
                        if f == "items":
                            txs = ', '.join([str(tx) for tx in i.items.all()])
                            row.append(txs)
                        else:
                            row.append(getattr(i, f))
                    writer.writerow(row)
            return response

        context['results'] = getPagination(request, context['results'], DEFAULT_PAGINATION_SIZE)
        return render(request, 'inventory/generate_report.html', context)

    today = date.today()
    weekAgo = today - timedelta(days=7)
    context['endDate'] = today.strftime('%Y-%m-%d')
    context['startDate'] = weekAgo.strftime('%Y-%m-%d')
    return render(request, 'inventory/generate_report.html', context)

  
###################### CHECKIN/CHECKOUT VIEWS ######################

# Add item to cart
@login_required
def addtocart_action(request, location):
    context = {}

    context['location'] = location

    if request.method == 'GET':
        if location == 'in':
            context['form'] = AddItemForm()
        else:
            context['form'] = AddItemOutForm()
        
        return render(request, 'inventory/additem.html', context)

    if request.method == 'POST':
        if location == 'in':
            form = AddItemForm(request.POST)
        else:
            form = AddItemOutForm(request.POST)

        context['form'] = form

        if not form.is_valid():
            return render(request, 'inventory/additem.html', context)

        # category = form.cleaned_data['category']
        name = form.cleaned_data['name']
        quantity = form.cleaned_data['quantity']

        item = Item.objects.filter(name=name).first()
    
        tx = serializers.serialize("json", [ ItemTransaction(item=item, quantity=quantity), ])
        if not 'transactions-' + location in request.session or not request.session['transactions-' + location]:
            request.session['transactions-' + location] = [tx]
        else:
            saved_list = request.session['transactions-' + location]
            saved_list.append(tx)
            request.session['transactions-' + location] = saved_list

        messages.success(request, 'Item Added')
        return redirect(reverse('Check' + location))


# Remove item from cart
def removeitem_action(request, index, location):
    saved_list = request.session['transactions-' + location]
    saved_list.pop(index)
    request.session['transactions-' + location] = saved_list

    messages.success(request, 'Item Removed')
    return redirect(reverse('Check' + location))


# Checkin view
@login_required
def checkin_action(request):
    context = {}
        
    # Create transactions if they don't exist
    if not 'transactions-in' in request.session or not request.session['transactions-in']:
        request.session['transactions-in'] = []

    # Deserialize transactions 
    serialized_transactions = request.session['transactions-in']
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

    if not transactions:
        messages.warning(request, 'Could not create checkin: No items added')
        return redirect(reverse('Checkin'))

    checkin = Checkin(user=request.user)
    checkin.save()

    for tx in transactions:
        tx.save()

        checkin.items.add(tx)

        tx.item.quantity += tx.quantity
        tx.item.save()

    del request.session['transactions-in']
    request.session.modified = True

    messages.success(request, 'Checkin created')
    return redirect(reverse('Checkin'))

  
# Checkout view
@login_required
def checkout_action(request):
    context = {}
        
    # Create transactions if they don't exist
    if not 'transactions-out' in request.session or not request.session['transactions-out']:
        request.session['transactions-out'] = []

    # Deserialize transactions 
    serialized_transactions = request.session['transactions-out']
    transactions = []
    for tx in serialized_transactions:
        for deserialized_transaction in serializers.deserialize("json", tx):
            transactions.append(deserialized_transaction.object)

    if request.method == 'GET':
        context['items'] = Item.objects.all()
        context['categories'] = Category.objects.all()
        context['formcheckout'] = CheckOutForm()
        context['transactions'] = transactions
        return render(request, 'inventory/checkout.html', context)

    form = CheckOutForm(request.POST)

    if not form.is_valid():
        return render(request, 'inventory/checkout.html', context)

    family = form.cleaned_data['family']

    if not transactions:
        messages.warning(request, 'Could not create checkout: No items added')
        return redirect(reverse('Checkout'))

    checkout = Checkout(family=family, user=request.user)
    checkout.save()

    for tx in transactions:
        tx.save()

        checkout.items.add(tx)

        tx.item.quantity -= tx.quantity
        tx.item.save()

    del request.session['transactions-out']
    request.session.modified = True

    messages.success(request, 'Checkout created')
    return redirect(reverse('Checkout'))

  
def autocomplete(request):
    if 'term' in request.GET:
        qs = Item.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for item in qs:
            names.append(item.name)
        return JsonResponse(names, safe=False)
  
  
######################### DATABASE VIEWS #########################

class FamilyIndexView(LoginRequiredMixin, SingleTableView):
    model = Family
    table_class = FamilyTable
    template_name = "inventory/families/index.html"

class CategoryIndexView(LoginRequiredMixin, SingleTableView):
    model = Category
    table_class = CategoryTable
    template_name = "inventory/categories/index.html"

class ItemIndexView(LoginRequiredMixin, SingleTableView):
    model = Item
    table_class = ItemTable
    template_name = "inventory/items/index.html"

class CheckinIndexView(LoginRequiredMixin, SingleTableView):
    model = Checkin
    table_class = CheckinTable
    template_name = "inventory/checkins/index.html"

class CheckoutIndexView(LoginRequiredMixin, SingleTableView):
    model = Checkout
    table_class = CheckoutTable
    template_name = "inventory/checkouts/index.html"


######################### VIEW HELPERS #########################

def getPagination(request, objects, count):
    page = request.POST.get('page', 1)
    paginator = Paginator(objects, count)
    
    try:
        paginationOut = paginator.page(page)
    except PageNotAnInteger:
        paginationOut = paginator.page(1)
    except EmptyPage:
        paginationOut = paginator.page(paginator.num_pages)
    return paginationOut
