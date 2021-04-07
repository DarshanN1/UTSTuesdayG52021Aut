from django.shortcuts import render
from .models import *

# Create your views here.
def menu(request):
	menu_items = MenuItem.objects.all()
	context = {'menu_items':menu_items}
	return render(request,'restaurantApp/menu.html',context)

def mainpg(request):
	context = {}
	return render(request,'restaurantApp/mainpg.html',context)

def login(request):
	context = {}
	return render(request,'restaurantApp/login.html',context)

def registration(request):
	context = {}
	return render(request,'restaurantApp/registration.html',context)

def restaurants(request):
	context = {}
	return render(request,'restaurantApp/restaurants.html',context)

def contact(request):
	context = {}
	return render(request,'restaurantApp/contact.html',context)