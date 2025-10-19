📚 Library Management System API
📖 Overview

The Library Management System API is a backend solution built with Django and Django REST Framework (DRF).
It enables management of library books, users, and book transactions (checkouts and returns).
This project simulates a real-world backend development workflow using MySQL for persistent data storage.

🗓️ Project Timeline (4 Weeks)
Week 1 – Project Setup & Database Design

Initialize Django project and apps (library_app).

Configure environment variables and MySQL connection.

Create models for:

Book

Transaction

Extend User using Django’s built-in authentication.

Design and import the MySQL database schema (library_db.sql) with sample data.

Deliverables:

Working Django project connected to MySQL

Successfully migrated models

Admin interface accessible at /admin'




Week 2 – API Development (CRUD Operations)

Implement CRUD endpoints for:

Books

Users

Enable filtering and searching for books by:

Title, Author, ISBN

Availability (only show available copies)

Add serializers for Book and User.

Deliverables:

Functional /api/books/ and /api/users/ endpoints

Validation for unique ISBNs

Browsable DRF API interface working




Week 3 – Transactions & Authentication

Add JWT authentication using SimpleJWT (/api/token/, /api/token/refresh/).

Implement book check-out and return endpoints:

/api/checkout/

/api/return/

Update logic:

Decrease available copies on checkout

Increase available copies on return

Prevent multiple checkouts of the same book by one user

Track checkout_date and return_date

Deliverables:

Secure endpoints with JWT

Transaction logs showing who borrowed and returned books

Error handling for unavailable books




Week 4 – Testing, Documentation & Deployment Prep

Test all endpoints using Postman or DRF UI.

Write and format project documentation (README.md).

Prepare for optional deployment (Heroku/PythonAnywhere).

Clean up code:

Apply PEP8 formatting

Remove hardcoded credentials

Deliverables:

Completed and documented project

Working local API connected to MySQL

Optional: Deployed API accessible publicly
