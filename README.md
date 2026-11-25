# Aras 3D 🖨️

A Django-based product showcase website for 3D-printed products.

## Overview

Aras 3D is a web application designed to showcase 3D-printed products. Visitors can explore the product catalog, view product details and images, learn more about the business, and contact the company.

The website also provides a Django administration panel for managing products, product images, and contact messages.

## Features

### Customer Features

- Homepage with business information
- About page
- Product catalog
- Individual product detail pages
- Multiple images per product
- Contact form
- Responsive website interface

### Product Management

- Product and category management
- Multiple images for each product
- Product image validation
- Django administration panel

### Contact System

- Online contact form
- Contact message management through Django Admin

## Technologies

- Python
- Django
- SQLite
- HTML5
- CSS3
- JavaScript
- Pillow

## Project Structure

```text
aras_3D/
├── catalog/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── validators.py
│   ├── views.py
│   └── urls.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/
│   ├── base.html
│   └── catalog/
│       ├── about.html
│       ├── contact.html
│       ├── home.html
│       ├── product_detail.html
│       └── product_list.html
├── .env.example
├── .gitignore
├── manage.py
└── requirements.txt
```

## Requirements

- Python 3.12 or newer
- pip
- Git

## Installation

### 1. Clone the repository

```bash
git clone <REPOSITORY_URL>
cd aras_3D
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Apply database migrations

```bash
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Main Routes

| Route | Description |
|---|---|
| `/` | Homepage |
| `/products/` | Product catalog |
| `/products/<slug>/` | Product details |
| `/about/` | About page |
| `/contact/` | Contact page |
| `/admin/` | Django administration |

## Environment Variables

The application supports the following environment variables:

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django secret key |
| `DJANGO_DEBUG` | Enables or disables debug mode |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames |

The `.env.example` file provides an example configuration. Environment variables must be configured in the operating system or deployment environment; Django does not automatically load `.env` files in this project.

Never publish actual secrets or private environment configuration.

## License

No license has been specified yet.