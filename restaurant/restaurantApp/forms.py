from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from datetimepicker.widgets import DateTimePicker
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class BookingForm(forms.Form):
    class Meta:
        date_time = forms.DateTimeField(widget=DateTimePicker())