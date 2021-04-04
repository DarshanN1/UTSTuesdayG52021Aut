from django.shortcuts import render
from .models import *

# Create your views here.
def menu(request):
	menu_items = MenuItem.objects.all()
	context = {'menu_items':menu_items}
	return render(request,'restaurantApp/menu.html',context)