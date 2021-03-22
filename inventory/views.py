from django.shortcuts import render, redirect
from django.urls import reverse
# from django.http import HttpResponse

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from inventory.forms import LoginForm, RegistrationForm
from inventory.models import Checkin, Checkout

from datetime import date, timedelta

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


######################### OTHER ACTIONS #########################

def generate_report(request):
    context = {}

    if 'start-date' in request.POST \
        and 'end-date' in request.POST \
        and 'tx-type' in request.POST \
        and (request.POST['tx-type'] in ['Checkin', 'Checkout']):

        context['endDate'] = request.POST['end-date']
        context['startDate'] = request.POST['start-date']
        context['tx'] = request.POST['tx-type']

        if request.POST['tx-type'] == 'Checkin':
            context['results'] = Checkin.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=context['endDate']).all()
        else:
            context['results'] = Checkout.objects.filter(datetime__gte=context['startDate']).filter(datetime__lte=context['endDate']).all()

        context['results'] = getPagination(request, context['results'], DEFAULT_PAGINATION_SIZE)

        return render(request, 'inventory/generate_report.html', context)

    today = date.today()
    weekAgo = today - timedelta(days=7)
    context['endDate'] = today.strftime('%Y-%m-%d')
    context['startDate'] = weekAgo.strftime('%Y-%m-%d')
    return render(request, 'inventory/generate_report.html', context)


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