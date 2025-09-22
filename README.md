Doctor Appointment Booking System

By Bokka Divya

This is a simple Django web application that helps patients book appointments with doctors. The system has different dashboards for patients and doctors, and an admin panel to approve doctors. It also sends email notifications to keep everyone informed. The UI is built with Bootstrap, making it clean and responsive.



What the App Does

For Patients:
Patients can browse a list of approved doctors, book appointments, and manage their appointments.

For Doctors:
Doctors can view pending appointments and approve them. They do not manage availability.

For Admins:
Admins can approve new doctors and see which doctors are approved or waiting for approval. Admins do not manage appointments.

Email Notifications:
Patients get an email when their appointment is approved by a doctor.

Responsive Design:
The app uses Bootstrap for a modern, mobile-friendly layout.




Skills and Technologies

Python & Django

HTML, CSS, JavaScript

Bootstrap





How to Run the App

1. Open Command Prompt or Terminal in the project folder


2. Start the server:

python manage.py runserver 8000


3. Open your browser and go to:

localhost:8000/appointment/





How to Use the App

Patients: Sign up, browse doctors, and book appointments through your dashboard.

Doctors: Log in to see pending appointments and approve them.

Admin: Approve pending doctors and view approved doctors.





Project Structure

templates/ – HTML pages for patients, doctors, admin, and common views

static/ – CSS, JavaScript, images

models.py – Database models for users, doctors, and appointments

views.py – Application logic

urls.py – URL routing
