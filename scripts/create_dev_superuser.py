#!/usr/bin/env python3
"""
create_dev_superuser.py

Non-interactive helper to create a development superuser.

Usage (Linux/macOS):
  SUPERUSER_USERNAME=admin SUPERUSER_EMAIL=admin@example.com SUPERUSER_PASSWORD=pass python scripts/create_dev_superuser.py

Usage (Windows PowerShell):
  $env:SUPERUSER_USERNAME='admin'; $env:SUPERUSER_EMAIL='admin@example.com'; $env:SUPERUSER_PASSWORD='pass'; python scripts/create_dev_superuser.py

This script is intended for development only. Do NOT use these defaults in production.
"""
import os
import sys

def setup_django():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE', 'django_invoice.local'))
    # Ensure project root is on sys.path so Django can import the project package
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    try:
        import django
        django.setup()
    except Exception as exc:
        print('Failed to setup Django:', exc)
        sys.exit(1)


def main():
    setup_django()
    try:
        from django.contrib.auth import get_user_model
    except Exception as exc:
        print('Django auth not available:', exc)
        sys.exit(1)

    User = get_user_model()
    username = os.environ.get('SUPERUSER_USERNAME', 'admin')
    email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
    password = os.environ.get('SUPERUSER_PASSWORD', 'adminpass')

    if User.objects.filter(username=username).exists():
        print(f"Superuser '{username}' already exists. Skipping creation.")
        return

    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Created superuser '{username}' with email '{email}'. (Development only)")
        print('WARNING: default credentials are insecure. Change password immediately in production.')
    except Exception as exc:
        print('Failed to create superuser:', exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
