from django.urls import path
from . import views

urlpatterns = [
	path('menu/',views.menu,name="menu"),
	path('',views.mainpg,name="home"),
	path('loggedUser/',views.mainpgLog,name="loggedUser"),
	path('login/',views.loginPage,name="login"),
	path('logout/',views.logoutUser,name="logout"),
	path('contact/',views.contact,name="contact"),
	path('registration/',views.registration,name="registration"),
	path('booking/',views.booking,name="booking"),
	path('account/',views.account,name='account'),
	path('restaurants/',views.restaurants,name="restaurants"),
	path('test/',views.test,name="test"),
]