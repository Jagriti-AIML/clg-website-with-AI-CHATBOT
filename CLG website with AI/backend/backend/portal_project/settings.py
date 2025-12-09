# settings.py

# ... (Standard Django settings)

INSTALLED_APPS = [
    # ... other apps
    'rest_framework',
    'portal_app.apps.PortalAppConfig',
    'corsheaders',  # Required for React integration
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', # Add this line
    # ... other middleware
]

# Configure your React frontend development server access
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# MySQL Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'college_portal_db',
        'USER': 'your_mysql_user',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# ... (other standard settings like TEMPLATES, STATIC_URL, etc.)