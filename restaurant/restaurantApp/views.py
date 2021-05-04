from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import json
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .decorators import unauthenticated_user,allowed_user,admin_only

# Create your views here.
def menu(request):
	menu_items = MenuItem.objects.all()
	context = {'menu_items':menu_items}
	return render(request,'restaurantApp/menu.html',context)

def updateItem(request):
	data = json.loads(request.body)
	itemId = data['itemId']
	action = data['action']
	print('Action:',action)
	print('Item ID:',itemId)

	customer = request.user.customer
	item = MenuItem.objects.get(id=itemId)
	order, created = Order.objects.get_or_create(customer=customer,status='Pending')
	#if the order already exists, then we do not make a new Order
	#just add/substract from it
	orderItem, created = OrderItem.objects.get_or_create(order=order,item=item)
	
	if action == 'add':
		orderItem.quantity += 1
	elif action == 'remove':
		orderItem.quantity -= 1
	orderItem.save()

	if orderItem.quantity <= 0:
		OrderItem.delete()

	return JsonResponse('Item was added',safe=False)

def dashboard_admin(request):
	#menu_items = MenuItem.objects.all()
	orders = Order.objects.all()
	customers = Customer.objects.all()

	total_customers = customers.count()
	total_orders = orders.count()
	served = orders.filter(status='Served').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders,'customers':customers,'total_orders':total_orders,'total_customers':total_customers,'served':served,'pending':pending}
	return render(request,'restaurantApp/dashboard-admin.html',context)


def mainpg(request):
	context = {}
	return render(request,'restaurantApp/mainpg.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def mainpgLog(request):
	context = {}
	return render(request,'restaurantApp/mainpgLog.html',context)

@unauthenticated_user
def loginPage(request):
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

@unauthenticated_user
def registration(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		# if entered data is valid
		if form.is_valid():
			# form based on User model, saving will create a new User
			user = form.save()
			username = form.cleaned_data.get('username')
			group = Group.objects.get(name='customer')
			user.groups.add(group)
			messages.success(request,'Account was created for ' + username)
			return redirect('login')
	else:
		form = CreateUserForm()
	context = {'form': form}
	return render(request,'restaurantApp/registration.html',context)

def booking(request):
	context = {}
	return render(request,'restaurantApp/booking.html',context)

def account(request):
	return render(request,'restaurantApp/account.html')


def restaurants(request):
	context = {}
	return render(request,'restaurantApp/restaurants.html',context)

def contact(request):
	context = {}
	return render(request,'restaurantApp/contact.html',context)

def checkout(request):
	context = {}
	return render(request,'restaurantApp/checkout.html',context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,status='Pending')
		items = order.menu_item.all()
	else:
		items = []
	#remove loop
	for i in range(items.count()):
		print(items[i])
	context = {'items':items}
	return render(request,'restaurantApp/cart.html',context)

def test(request):
	context = {}
	return render(request,'restaurantApp/test.html',context)