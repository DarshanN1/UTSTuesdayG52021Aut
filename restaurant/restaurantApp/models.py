from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# null True and blank True are almost the same, except in the case
# of TextField & CharField, which are not saved as NULL but as '' in db
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200,null=True)
	phone = models.CharField(max_length=10,null=True)
	email = models.CharField(max_length=200,null=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return self.name

class Restaurant(models.Model):
	address = models.CharField(max_length=200,null=False)
	city = models.CharField(max_length=50,null=False)
	state = models.CharField(max_length=3,null=False)
	postcode = models.CharField(max_length=4,null=False)
	opening_time = models.IntegerField()
	closing_time = models.IntegerField()

	def __str__(self):
		return self.city

class MenuItem(models.Model):
	CATEGORY = (
		('Entree','Entree'),
		('Salads','Salads'),
		('Main Course','Main Course'),
		('Dessert','Dessert'),
		('Drinks','Drinks'),
	)

	name = models.CharField(max_length=200,null=True)
	price = models.FloatField()
	portion_size = models.CharField(max_length=10,null=True)
	desc = models.CharField(max_length=750,null=True)
	image = models.ImageField(null=True, blank=True)
	#category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.CASCADE)

	def __str__(self):
		return self.name


class Booking(models.Model):
	"""Assuming a customer can make a single booking at a given time"""
	customer = models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True, blank=True)
	restaurant = models.ForeignKey(Restaurant,on_delete=models.SET_NULL,null=True,blank=True)
	dt_booking_created = models.DateTimeField(auto_now_add=True)
	#reservation_date = 
	complete = models.BooleanField(default=False,null=True,blank=False)
	number_of_guests = models.IntegerField()
	special_req = models.CharField(max_length=200,null=True,blank=True)
	transaction_id = models.CharField(max_length=200,null=True)

	def __str__(self):
		return str(self.id)

class Table(models.Model):
	restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	capacity = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(2)])
	#booked at a certain date & time
	#booked = models.BooleanField(default=False,null=True,blank=False)
	
	#table currently selected by a user; lock it for a time period
	#selected = models.BooleanField()

	def __str__(self):
		return str(self.id)


class Category(models.Model):
	name = models.CharField(max_length=200,null=True)
	category_item = models.ForeignKey(MenuItem,null=True,blank=True,on_delete=models.CASCADE)

	def __str__(self):
		return self.name


#create a complete order based on what is already in the cart? i.e. separate class
#or cart itself

class Order(models.Model):
	STATUS = (
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered','Delivered'),
		('Served','Served'),
	)
	customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
	menuitem = models.ForeignKey(MenuItem,null=True,on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=200,null=True,choices=STATUS)
	transaction_id = models.CharField(max_length=100,null=True)

	def __str__(self):
		return str(self.id)

class OrderItem(models.Model):
	order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
	item = models.ForeignKey(MenuItem,null=True,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0,null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.item.price * self.quantity
		return total