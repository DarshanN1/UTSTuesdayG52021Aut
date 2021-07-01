from django.shortcuts import render, redirect
from django.db.models import Q
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
from .filters import MenuFilter

# Create your views here.
def menu(request):
	menu_items = MenuItem.objects.all()

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		items = []
		order = {'get_cart_items':0, 'get_cart_total':0}
		cartItems = order['get_cart_items']

	itemFilter = MenuFilter(request.GET,queryset=menu_items)
	menu_items = itemFilter.qs

	context = {'menu_items':menu_items,'order':order,'itemFilter':itemFilter}
	return render(request,'restaurantApp/menu.html',context)

def updateItem(request):
	try:
		data = json.loads(request.body)
		itemId = data['itemId']
		action = data['action']
		print('Action:',action)
		print('Item ID:',itemId)

		customer = request.user.customer
		item = MenuItem.objects.get(id=itemId)
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		#if the order already exists, then we do not make a new Order
		#just add/substract from it
		orderItem, created = OrderItem.objects.get_or_create(order=order,menu_item=item)
	
		if action == 'add':
			orderItem.quantity += 1
		elif action == 'remove':
			orderItem.quantity -= 1
		orderItem.save()

		if orderItem.quantity <= 0:
			orderItem.delete()

		return JsonResponse('Item was added',safe=False)

	except json.decoder.JSONDecodeError:
		print("There was a problem accessing the website data.")
	return JsonResponse('Oops...',safe=False)

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
			email = form.cleaned_data.get('email')
			cust_group = Group.objects.get(name='customer')
			user.groups.add(cust_group)
			customer = Customer.create(user,username,email)
			customer.save()
			messages.success(request,'Account was created for ' + username)
			return redirect('login')
	else:
		form = CreateUserForm()
	context = {'form': form}
	return render(request,'restaurantApp/registration.html',context)

@login_required(login_url='login')
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
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False)
		#booking, created = Booking.objects.get_or_create(customer=customer,transaction_id='2348750401')
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items':0, 'get_cart_total':0}
	#remove loop
	for i in range(items.count()):
		print(items[i])
	context = {'items':items, 'order':order}
	return render(request,'restaurantApp/checkout.html',context)

def cart(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,status='Pending',complete=False)
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items':0, 'get_cart_total':0}
	#remove loop
	for i in range(items.count()):
		print(items[i])
	context = {'items':items, 'order':order}
	return render(request,'restaurantApp/cart.html',context)

def test(request):
	context = {}
	return render(request,'restaurantApp/test.html',context)