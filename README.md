# Doctor Appointment Booking System 

**By Bokka Divya**

This is a simple Django web application that helps patients book appointments with doctors. The system has **different dashboards for patients and doctors**, and an **admin panel** to approve doctors. It also sends **email notifications** to keep everyone informed. The UI is built with **Bootstrap**, making it clean and responsive.

---

## What the App Does

- **For Patients:**  
  Browse a list of approved doctors, book appointments, and manage their appointments.

- **For Doctors:**  
  View pending appointments and approve them. Doctors **do not manage availability**.

- **For Admins:**  
  Approve new doctors and see which doctors are approved or waiting for approval. Admins **do not manage appointments**.

- **Email Notifications:**  
  Patients get an email when their appointment is approved by a doctor.

- **Responsive Design:**  
  Built with **Bootstrap** for a modern, mobile-friendly layout.

---

## Skills and Technologies

- Python & Django  
- HTML, CSS, JavaScript  
- Bootstrap  

---

## How to Run the App

1. Open **Command Prompt** or **Terminal** in the project folder  
2. Start the server by running:  
   ```bash
   python manage.py runserver 8000
Doctors: Log in to see pending appointments and approve them.

Admin: Approve pending doctors and view approved doctors.





Project Structure

templates/ – HTML pages for patients, doctors, admin, and common views

static/ – CSS, JavaScript, images

models.py – Database models for users, doctors, and appointments

views.py – Application logic

urls.py – URL routing
