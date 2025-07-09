📌 Overview
A web-based platform for managing lost and found items within an organization. Users can report lost or found items, and administrators can manage submissions and claims. The system includes automated cleanup, PDF generation, and basic messaging.

🚀 Features
👤 User Features
User registration and login

Report lost or found items with image and description

View list of items by type (lost/found)

Claim items by submitting a claim form

Send messages regarding claims

View own posted and claimed items

🛠️ Admin Features
Login to admin dashboard

View all reported items

Approve or reject claim requests

View and manage user data

View feedback messages

📄 Other Functionalities
PDF generation of lost/found item records using reportlab

Automatic cleanup of items older than a certain date using APScheduler

Feedback form for users

Stored procedures and triggers in MySQL to manage item and user operations

🗂️ Tech Stack
Layer	Technology
Frontend	HTML, CSS, Bootstrap
Backend	Flask (Python)
Database	MySQL with triggers and procedures
PDF	ReportLab
Scheduler	APScheduler

📁 File Structure (Simplified)
php
Copy
Edit
project/
│
├── static/
│   └── css, js, uploads
├── templates/
│   └── *.html files (login, dashboard, etc.)
├── app.py
├── script.py              # PDF generation logic
├── scheduler.py           # Auto-deletion of old items
├── db_connection.py
└── requirements.txt
🔐 Authentication
Session-based user and admin login system

Login pages redirect based on user type

Role-based access control for admin/user panels

🧠 Database Logic
MySQL schema with tables:

users, lost_items, found_items, claims, feedback, etc.

Includes:

Stored procedures for item insertion

Triggers to auto-update claim status or cleanup

Joins for fetching data across tables

📦 Dependencies (from requirements.txt)
Flask

ReportLab

APScheduler

mysql-connector-python

Other standard Python packages (os, time, etc.)
