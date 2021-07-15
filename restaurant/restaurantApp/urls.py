from django.urls import path
from . import views

urlpatterns = [
	path('menu/',views.menu,name="menu"),
	path('viewMenu/',views.viewMenu,name="viewMenu"),
	path('',views.mainpg,name="home"),
	path('update_item/',views.updateItem,name="update_item"),
	path('loggedUser/',views.mainpgLog,name="loggedUser"),
	path('dashboard-admin/',views.dashboard_admin,name="dashboard-admin"),
	path('login/',views.loginPage,name="login"),
	path('logout/',views.logoutUser,name="logout"),
	path('contact/',views.contact,name="contact"),
	path('registration/',views.registration,name="registration"),
	path('booking/',views.booking,name="booking"),
	path('account/',views.account,name='account'),
	path('restaurants/',views.restaurants,name="restaurants"),
	path('cart/',views.cart,name="cart"),
	path('checkout/',views.checkout,name="checkout"),
	path('test/',views.test,name="test"),
]