from django import forms
from .models import Appointment, Doctor, Patient, CustomUser

class AppointmentForm(forms.ModelForm):
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),  # calendar picker
        input_formats=['%Y-%m-%d']  # HTML5 date input always submits in YYYY-MM-DD
    )
    appointment_time = forms.TimeField(
    widget=forms.TimeInput(attrs={'type': 'time'}),
    input_formats=['%H:%M']  # example: 14:30
)

    class Meta:
        model = Appointment
        fields = ["doctor", "appointment_date", "appointment_time"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["doctor"].queryset = Doctor.objects.filter(approved=True)

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['speciality', 'phone_number']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['city',  'phone_number']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'role']
