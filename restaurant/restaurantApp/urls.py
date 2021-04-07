from django.urls import path
from . import views

urlpatterns = [
	path('',views.menu,name="menu"),
	path('home/',views.mainpg,name="home"),
	path('login/',views.login,name="login"),
	path('contact/',views.contact,name="contact"),
	path('registration/',views.registration,name="registration"),
	path('restaurants/',views.restaurants,name="restaurants"),
]