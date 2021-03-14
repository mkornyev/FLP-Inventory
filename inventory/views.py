
# IMPORTS 

from django.shortcuts import render
# from django.http import Http404, HttpResponse, HttpResponseRedirect #, JsonResponse
# from django.shortcuts import render, redirect, get_object_or_404
# from django.urls import reverse


# BASIC VIEWS 

def home(request): 
	return render(request, 'inventory/home.html')

def about(request):
	return render(request, 'inventory/about.html')