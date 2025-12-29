

from pathlib import Path
import os 
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

try:
    from django.contrib.messages import constants as messages
    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger'
    }
except Exception as e:
    pass    

SECRET_KEY = config('SECRET_KEY', default="django-invoiceadfasdfa")


ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default='*').split(",")



# Application definition

INSTALLED_APPS = [
    # Jazzmin admin interface (must be before django.contrib.admin)
    'jazzmin',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    "whitenoise.runserver_nostatic",

    'django.contrib.staticfiles',
    
    # third party apps
    "django_celery_beat",
    
    # local app 
    'fact_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'django_invoice.urls'
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'django_invoice.wsgi.application'




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

from django.utils.translation import gettext_lazy as _

LANGUAGES = [
('fr', _('French')),
('en', _('English')),
]

USE_I18N = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static/'),)

MEDIA_URL = 'media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# JAZZMIN CONFIGURATION (Modern Django Admin)
# ============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "Invoice System",
    "site_header": "📊 Invoice Management System",
    "site_brand": "📋 Invoice System",
    "site_logo": None,
    "welcome_sign": "Welcome to Invoice System Administration",
    "copyright": "Donald Tè © 2025 - Invoice Management System",
    
    # Sidebar
    "show_sidebar": True,
    "navigation_expanded": False,
    
    # Colorscheme
    "usertheme_use_navbar": True,
    "changeform_format": "vertical_tabs",
    "changeform_format_overrides": {
        "auth.user": "horizontal_tabs",
        "auth.permission": "vertical_tabs",
    },
    "language_chooser": True,
    
    # Search
    "search_model": ["fact_app.invoice", "fact_app.customer"],
    
    # Icons
    "icons": {
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "fact_app.invoice": "fas fa-file-invoice-dollar",
        "fact_app.customer": "fas fa-users",
        "fact_app.article": "fas fa-shopping-cart",
    },
    
    # Default Icon
    "default_icon_parents": "fas fa-chevron-right",
    "default_icon_children": "fas fa-arrow-right",
    
    # Custom Navigation
    "show_ui_builder": False,
    "navigation": [
        {
            "name": "📊 Dashboard",
            "url": "/admin/",
            "icon": "fas fa-home",
        },
        {
            "name": "💼 Management",
            "icon": "fas fa-briefcase",
            "children": [
                {
                    "name": "👥 Customers",
                    "url": "/admin/fact_app/customer/",
                    "icon": "fas fa-users",
                },
                {
                    "name": "📋 Invoices",
                    "url": "/admin/fact_app/invoice/",
                    "icon": "fas fa-file-invoice-dollar",
                },
                {
                    "name": "📦 Articles",
                    "url": "/admin/fact_app/article/",
                    "icon": "fas fa-shopping-cart",
                },
            ],
        },
        {
            "name": "🔐 Users & Permissions",
            "icon": "fas fa-lock",
            "children": [
                {
                    "name": "👤 Users",
                    "url": "/admin/auth/user/",
                    "icon": "fas fa-user",
                },
                {
                    "name": "🔑 Permissions",
                    "url": "/admin/auth/permission/",
                    "icon": "fas fa-key",
                },
                {
                    "name": "👥 Groups",
                    "url": "/admin/auth/group/",
                    "icon": "fas fa-user-shield",
                },
            ],
        },
        {
            "name": "📱 SPA",
            "url": "/spa/",
            "icon": "fas fa-mobile-alt",
        },
    ],
    
    # Disable admin site
    "show_admin_site": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small": False,
    "footer_small": False,
    "body_small": False,
    "sign_up_to_dashboard": True,
    "navbar_fixed": False,
    "sidebar_fixed": False,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-info",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success",
    },
    "actions_sticky_top": False,
}

LOGIN_URL = 'admin:login'
