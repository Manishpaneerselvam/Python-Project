# Python-Project

A RESTful backend application built using Python, Django, and Django REST Framework to manage personal financial data. The system allows users to track income and expenses, manage categories, automate recurring transactions, and generate financial summaries.

Features:
User registration and login
Add and manage categories
Add, update, and delete transactions
Recurring transactions (like rent or salary)
Monthly income and expense summary

Technologies Used:
Python
Django
Django REST Framework
SQLite / MySQL
Django ORM

How to run the project:
1. Clone the repository:
  git clone https://github.com/your-username/finance-tracker.git
cd finance-tracker

2.Create a virtual environment:
  python -m venv venv

3.Install dependencies:
  pip install django djangorestframework

4.Apply migrations:
  python manage.py makemigrations
  python manage.py migrate

5.Create superuser (optional)
  python manage.py createsuperuser

6.Run the server
  python manage.py runserver

7.API Base URL:
  http://127.0.0.1:8000/api/
