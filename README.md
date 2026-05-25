

# Integrated Academics Management System

A university-level platform with role-based access built with Django and MySQL.  
The Main Assistant manages departments and grants access to Department Assistants.  
Departments manage faculty, students, generate semester timetables, and upload syllabus and previous papers.  
Students can view timetables and download academic resources.

---

## Requirements

- Python 3.10+
- MySQL 8.0+

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

```
MYSQL_DATABASE=academics_management_system
MYSQL_USER=root
MYSQL_PASSWORD=Priyas$5
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## Notes

- This project uses **MySQL only** 
- Never commit your `.env` file (it is in `.gitignore`).
