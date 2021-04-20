from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def menu(request):
	menu_items = MenuItem.objects.all()
	context = {'menu_items':menu_items}
	return render(request,'restaurantApp/menu.html',context)


def mainpg(request):
	context = {}
	return render(request,'restaurantApp/mainpg.html',context)

@login_required(login_url='login')
def mainpgLog(request):
	context = {}
	return render(request,'restaurantApp/mainpgLog.html',context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('loggedUser')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')
			#ensure the user can be authenticated to registered details
			user = authenticate(request,username=username,password=password)

			#if authenticated
			if user is not None:
				login(request,user)
				return redirect('loggedUser')
			else:
				messages.info(request,'Username or password is incorrect.')
		
		context = {}
		return render(request,'restaurantApp/login.html',context)

def logoutUser(request):
	logout(request)
	return redirect('login')

def registration(request):
	if request.user.is_authenticated:
		return redirect('loggedUser')
	else:
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			# if entered data is valid
			if form.is_valid():
				# form based on User model, saving will create a new User
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request,'Account was created for ' + user)
				return redirect('login')
		else:
			form = CreateUserForm()
		context = {'form': form}
		return render(request,'restaurantApp/registration.html',context)

def account(request):
	return render(request,'restaurantApp/account.html')


def restaurants(request):
	context = {}
	return render(request,'restaurantApp/restaurants.html',context)

def contact(request):
	context = {}
	return render(request,'restaurantApp/contact.html',context)

def test(request):
	context = {}
	return render(request,'restaurantApp/test.html',context)