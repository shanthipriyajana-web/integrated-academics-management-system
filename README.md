# Integrated Academic Management System

A university-level platform with role-based access built using Django and MySQL.
The Main Assistant manages departments and grants access to Department Assistants.
Departments manage faculty, students, generate semester timetables, and upload syllabus and previous papers.
Students can view timetables and download academic resources.

---

## Features

* Role-Based Authentication
* Automated Timetable Scheduling
* Faculty & Student Dashboards
* Academic Resource Management
* Syllabus & Previous Papers Upload
* Department-Wise Access Control
* Conflict-Free Timetable Generation

---

## Technologies Used

* Python
* Django
* React.js
* MySQL
* HTML
* CSS
* JavaScript

---

## Requirements

* Python 3.10+
* MySQL 8.0+

---

## Setup Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create the MySQL database

Open MySQL and run:

```sql
CREATE DATABASE academics_management_system;
```

### 3. Configure your credentials

Copy the example env file:

```bash
copy .env.example .env        # Windows
# OR
cp .env.example .env          # Mac/Linux
```

Edit `.env` and set your MySQL password:

```env
MYSQL_DATABASE=academics_management_system
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the server

Run the Django development server:

```bash
python manage.py runserver

---
## Project Demo Video
[watch the project demo video](https://drive.google.com/file/d/1dhMl6TkbxuTnoDMN0cxHrciTKUsKD_ML/view?usp=sharing)
---

## Notes

* This project uses MySQL only
* Never commit your `.env` file (it is included in `.gitignore`)


