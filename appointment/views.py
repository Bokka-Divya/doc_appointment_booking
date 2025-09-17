from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login

from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from datetime import date
from django.http import HttpResponse
from django.utils import timezone

from django.contrib.auth import get_user_model
from .models import Appointment, Patient, Doctor
from .forms import UserForm, PatientForm, DoctorForm, AppointmentForm



# Home page with auto-delete of past appointments

def home(request):
    
    return render(request, 'index.html')

#@login_required
def home_page(request):
    return redirect('home')


# Patient dashboard
@login_required
def patient_page(request):
    if request.user.role!='patient':
        messages.info(request,"you have no permissions to this page")
        return redirect('home-page')
    return render(request, 'patient_page.html')
@login_required
def doctor_page(request):
    if request.user.role!='doctor':
        messages.info(request,"you have no permissions to this page")
        return redirect('home-page')
    return render(request,'doctor_page.html')
def contact_page(request):
    return render(request,'contact_page.html')


# Book appointment
#@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            patient = Patient.objects.get(user=request.user)
            appointment.patient = patient
            existing=Appointment.objects.filter(doctor=appointment.doctor, appointment_date=appointment.appointment_date,appointment_time=appointment.appointment_time).exists()
            if existing:
                messages.info(request,"Sorry this slot is already booked,Please book another slot")
                return redirect("patient-page")
            else:
                appointment.save()
                messages.success(request, "Your appointment has been submitted. You will get confirmation via email.")
            return redirect("patient-page")
    else:
        form = AppointmentForm()
    return render(request, "appointment_form.html", {"form": form})


# View my appointments
@login_required
def my_appointments(request):
    today=timezone.now().date()
    Appointment.objects.filter(date__lt=today).delete()
    #Appointment.objects.filter(user=request.user).order_by("appointment_date")
    if request.user.role == "patient":
        patient = get_object_or_404(Patient, user=request.user)
        
        Appointment.objects.filter(patient__user=request.user,appointment_date__lt=today).delete()

        approved_appointments = Appointment.objects.filter(patient=patient, approved=True).order_by("appointment_date")
        unapproved_appointments = Appointment.objects.filter(patient=patient, approved=False).order_by("appointment_date")
        return render(request, "my_appointments.html", {
            "approved_appointments": approved_appointments,
            "unapproved_appointments": unapproved_appointments
        })

    elif request.user.role == "doctor":
        doctor = get_object_or_404(Doctor, user=request.user)

        Appointment.objects.filter(doctor__user=request.user,appointment_date__lt=today).delete()

        approved_appointments = Appointment.objects.filter(doctor=doctor, approved=True).order_by("appointment_date")
        unapproved_appointments = Appointment.objects.filter(doctor=doctor, approved=False).order_by("appointment_date")
        return render(request, "doctor_appointments.html", {
            "approved_appointments": approved_appointments,
            "unapproved_appointments": unapproved_appointments
        })
    else:
        messages.warning(request, "You don't have permission to view appointments.")
        return redirect("home-page")


# Delete appointment
@login_required
def delete_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    if request.user.role == 'patient':
        patient = get_object_or_404(Patient, user=request.user)
        if appointment.patient != patient:
            messages.error(request, "You are not authorized to delete this appointment.")
            return redirect("home-page")

    elif request.user.role == 'doctor':
        doctor = get_object_or_404(Doctor, user=request.user)
        if appointment.doctor != doctor:
            messages.error(request, "You are not authorized to delete this appointment.")
            return redirect("home-page")
    else:
        messages.error(request, "You don't have permission to delete this appointment.")
        return redirect("home-page")

    if request.method == "POST":
        appointment.delete()
        return redirect('my-appointments')

    return render(request, "appointment_delete.html", {"appointment": appointment})


# Admin-only doctor approval views
def is_admin(user):
    return user.is_superuser or user.is_staff


@user_passes_test(is_admin)
def pending_doctors(request):
    doctors = Doctor.objects.filter(approved=False)
    return render(request, 'admin/pending_doctors.html', {'doctors': doctors})


@user_passes_test(is_admin)
def approve_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    doctor.approved = True
    doctor.save()
    messages.success(request, f"Doctor {doctor.user.username} approved successfully.")
    return redirect('pending-doctors')


@user_passes_test(is_admin)
def reject_doctor(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id)
    user = doctor.user
    doctor.delete()
    user.delete()
    messages.warning(request, "Doctor application rejected and deleted.")
    return redirect('pending-doctors')


# Doctor approves appointment
@login_required
def approve_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor=doctor)

    if not appointment.approved:
        appointment.approved = True
        appointment.save()

        subject = 'Appointment Booked'
        message = f"""
        Hi {appointment.patient.user.username},
        Your appointment with Dr. {doctor.user.username} on {appointment.appointment_date} at {appointment.appointment_time} has been approved.
        """
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [appointment.patient.user.email]
        send_mail(subject, message, from_email, recipient_list)
        messages.info(request,"Appointment approved and email sent.")
    return redirect('my-appointments')


# Custom registration view
def approved_doctors(request):
    doctors = Doctor.objects.filter(approved=True)
    return render(request, 'admin/approved_doctors.html', {'doctors': doctors})
def delete_approved_doctor(request, id):
    doctor = get_object_or_404(Doctor,id=id)
    if doctor.user:
        doctor.user.delete()
        doctor.delete()
    return redirect('approved_doctors')

# Custom login view
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")

            if user.is_superuser or user.is_staff:
                return redirect('pending-doctors')
            elif user.role == "doctor":
                doctor = get_object_or_404(Doctor,user=user)
                if doctor.approved:
                    return redirect('my-appointments')
                else:
                    messages.warning(request, "Your doctor account is pending approval.")
                    return redirect('home')
            elif user.role == "patient":
                return redirect('patient-page')
            else:
                return redirect('home-page')
        else:
            messages.error(request, "Invalid credentials")
    '''else:
        messages.error(request,"invalid credentials")'''
    return render(request, 'login.html')



def doctor_form_view(request, user_id):
    doctor,created = Doctor.objects.get_or_create(user__id=user_id)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            return redirect('user-login')  # Now go to login
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'doctor_form.html', {'form': form})


def patient_form_view(request, user_id):
    patient = get_object_or_404(Patient, user__id=user_id)

    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('user-login')  # Now go to login
    else:
        form = PatientForm(instance=patient)
    
    return render(request, 'patient_form.html', {'form': form})
def user_logout(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect('user-login')
@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin/dashboard.html')


def register_view(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email=form.cleaned_data.get('email')
            '''if request.user.is_authenticated:
                message.info(request,"You have already created account.Please log in ")
                return redirect("user-login")'''
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose another.")
                return render(request, 'register.html', {'user_form': form})
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already taken. Please choose another.")
                return render(request, 'register.html', {'user_form': form})

            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()

            role = form.cleaned_data['role']

            if role == 'doctor':
                Doctor.objects.create(user=user)
                return redirect('doctor_form', user_id=user.id)
            elif role == 'patient':
                Patient.objects.create(user=user,email=user.email)
                return redirect('patient_form', user_id=user.id)
    else:
        form = UserForm()
    return render(request, 'register.html', {'user_form': form})

