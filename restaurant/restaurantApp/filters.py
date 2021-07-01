import django_filters
from django_filters import CharFilter
from django import forms
from .models import *

class MenuFilter(django_filters.FilterSet):
	name = CharFilter(field_name="name",lookup_expr="icontains",required=False,label=False)
	
	class Meta:
		model = MenuItem
		fields = ['name']

	"""def custom_search_filter(self,queryset,name,value):
		return queryset.filter(**{
			name__icontains=value
		})"""