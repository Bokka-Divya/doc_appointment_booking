from django.urls import path
from . import views
#from django.urls import path
#from . import views
'''from django.contrib.auth import views as auth_views
from appointment.views import register_view
from appointment.views import doctor_form_view
from appointment.views import patient_form_view'''
urlpatterns = [
    path('', views.home, name='home'),  
    path('login/', views.user_login, name='user-login'),
    path('register/', views.register_view, name='register'),
    path('home-page/', views.home_page, name='home-page'),
    path('patient/', views.patient_page, name='patient-page'),
    path('doctor/', views.doctor_page,name='doctor-page'),
    path('contact/',views.contact_page,name='contact-page'),
    path('book-appointment/', views.book_appointment, name='book-appointment'),
    path('my-appointments/', views.my_appointments, name='my-appointments'),
    path('delete-appointment/<int:appointment_id>/', views.delete_appointment, name='delete-appointment'),
    path('admin/pending-doctors/', views.pending_doctors, name='pending-doctors'),
    path('admin/approve-doctor/<int:doctor_id>/', views.approve_doctor, name='approve-doctor'),
    path('admin/reject-doctor/<int:doctor_id>/', views.reject_doctor, name='reject-doctor'),
    path('approve-appointment/<int:appointment_id>/', views.approve_appointment, name='approve-appointment'),
    
    path('logout/',views.user_logout,name='user-logout'),
    path('admin/approved-doctors/', views.approved_doctors, name='approved_doctors'),
    path('admin/delete-approved-doctor/<int:id>/', views.delete_approved_doctor, name='delete_approved_doctor'),
    path('doctor/form/<int:user_id>/', views.doctor_form_view, name='doctor_form'),
    path('patient/form/<int:user_id>/', views.patient_form_view, name='patient_form'),
    path('admin/dashboard/', views.admin_dashboard, name='admin-dashboard'),
]
