from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import StaffMember
from .models import Booking
from django.contrib.auth.forms import UserCreationForm
from datetimepicker.widgets import DateTimePicker
from django import forms

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class StaffForm(ModelForm):
    phone = forms.CharField(max_length=10,min_length=10)
    class Meta:
        model = StaffMember
        fields = ['first_name','last_name','phone','email']

class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'

class BookingForm(ModelForm):
    phone = forms.CharField(max_length=10,min_length=10)
    name = forms.CharField(max_length=100)
    class Meta:
        model = Booking
        fields = ['booking_date','booking_time','number_of_guests','name','phone']
        widgets = {'booking_date':DateInput(),'booking_time':TimeInput()}

    def __init__(self, *args, **kwargs):
        super(BookingForm,self).__init__(*args, **kwargs)
        self.fields['number_of_guests'].widget.attrs.update({'min': 1, 'max':20})