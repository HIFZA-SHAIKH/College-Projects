from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from .models import Court, CourtBooking
from django.forms.widgets import DateInput, TimeInput



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'role', 'password1', 'password2']

class CourtForm(forms.ModelForm):
    class Meta:
        model = Court
        fields = ['name', 'location', 'is_available']

class CourtBookingForm(forms.ModelForm):
    class Meta:
        model = CourtBooking
        fields = ['court', 'booking_date', 'start_time', 'end_time']
        widgets = {
            'booking_date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }


