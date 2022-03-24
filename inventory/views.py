from re import S
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core import serializers
from django.http import JsonResponse
from django_tables2 import SingleTableView, SingleTableMixin
from django_filters.views import FilterView
from .filters import CheckoutFilter, ItemFilter
from .tables import FamilyTable, CategoryTable, ItemTable, CheckinTable, CheckoutTable

from django.contrib import messages
from django.http import HttpResponse

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import ExtractYear, ExtractMonth
from django.db.models import Count, Q

from inventory.models import Family, Category, Item, Checkin, Checkout, ItemTransaction
from inventory.forms import LoginForm, AddItemForm, CheckOutForm, CreateFamilyForm, CreateItemForm

from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from collections import defaultdict
from io import StringIO
import json
import calendar
import csv

DEFAULT_PAGINATION_SIZE = 25
LOW_QUANTITY_THRESHOLD = 10 # this number or below is considered low quantity

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
        context['tx_type'] = request.POST['tx-type']

        context['totalValue'] = 0 
        for result in context['results']:
            context['totalValue'] = result.getValue() + context['totalValue']

        if 'export' in request.POST:
            qs = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=ItemReport ' + request.POST['start-date'] + " to " + request.POST['end-date'] + '.csv'
            writer = csv.writer(response)
    
            if qs is not None:
                writer.writerow(["item", "new/used", "category", "quantity", "new/used price", "total value"])

                uniqueItems = {} 

                for c in qs:
                    for tx in c.items.all():
                        item_key = (tx.item.id, tx.is_new)
                        try: 
                            originalPrice = tx.item.new_price if tx.is_new else tx.item.used_price
                            adjustedPrice = float(request.POST.get(str(tx.item.id) + '-' + str(tx.is_new) + '-adjustment', originalPrice))
                        except (ValueError, TypeError) as _: # noqa: F841
                            adjustedPrice = 0

                        if item_key not in uniqueItems: 
                            uniqueItems[item_key] = [
                                tx.item.name,
                                "New" if tx.is_new else "Used",
                                "No category" if tx.item.category is None else tx.item.category.name,
                                tx.quantity,
                                adjustedPrice,
                                0 if adjustedPrice is None else round(tx.quantity*adjustedPrice, 2)
                            ]
                        else: 
                            item_key = (tx.item.id, tx.is_new)
                            uniqueItems[item_key][3] += tx.quantity
                            uniqueItems[item_key][5] += 0 if adjustedPrice is None else tx.quantity*adjustedPrice
                            round(uniqueItems[item_key][5], 2)
                
                sorted_items = list(sorted(uniqueItems.values(), key=lambda x: (x[0], x[1])))
                for item in sorted_items:
                    writer.writerow(item)

            return response

        if 'export_drive' in request.POST:
            qs = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=endDatetime).all()
            si = StringIO()
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            writer = csv.writer(si)
    
            if qs is not None:
                writer.writerow(["item", "new/used", "category", "quantity", "new/used price", "total value"])

                uniqueItems = {} 

                for c in qs:
                    for tx in c.items.all():
                        item_key = (tx.item.id, tx.is_new)
                        try: 
                            originalPrice = tx.item.new_price if tx.is_new else tx.item.used_price
                            adjustedPrice = float(request.POST.get(str(tx.item.id) + '-' + str(tx.is_new) + '-adjustment', originalPrice))
                        except (ValueError, TypeError) as _: # noqa: F841
                            adjustedPrice = 0

                        if item_key not in uniqueItems: 
                            uniqueItems[item_key] = [
                                tx.item.name,
                                "New" if tx.is_new else "Used",
                                "No category" if tx.item.category is None else tx.item.category.name,
                                tx.quantity,
                                adjustedPrice,
                                0 if adjustedPrice is None else round(tx.quantity*adjustedPrice, 2)
                            ]
                        else: 
                            item_key = (tx.item.id, tx.is_new)
                            uniqueItems[item_key][3] += tx.quantity
                            uniqueItems[item_key][5] += 0 if adjustedPrice is None else tx.quantity*adjustedPrice
                            round(uniqueItems[item_key][5], 2)
                
                sorted_items = list(sorted(uniqueItems.values(), key=lambda x: (x[0], x[1])))
                for item in sorted_items:
                    writer.writerow(item)

            fileTitle = context['tx_type'] + 'Report By Item ' + request.POST['start-date'] + " to " + request.POST['end-date'] + '.csv'
            csvFile = drive.CreateFile({'title': fileTitle, 'mimeType': 'text/csv'})
            csvFile.SetContentString(si.getvalue().strip('\r\n'))
            csvFile.Upload()
            return render(request, 'inventory/reports/generate_report.html', context)

        if 'itemizedOutput' in request.POST:
            context['itemizedOutput'] = request.POST['itemizedOutput']

            newUniqueItems = {}
            for res in context['results']: 
                for tx in res.items.all(): 
                    item_key = (tx.item.id, tx.is_new)
                    item_price = None
                    if tx.is_new and tx.item.new_price != None:
                        item_price = tx.item.new_price
                    elif not tx.is_new and tx.item.used_price != None:
                        item_price = tx.item.used_price
                    if item_key not in newUniqueItems:
                        newUniqueItems[item_key] = {
                            'id': tx.item.id,
                            'item': tx.item.name,
                            'category': "No category" if tx.item.category is None else tx.item.category.name,
                            'is_new': tx.is_new,
                            'quantity': tx.quantity,
                            'new_price': tx.item.new_price,
                            'used_price': tx.item.used_price,
                            'value': 0 if item_price is None else tx.quantity*item_price,
                            'tx_notes': res.notes_description()
                        }
                    else: 
                        newUniqueItems[item_key]['quantity'] += tx.quantity
                        newUniqueItems[item_key]['value'] += 0 if item_price is None else tx.quantity*item_price

                        currNotes = newUniqueItems[item_key]['tx_notes']
                        if res.notes and currNotes and str(res.id) not in currNotes: 
                            currNotes = currNotes + "<br>" + res.notes_description()
                            newUniqueItems[item_key]['tx_notes'] = currNotes

                        currNotes = newUniqueItems[item_key]['tx_notes']
                        if res.notes and currNotes and str(res.id) not in currNotes: 
                            currNotes = currNotes + "<br>" + res.notes_description()
                            newUniqueItems[item_key]['tx_notes'] = currNotes

            context['results'] = list(sorted(newUniqueItems.values(), key=lambda x: (x['item'], "New" if x['is_new'] else "Used")))

        if 'export_table' not in request.POST \
            and 'export_drive_table' not in request.POST:
            context['results'] = getPagination(request, context['results'], DEFAULT_PAGINATION_SIZE)
            return render(request, 'inventory/reports/generate_report.html', context)

        if 'export_table' in request.POST:
            qs = context['results']
            response = HttpResponse()
            response['Content-Disposition'] = 'attachment; filename=' + context['tx_type'] + 'Report ' + request.POST['start-date'] + " to " + request.POST['end-date'] + '.csv'
            writer = csv.writer(response)

            if 'itemizedOutput' in request.POST:
                if len(context.get('results', [])) != 0:
                    headers = list(context['results'][0].keys())
                    headers = [x for x in headers if x not in ['tx_notes', 'new_price', 'used_price']]
                    headers.append('new/used price')
                    writer.writerow(headers)
                    for i in context['results']:
                        row = []
                        for h in headers:
                            if h == "new/used price":
                                if i['is_new']:
                                    row.append(i['new_price'])
                                else:
                                    row.append(i['used_price'])
                            else:
                                row.append(i[h])
                        writer.writerow(row)
                return response

            if len(qs) != 0:
                field_names = [f.name for f in qs.model._meta.get_fields()] + ["value"]
                writer.writerow(field_names)
                for i in qs:
                    row = []
                    for f in field_names:
                        if f == "items":
                            txs = ', '.join([str(tx) for tx in i.items.all()])
                            row.append(txs)
                        elif f == "value":
                            row.append(i.getValue())
                        else:
                            row.append(getattr(i, f))
                    writer.writerow(row)
            return response

        if 'export_drive_table' in request.POST:
            si = StringIO()
            gauth = GoogleAuth()
            gauth.LocalWebserverAuth()
            drive = GoogleDrive(gauth)
            qs = context['results']
            writer = csv.writer(si)
            fileTitle = ""

            if 'itemizedOutput' in request.POST:  
                fileTitle = context['tx_type'] + 'Report By Item ' + request.POST['start-date'] + " to " + request.POST['end-date'] + '.csv'
                if len(context.get('results', [])) != 0:
                    headers = list(context['results'][0].keys())
                    headers = [x for x in headers if x not in ['tx_notes', 'new_price', 'used_price']]
                    headers.append('new/used price')
                    writer.writerow(headers)
                    for i in context['results']:
                        row = []
                        for h in headers:
                            if h == "new/used price":
                                if i['is_new']:
                                    row.append(i['new_price'])
                                else:
                                    row.append(i['used_price'])
                            else:
                                row.append(i[h])
                        writer.writerow(row)

            if len(qs) != 0 and 'itemizedOutput' not in request.POST:
                fileTitle = context['tx_type'] + 'Report ' + request.POST['start-date'] + " to " + request.POST['end-date'] + '.csv'
                field_names = [f.name for f in qs.model._meta.get_fields()] + ["value"]
                writer.writerow(field_names)
                for i in qs:
                    row = []
                    for f in field_names:
                        if f == "items":
                            txs = ', '.join([str(tx) for tx in i.items.all()])
                            row.append(txs)
                        elif f == "value":
                            row.append(i.getValue())
                        else:
                            row.append(getattr(i, f))
                    writer.writerow(row)
            csvFile = drive.CreateFile({'title': fileTitle, 'mimeType': 'text/csv'})
            csvFile.SetContentString(si.getvalue().strip('\r\n'))
            csvFile.Upload()
            return render(request, 'inventory/reports/generate_report.html', context)

    today = date.today()
    weekAgo = today - timedelta(days=7)
    context['endDate'] = today.strftime('%Y-%m-%d')
    context['startDate'] = weekAgo.strftime('%Y-%m-%d')
    return render(request, 'inventory/reports/generate_report.html', context)

######################### ANALYTICS #########################
@login_required
def analytics(request):
    context = {}

    all_checkouts = Checkout.objects

    ###  Item Checkout Quantities tables
    one_week_ago = date.today() - timedelta(days=7)
    context['one_week_ago'] = one_week_ago
    one_month_ago = date.today() - relativedelta(months=1)
    context['one_month_ago'] = one_month_ago
    six_months_ago = date.today() - relativedelta(months=6)
    context['six_months_ago'] = six_months_ago
    context['all_time'] = 'All Time'

    def item_checkout_quantities(checkout_objects, date_gte, group_by):
        '''
        Generate checkout quantities as tuples of what's being grouped by and 
        quantity for all dates greater than or equal to date_gte (e.g. from one week ago).
        group_by should be either "item" or "category".
        '''
        if group_by not in {'item', 'category'}:
            raise Exception("Invalid group by: must be item or category")
        filtered_checkouts = checkout_objects.filter(datetime__date__gte=date_gte).all()

        # Get checkouts grouped by group_by, sorted by quantity checked out
        checkout_quantities = defaultdict(int)
        for checkout in filtered_checkouts:
            for itemTransaction in checkout.items.all():
                if group_by == 'item':
                    group_by_obj = itemTransaction.item
                else: # category
                    group_by_obj = itemTransaction.item.category

                quantity = itemTransaction.quantity
                checkout_quantities[group_by_obj] += quantity
        
        return checkout_quantities.items()

    item_quant_week = item_checkout_quantities(all_checkouts, one_week_ago, 'item')
    item_quant_month = item_checkout_quantities(all_checkouts, one_month_ago, 'item')
    item_quant_six_months = item_checkout_quantities(all_checkouts, six_months_ago, 'item')
    item_quant_all_time = item_checkout_quantities(all_checkouts, datetime.min, 'item')

    cat_quant_week = item_checkout_quantities(all_checkouts, one_week_ago, 'category')
    cat_quant_month = item_checkout_quantities(all_checkouts, one_month_ago, 'category')
    cat_quant_six_months = item_checkout_quantities(all_checkouts, six_months_ago, 'category')
    cat_quant_all_time = item_checkout_quantities(all_checkouts, datetime.min, 'category')

    ### Sorting columns for checkout quantities tables when pressed

    def new_sort_type():
        '''
        Returns new sort type based on a column, switching the sorting order each time. 
        The default sorting is "desc" for descending.
        '''
        # non_default instead of default b/c we always use "not" on sort_type
        non_default_sorting = "asc"
        sort_type = request.GET.get('sort_type', non_default_sorting)
        # switch sort_type
        new_sort_type = "asc" if sort_type == "desc" else "desc"
        
        return new_sort_type

    context['sort_type'] = new_sort_type()
    sort_reverse = context['sort_type'] == "desc"

    def order_function():
        '''
        Returns function with order field to sort by. Defaulted to 'checkout_quantity'.
        '''
        default_order = 'checkout_quantity'
        order_field = request.GET.get('order_by', default_order)

        order_lambda = lambda i_quantity: i_quantity[1] # default_order is checkout quantity
        if order_field == 'quantity':
            order_lambda = lambda i_quantity: i_quantity[0].quantity
        elif order_field == 'name':
            order_lambda = lambda i_quantity: i_quantity[0].name.lower()
        return order_lambda

    order_by_field = order_function()
    def sort_checkouts_paginated(item_quantities, order_func=order_by_field, sort_rev=sort_reverse):
        '''
        Sort the objects based on an order function and whether to reverse sort it.
        Return a paginated object of the sorted items and quantities.
        '''
        sorted_item_quants = sorted(item_quantities, key=order_func, reverse=sort_rev)
        return getPagination(request, sorted_item_quants, DEFAULT_PAGINATION_SIZE)

    context['item_week_checkouts'] = sort_checkouts_paginated(item_quant_week)
    context['item_month_checkouts'] = sort_checkouts_paginated(item_quant_month)
    context['item_six_month_checkouts'] = sort_checkouts_paginated(item_quant_six_months)
    context['item_all_time_checkouts'] = sort_checkouts_paginated(item_quant_all_time)

    context['cat_week_checkouts'] = sort_checkouts_paginated(cat_quant_week)
    context['cat_month_checkouts'] = sort_checkouts_paginated(cat_quant_month)
    context['cat_six_month_checkouts'] = sort_checkouts_paginated(cat_quant_six_months)
    context['cat_all_time_checkouts'] = sort_checkouts_paginated(cat_quant_all_time)

    context['LOW_QUANTITY_THRESHOLD'] = LOW_QUANTITY_THRESHOLD

    ###  Data for charts
    def chart_info_by_month(objects, count_field):
        '''
        Returns a tuple of chart's labels and data both as json-lists based on the objects grouped by year/month. 
        A label is a year + month as a string and data is an integer value for how many occurred in that month.
        count_field is the field in Checkout to count for each month.
        '''
        by_month = objects.annotate(   
            month=ExtractMonth('datetime'),
            year=ExtractYear('datetime') 
        ).values('year', 'month').annotate(
            count=Count(count_field, distinct=True)
        ).order_by('year', 'month')

        # Note: technically if a month has no checkouts, it will not show up as 0, 
        # but instead be omitted, but hoping that's not something that might happen for now
        labels_by_month, data_by_month = [], []
        for month_count in by_month:
            month = calendar.month_name[month_count['month']]
            labels_by_month.append(month + ' ' + str(month_count['year']))
            data_by_month.append(month_count['count'])
        
        return (json.dumps(labels_by_month), json.dumps(data_by_month))

    context['labels_couts'], context['data_couts'] = chart_info_by_month(all_checkouts, 'id')
    context['labels_fams'], context['data_fams'] = chart_info_by_month(all_checkouts, 'family')

    return render(request, 'inventory/analytics/analytics.html', context)

  
###################### CHECKIN/CHECKOUT VIEWS ######################
# Remove item from cart
def removeitem_action(request, index, location):
    saved_list = request.session['transactions-' + location]

    saved_list.pop(index)
    request.session['transactions-' + location] = saved_list

    return redirect(reverse('Check' + location))


def editquantity_action(request, index, location, qty):
    saved_list = request.session['transactions-' + location]
    curr_item = json.loads(saved_list[index])
    curr_item[0]['fields']['quantity'] = qty
    
    saved_list[index] = json.dumps(curr_item)
    request.session['transactions-' + location] = saved_list

    return redirect(reverse('Check' + location))  

def editisnew_action(request, index, location, isnew):
    saved_list = request.session['transactions-' + location]
    curr_item = json.loads(saved_list[index])
    if (isnew == 1):
        curr_item[0]['fields']['is_new'] = True
    else:
        curr_item[0]['fields']['is_new'] = False

    saved_list[index] = json.dumps(curr_item)
    request.session['transactions-' + location] = saved_list

    return redirect(reverse('Check' + location))  

# Create Family View 
@login_required
def createFamily_action(request, location):
    context = {}

    context['location'] = location

    if request.method == 'GET':
        context['form'] = CreateFamilyForm()
        
        return render(request, 'inventory/families/create.html', context)

    if request.method == 'POST':
        form = CreateFamilyForm(request.POST)

        context['form'] = form

        if not form.is_valid():
            return render(request, 'inventory/families/create.html', context)

        # category = form.cleaned_data['category']
        fname = form.cleaned_data['first_name']
        lname = form.cleaned_data['last_name']
        phone = form.cleaned_data['phone']

        family = Family(fname=fname, lname=lname, phone=phone)
        family.save()

        request.session['createdFamily'] = family.displayName
        messages.success(request, 'Family created')

        return redirect(reverse(location))

# Create Item View
@user_passes_test(lambda u: u.is_superuser)
def createItem_action(request, location):
    context = {}

    context['location'] = location

    if request.method == 'GET':
        context['form'] = CreateItemForm()
        
        return render(request, 'inventory/items/create.html', context)

    if request.method == 'POST':
        form = CreateItemForm(request.POST)

        context['form'] = form

        if not form.is_valid():
            return render(request, 'inventory/items/create.html', context)

        category = form.cleaned_data['category']
        name = form.cleaned_data['name']
        new_price = form.cleaned_data['new_price']
        used_price = form.cleaned_data['used_price']
        quantity = form.cleaned_data['quantity']

        item = Item(category=category, name=name, new_price=new_price, used_price=used_price, quantity=quantity)
        item.save()

        if location == 'in' or location == 'out':
            request.session["itemInfo"] = (item.name, item.quantity)
            messages.success(request, 'Item created')
            return redirect(reverse('Check' + location))
        else:
            return redirect(reverse(location))

# Checkin view
@login_required
def checkin_action(request):
    context = {}
        
    context['items'] = Item.objects.all()
    context['categories'] = Category.objects.all()

    # Create transactions if they don't exist
    if not 'transactions-in' in request.session or not request.session['transactions-in']:
        request.session['transactions-in'] = []

    # Deserialize transactions 
    serialized_transactions = request.session['transactions-in']
    transactions = []
    for tx in serialized_transactions:
        for deserialized_transaction in serializers.deserialize("json", tx):
            transactions.append(deserialized_transaction.object)

    context['transactions'] = transactions

    if request.method == 'GET':
        addItemForm = AddItemForm()
        if ('itemInfo' in request.session):
            itemInfo = request.session['itemInfo']
            addItemForm.fields['item'].initial = itemInfo[0]
            addItemForm.fields['quantity'].initial = itemInfo[1]
            del request.session['itemInfo']

        context['formadditem'] = addItemForm
        return render(request, 'inventory/checkin.html', context)

    if request.method == 'POST' and 'additem' in request.POST:
        form = AddItemForm(request.POST)

        context['formadditem'] = form

        if not form.is_valid():
            return render(request, 'inventory/checkin.html', context)

        # category = form.cleaned_data['category']
        name = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']
        is_new = form.cleaned_data['is_new']

        item = Item.objects.filter(name=name).first()
    
        tx = serializers.serialize("json", [ ItemTransaction(item=item, quantity=quantity, is_new=is_new), ])
        if not 'transactions-in' in request.session or not request.session['transactions-in']:
            saved_list = []
        else:
            saved_list = request.session['transactions-in']

        saved_list.append(tx)
        request.session['transactions-in'] = saved_list

        return redirect(reverse('Checkin'))

    if request.method == 'POST' and 'checkin' in request.POST:
        if not transactions:
            messages.warning(request, 'Could not create checkin: No items added')
            return render(request, 'inventory/checkin.html', context, status=400)

        if 'checkin_notes' in request.POST and len(request.POST['checkin_notes']) > 0: 
            checkin = Checkin(user=request.user, notes=request.POST['checkin_notes'])
        else: 
            checkin = Checkin(user=request.user)
        checkin.save()

        for tx in transactions:
            tx.save()

            checkin.items.add(tx)

            tx.item.quantity += tx.quantity
            tx.item.save()

        del request.session['transactions-in']
        request.session.modified = True

        messages.success(request, 'Checkin created.')
        return redirect(reverse('Checkin'))

# Checkout view
@login_required
def checkout_action(request):
    context = {}
        
    context['items'] = Item.objects.all()
    context['categories'] = Category.objects.all()
    context['createdFamily'] = 'no family'

    # Create transactions if they don't exist
    if not 'transactions-out' in request.session or not request.session['transactions-out']:
        request.session['transactions-out'] = []

    # Deserialize transactions 
    serialized_transactions = request.session['transactions-out']
    transactions = []
    for tx in serialized_transactions:
        for deserialized_transaction in serializers.deserialize("json", tx):
            transactions.append(deserialized_transaction.object)

    context['transactions'] = transactions

    if request.method == 'GET':
        addItemForm = AddItemForm()
        context['formadditem'] = addItemForm
        form = CheckOutForm()
        context['formcheckout'] = form

        if ('createdFamily' in request.session):
            famName = request.session['createdFamily']
            form.fields['family'].initial = famName
            context['createdFamily'] = famName
            del request.session['createdFamily']

        if ('itemInfo' in request.session):
            itemInfo = request.session['itemInfo']
            addItemForm.fields['item'].initial = itemInfo[0]
            addItemForm.fields['quantity'].initial = itemInfo[1]
            del request.session['itemInfo']

        return render(request, 'inventory/checkout.html', context)

    if request.method == 'POST' and 'additem' in request.POST:
        form = AddItemForm(request.POST)

        context['formadditem'] = form
        context['formcheckout'] = CheckOutForm()

        if not form.is_valid():
            return render(request, 'inventory/checkout.html', context)

        # category = form.cleaned_data['category']
        name = form.cleaned_data['item']
        quantity = form.cleaned_data['quantity']
        is_new = form.cleaned_data['is_new']

        item = Item.objects.filter(name=name).first()
    
        tx = serializers.serialize("json", [ ItemTransaction(item=item, quantity=quantity, is_new=is_new, ), ])
        if not 'transactions-out' in request.session or not request.session['transactions-out']:
            saved_list = []
        else:
            saved_list = request.session['transactions-out']

        saved_list.append(tx)
        request.session['transactions-out'] = saved_list

        return redirect(reverse('Checkout'))

    if request.method == 'POST' and 'checkout' in request.POST:
        form = CheckOutForm(request.POST)

        context['formcheckout'] = form
        context['formadditem'] = AddItemForm()

        if not form.is_valid():
            return render(request, 'inventory/checkout.html', context, status=400)

        family = form.cleaned_data['family'].strip()
        childName = form.cleaned_data['child'].strip()
        ageRange = form.cleaned_data['age']

        family_object = Family.objects.filter(displayName__exact=family)

        if not transactions:
            messages.warning(request, 'Could not create checkout: No items added')
            return render(request, 'inventory/checkout.html', context, status=400)

        notes = None
        if 'checkout_notes' in request.POST and request.POST['checkout_notes'] != '': 
            notes = request.POST['checkout_notes']
        
        checkout = Checkout(family=family_object[0], user=request.user, notes=notes, childName=childName, ageRange=ageRange)
        checkout.save()

        for tx in transactions:
            tx.save()

            checkout.items.add(tx)

            tx.item.quantity -= tx.quantity
            tx.item.save()

        del request.session['transactions-out']
        request.session.modified = True

        messages.success(request, 'Checkout created.')
        return redirect(reverse('Checkout'))
  
def autocomplete_item(request):
    if 'term' in request.GET:
        qs = Item.objects.filter(name__icontains=request.GET.get('term'))
        names = list()
        for item in qs:
            names.append(item.name)
        return JsonResponse(names, safe=False)
  
def autocomplete_family(request):
    if 'term' in request.GET:
        qs = Family.objects.filter(Q(displayName__icontains=request.GET.get('term')) )
        names = list()
        for fam in qs: 
            names.append(fam.displayName)
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

class ItemIndexView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Item
    table_class = ItemTable
    template_name = "inventory/items/index.html"
    filterset_class = ItemFilter

class CheckinIndexView(LoginRequiredMixin, SingleTableView):
    model = Checkin
    table_class = CheckinTable
    template_name = "inventory/checkins/index.html"

class CheckoutIndexView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Checkout
    table_class = CheckoutTable
    template_name = "inventory/checkouts/index.html"
    filterset_class = CheckoutFilter


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
