# 🔍 Lost and Found Management System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-purple.svg)

**A comprehensive web-based platform for managing lost and found items within organizations**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack) 

</div>

---

## 📋 Overview

The Lost and Found Management System is a full-stack web application designed to streamline the process of reporting, tracking, and claiming lost or found items within an organization. Built with Flask and MySQL, it provides separate interfaces for users and administrators with robust claim management and automated cleanup features.

## ✨ Features

### 👥 User Features
- **🔐 User Registration & Authentication** - Secure account creation and login system
- **📝 Item Reporting** - Report lost or found items with detailed descriptions and images
- **🔍 Item Browse** - View categorized lists of lost and found items
- **📋 Claim Management** - Submit claims for items with detailed forms
- **💬 Messaging System** - Communicate with admins regarding claims
- **📊 Personal Dashboard** - Track your posted items and submitted claims

### 🛠️ Admin Features
- **🎛️ Admin Dashboard** - Comprehensive overview of all system activities
- **✅ Claim Approval** - Review and approve/reject claim requests
- **👥 User Management** - View and manage user accounts and data
- **📈 Analytics** - Monitor system usage and item statistics
- **💌 Feedback Management** - View and respond to user feedback

### 🔧 System Features
- **🗂️ Advanced Database Operations** - Stored procedures and triggers for efficient data management
- **🧹 Automatic Cleanup** - Scheduled removal of old items using APScheduler
- **📱 Responsive Design** - Mobile-friendly interface with Bootstrap
- **🖼️ Image Management** - Secure image upload and storage system
- **📧 Feedback System** - Integrated user feedback collection

## 🚀 Tech Stack

<table>
<tr>
<td align="center"><strong>Layer</strong></td>
<td align="center"><strong>Technology</strong></td>
<td align="center"><strong>Purpose</strong></td>
</tr>
<tr>
<td><strong>Frontend</strong></td>
<td>HTML, CSS, Bootstrap 5</td>
<td>Responsive user interface</td>
</tr>
<tr>
<td><strong>Backend</strong></td>
<td>Flask (Python)</td>
<td>Web framework and API</td>
</tr>
<tr>
<td><strong>Database</strong></td>
<td>MySQL</td>
<td>Data storage with procedures & triggers</td>
</tr>
<tr>
<td><strong>Scheduler</strong></td>
<td>APScheduler</td>
<td>Automated background tasks</td>
</tr>
<tr>
<td><strong>Connector</strong></td>
<td>mysql-connector-python</td>
<td>Database connectivity</td>
</tr>
</table>

## 📁 Project Structure

```
lost-found-system/
│
├── 📁 static/
│   ├── 🎨 css/
│   │   └── style.css
│   ├── 📜 js/
│   │   └── main.js
│   └── 📷 uploads/
│       └── (user uploaded images)
│
├── 📁 templates/
│   ├── 🏠 index.html
│   ├── 🔐 login.html
│   ├── 📝 register.html
│   ├── 🎛️ dashboard.html
│   ├── 👨‍💼 admin_dashboard.html
│   ├── 📋 report_item.html
│   ├── 🔍 view_items.html
│   └── 📧 feedback.html
│
├── 🐍 app.py                 # Main Flask application
└── 📖 README.md             # This file
```

## 🔧 Installation

### Prerequisites
- Python 3.8 or higher
- MySQL 8.0 or higher
- pip package manager

### Step-by-Step Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/lost-found-system.git
   cd lost-found-system
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```sql
   CREATE DATABASE lost_found_db;
   USE lost_found_db;
   -- Run your database schema script here
   ```

5. **Configure database connection**
   Update `db_connection.py` with your MySQL credentials:
   ```python
   config = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'lost_found_db'
   }
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://localhost:5000`

## 🎯 Usage

### For Users
1. **Register/Login** - Create an account or log in to access the system
2. **Report Items** - Use the "Report Lost/Found Item" feature to add items
3. **Browse Items** - View all reported items in categorized lists
4. **Submit Claims** - Claim items that belong to you with verification details
5. **Track Status** - Monitor your claims and posted items in your dashboard

### For Administrators
1. **Admin Login** - Access the admin panel with administrator credentials
2. **Manage Claims** - Review and approve/reject user claims
3. **User Management** - View user accounts and manage system users
4. **System Monitoring** - Track system usage and maintain item database

## 🔐 Authentication & Security

- **Session-based Authentication** - Secure user sessions with Flask sessions
- **Role-based Access Control** - Separate user and admin access levels
- **Input Validation** - Server-side validation for all user inputs
- **Secure File Upload** - Safe handling of user-uploaded images
- **Database Security** - Parameterized queries to prevent SQL injection

## 🗄️ Database Schema

The system uses a well-structured MySQL database with the following key tables:

- **`users`** - User account information
- **`lost_items`** - Lost item records
- **`found_items`** - Found item records
- **`claims`** - Claim submissions and status
- **`feedback`** - User feedback and messages

**Advanced Database Features:**
- **Stored Procedures** - Efficient data operations
- **Triggers** - Automated status updates
- **Joins** - Complex data relationships
- **Indexing** - Optimized query performance

## 📱 Screenshots

<div align="center">![1](https://github.com/user-attachments/assets/ea82db55-63e2-49db-a5f2-e5373bd673a5)

Made with ❤️ for better organization management
</div>
