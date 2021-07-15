from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from datetime import date

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

	@classmethod
	def create(cls,user,name,email):
		customer = cls(user=user,name=name,phone='',email=email)
		return customer

class StaffMember(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	first_name = models.CharField(max_length=15)
	last_name = models.CharField(max_length=15)
	#staffId
	phone = models.CharField(max_length=10)
	email = models.CharField(max_length=100)

	def __str__(self):
		return (self.last_name.upper() + ", " + self.first_name)

	def save(self, *args, **kwargs):
		if self.user.is_staff:
			self.email = self.user.email
			super(StaffMember, self).save(*args,**kwargs)


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
	name = models.CharField(max_length=100,null=True,blank=True)
	phone = models.CharField(max_length=10,null=True)
	date_created = models.DateField(auto_now_add=True)
	booking_date = models.DateField(null=True,blank=True)
	booking_time = models.TimeField(null=True,blank=True)
	complete = models.BooleanField(default=False,null=True,blank=False)
	number_of_guests = models.IntegerField(default=1,
        validators=[
            MaxValueValidator(20),
            MinValueValidator(1)
        ]
	)

	booking_ref = models.CharField(max_length=15,null=True,blank=True)

	def __str__(self):
		return (self.customer.name + " (" + str(self.id) + ")")

	@classmethod
	def create(cls,customer,name,phone,given_date,given_time,guests,transaction_id):
		booking = cls(customer=customer,name=name,phone=phone,booking_date=given_date,booking_time=given_time,complete=False,number_of_guests=guests,booking_ref=transaction_id)
		return booking

	@property
	def booking_complete(self):
		if self.booking_date > date.today():
			complete = True

	@property
	def booking_event(self):
		if self.booking_time.strftime("%H") < "12":
			return 'Breakfast'
		elif self.booking_time.strftime("%H") < "17":
			return 'Lunch'
		return 'Dinner'

class Table(models.Model):
	restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE)
	capacity = models.IntegerField(validators=[MaxValueValidator(10),MinValueValidator(2)])

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
	id = models.AutoField(primary_key=True)
	STATUS = (
		('Pending','Pending'),
		('Out for delivery','Out for delivery'),
		('Delivered','Delivered'),
		('Served','Served'),
		('Ready for Pickup','Ready for Pickup'),
	)
	customer = models.ForeignKey(Customer,null=True,on_delete=models.CASCADE)
	booking = models.OneToOneField(Booking, on_delete=models.CASCADE, null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False,null=True,blank=False)
	status = models.CharField(max_length=200,null=True,choices=STATUS)

	def __str__(self):
		return str(self.id)

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total

	

class OrderItem(models.Model):
	order = models.ForeignKey(Order,null=True,on_delete=models.CASCADE)
	menu_item = models.ForeignKey(MenuItem,null=True,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=0,null=True,blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.menu_item.price * self.quantity
		return total