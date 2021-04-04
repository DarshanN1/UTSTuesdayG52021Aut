from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=200,null=True)
	email = models.CharField(max_length=200,null=True)

	def __str__(self):
		return self.name

class MenuItem(models.Model):
	name = models.CharField(max_length=200,null=True)
	price = models.FloatField()
	desc = models.CharField(max_length=750,null=True)
	image = models.ImageField(null=True, blank=True)
	#menu_category (FK)
	#portion_size 
	#ingredients

	def __str__(self):
		return self.name
""""
	@property
	def imageURL(self):
		try:
			self.image.url
		except:
			url = ''
		return url
"""

#class Order(models.Model):
#class MenuCategory(models.Model):
#class OrderSummary(models.Model):
