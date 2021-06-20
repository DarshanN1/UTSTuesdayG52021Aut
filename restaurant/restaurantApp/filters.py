import django_filters
from .models import *

class MenuFilter(django_filters.FilterSet):
	class Meta:
		model = MenuItem
		fields = '__all__'
		exclude = ['image','price','portion_size','desc']