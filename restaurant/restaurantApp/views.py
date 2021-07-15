from django.shortcuts import render, redirect
from django.db.models import Q
from .models import *
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from .forms import BookingForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models.functions import Concat
from django.contrib import messages
from .decorators import unauthenticated_user,allowed_user,admin_only
from .filters import MenuFilter
import uuid
from datetime import date

# Create your views here.
def menu(request):
	menu_items = MenuItem.objects.all()

	#only create an order if 1) user is authenticated 2) has a booking
	if request.user.is_authenticated:
		customer = request.user.customer

		all_bookings = list(Booking.objects.filter(customer=customer))
		current_bookings = list(filter(lambda booking: (booking.booking_date > date.today()), all_bookings))

		if len(current_bookings) == 1:
			order, created = Order.objects.get_or_create(customer=customer,booking=current_bookings[0],complete=False,status='Pending')
			items = order.orderitem_set.all()
			cartItems = order.get_cart_items
		else:
			print("You need to make a booking first. An order can be made subsequently.")
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
		order, created = Order.objects.get_or_create(customer=customer,complete=False,status='Pending')
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

@allowed_user(allowed_roles=['admin','Staff'])
def dashboard_admin(request):
	#menu_items = MenuItem.objects.all()
	orders = Order.objects.all()
	customers = Customer.objects.all()

	staff_member = StaffMember.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	served = orders.filter(status='Served').count()
	pending = orders.filter(status='Pending').count()

	context = {'orders':orders,'customers':customers,'staff_member':staff_member,'total_orders':total_orders,'total_customers':total_customers,'served':served,'pending':pending}
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
			return redirect('home')
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

def addStaff(request):
	form = StaffForm()
	if request.method == 'POST':
		staff_reg_form = StaffForm(request.POST)
		staff_name = form.cleaned_data.get('first_name')
		if form.is_valid():
			staff_member = form.save()
			messages.success(request,'New staff account created for ' + staff_name)
			return redirect('dashboard-admin')

@login_required(login_url='login')
def booking(request):
	booking_form = BookingForm()
	if request.method == 'POST':
		booking_form = BookingForm(request.POST)
		if booking_form.is_valid():
			customer = request.user.customer
			name = booking_form.cleaned_data.get('name')
			phone = booking_form.cleaned_data.get('phone')
			booking_date = booking_form.cleaned_data.get('booking_date')
			booking_time = booking_form.cleaned_data.get('booking_time')
			number_of_guests = booking_form.cleaned_data.get('number_of_guests')

			bdate = str(booking_date)
			btime = booking_time.strftime('%H:%M')
			bdate = bdate.replace('-','')
			btime = btime.replace(':','')
			num_guests = str(number_of_guests)
			initials = ''.join([x[0] for x in name.split()])
			initials = initials.upper()
			transaction_id = initials + bdate + btime + num_guests

			prev_bookings = Booking.objects.filter(customer=customer, booking_date__range=["2021-01-01", date.today()])
			all_bookings = Booking.objects.filter(customer=customer)
			#if no new bookings exist, only then can a user make a booking
			if(all_bookings.count() - prev_bookings.count() == 0):
				booking = Booking.create(customer,name,phone,booking_date,booking_time,number_of_guests,transaction_id)
				booking.save()
				return redirect('menu')
			else:
				messages.warning(request,'A booking already exists under your account. Please try again another time.')
	context = {'booking_form':booking_form}	 
	return render(request,'restaurantApp/booking.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def account(request):
	customer = request.user.customer
	all_bookings = list(Booking.objects.filter(customer=customer))
	prev_bookings = list(filter(lambda booking: (booking.booking_date < date.today()), all_bookings))
	next_booking = list(filter(lambda booking: (booking not in prev_bookings), all_bookings))

	context = {'prev_bookings':prev_bookings,'next_booking':next_booking}
	return render(request,'restaurantApp/account.html',context)


def restaurants(request):
	context = {}
	return render(request,'restaurantApp/restaurants.html',context)

def contact(request):
	context = {}
	return render(request,'restaurantApp/contact.html',context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer,complete=False,status='Pending')
		booking = Booking.objects.get(customer=customer,date_created=date.today())
		items = order.orderitem_set.all()
	else:
		items = []
		order = {'get_cart_items':0, 'get_cart_total':0}
	#remove loop
	for i in range(items.count()):
		print(items[i])
	context = {'items':items, 'order':order, 'booking':booking}
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

def viewMenu(request):
	menu_items = MenuItem.objects.all()
	itemFilter = MenuFilter(request.GET,queryset=menu_items)
	menu_items = itemFilter.qs

	context = {'menu_items' : menu_items, 'itemFilter':itemFilter}
	return render(request,'restaurantApp/viewMenu.html',context)