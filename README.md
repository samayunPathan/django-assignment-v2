# Django-Scrapy-data Application

## Project Overview

This project is a Django application designed to store and manage property information using the Django admin interface. The application includes models to represent properties, locations, amenities, and images, with proper relationships between them. The admin interface provides full CRUD (Create, Read, Update, Delete) capabilities, ensuring that users can manage property data effectively. Additionally, a Django CLI application is provided to migrate data from a Scrapy project database to the Django application.
## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Task Breakdown](#task-breakdown)
  - [1. Create Django Models and Migrations](#1-create-django-models-and-migrations)
  - [2. Use Django Admin with Proper Authentication](#2-use-django-admin-with-proper-authentication)
  - [3. Write Django CLI Application](#3-write-django-cli-application)
- [Installation Guide](#installation-guide)
  - [1. Set Up the Environment](#1-set-up-the-environment)
  - [2. Clone the Repository](#2-clone-the-repository)
  - [3. Create a Virtual Environment](#3-create-a-virtual-environment)
  - [4. Install Dependencies](#4-install-dependencies)
  - [5. Configure PostgreSQL](#5-configure-postgresql)
  - [6. Apply Migrations](#6-apply-migrations)
  - [7. Create a Superuser](#7-create-a-superuser)
  - [8. Run the Development Server](#8-run-the-development-server)
  - [9. Migrate Data from Scrapy](#9-migrate-data-from-scrapy)
- [Usage](#usage)
  
## Features

- **Django Models**: Custom models for properties, locations, amenities, and images.
- **Relationships**: One-to-many and many-to-many relationships between models.
- **Django Admin**: Full CRUD capabilities with authentication and user management.
- **Data Migration**: CLI application for migrating data from a Scrapy project database.
- **PostgreSQL Database**: Utilizes PostgreSQL for database management.
- **Django ORM**: Leverages Django's powerful ORM for database operations.

## Task Breakdown

### 1. Create Django Models and Migrations

- **Property Model**:
  - `property_id`: Unique identifier for each property.
  - `title`: Title of the property.
  - `description`: Detailed description of the property.
  - `images`: One-to-many relationship with the `Image` model.
  - `location`: Many-to-many relationship with the `Location` model.
  - `latitude`: Latitude coordinate of the property.
  - `longitude`: Longitude coordinate of the property.
  - `amenities`: Many-to-many relationship with the `Amenity` model.
  - `create_date`: Timestamp when the property record was created.
  - `update_date`: Timestamp when the property record was last updated.

- **Location Model**:
  - `name`: Name of the location.
  - `type`: Type of location (e.g., country, state, city).
  - `latitude`: Latitude of location.
  - `longitude`: Longitude of location.

- **Amenity Model**:
  - `name`: Name of the amenity.

- **Image Model**:
  - `image_path`: Path to the image file.

### 2. Use Django Admin with Proper Authentication

- Enable Django's built-in admin interface with proper authentication to manage all models.
- Implement CRUD operations for all models while maintaining their relationships.

### 3. Write Django CLI Application

- Develop a Django CLI tool to migrate all property data from the Scrapy project PostgreSQL database to the Django application.


## Installation Guide
#### First go to scrapy project repo
https://github.com/samayunPathan/Scrapy-assignment.git  
#### Download/clone this and  setup in your system , run scrapy project in your system its project path and database credentions required to that Django project. 


### 1. Set Up the Environment

Ensure you have Python and PostgreSQL installed on your machine.

- **Python**: Install the latest version of Python from [python.org](https://www.python.org/).
- **PostgreSQL**: Install PostgreSQL from [postgresql.org](https://www.postgresql.org/).

### 2. Clone the Repository

```bash
git clone https://github.com/samayunPathan/django-assignment-v2.git
```
``` bash
cd django-assignment-v2
```
### 3. Create a Virtual Environment
```bash
python -m venv venv
```
```bash
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### 4. Install Dependencies
``` bash 
pip install -r requirements.txt
```
### 5. Configure PostgreSQL
- Set up your PostgreSQL database and user.
- Create a .pg_service.conf file in your home directory with the following content:
```bash
[django_model_db]
host=localhost
port=5432
dbname=scrapy_db
user=your_db_user
password=your_db_password

## Its scrapy_project database credentials

[scrapy_db] 
host=localhost
port=5432
dbname=scrapy_db
user=your_db_user
password=your_db_password
scrapy_image_dir='your scrapy project downloaded images path'
```
- Update the Django settings.py to use the service name:
``` bash 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'OPTIONS': {
            'service': 'scrapy_db',
        },
    }
}
```
- Update the `properties/management/commands/migrate_scrapy_data` to use the service name:
``` bash 
conn = psycopg2.connect(service='scrapy_db')
```
### 6. Apply Migrations
``` bash
python manage.py makemigrations
python manage.py migrate
```
### 7. Create a Superuser
```bash
python manage.py createsuperuser
```
### 8. Run the Development Server
```bash 
python manage.py runserver
```
Access the Django admin panel at http://127.0.0.1:8000/admin/ and log in with your superuser credentials.

### 9. Migrate Data from Scrapy
```bash
python manage.py migrate_scrapy_data
```

## Usage
- Manage properties, locations, amenities, and images through the Django admin interface.
- Perform CRUD operations on all models while maintaining their relationships.
