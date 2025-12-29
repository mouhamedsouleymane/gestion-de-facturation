#!/bin/bash
# Installation script for Django-Invoice modernized version

echo "🚀 Installing Django-Invoice Modernized Version..."

# Update pip
echo "📦 Updating pip..."
python -m pip install --upgrade pip

# Install requirements
echo "📦 Installing requirements..."
pip install -r requirements.txt

# Check if Django is installed
if ! pip show django > /dev/null 2>&1; then
    echo "⚠️  Django not found, installing..."
    pip install django==4.2
fi

# Create migrations
echo "📝 Creating migrations..."
python manage.py makemigrations fact_app

# Apply migrations
echo "🔄 Applying migrations..."
python manage.py migrate

# Collect static files
echo "📂 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if needed
echo "👤 Creating superuser..."
echo "Note: Leave empty to skip"
python manage.py createsuperuser

echo "✅ Installation complete!"
echo "You can now run: python manage.py runserver"
