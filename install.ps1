# Installation script for Django-Invoice modernized version (Windows PowerShell)

Write-Host "🚀 Installing Django-Invoice Modernized Version..." -ForegroundColor Green

# Update pip
Write-Host "📦 Updating pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install requirements
Write-Host "📦 Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Check if Django is installed
try {
    pip show django | Out-Null
} catch {
    Write-Host "⚠️  Django not found, installing..." -ForegroundColor Yellow
    pip install "django==4.2"
}

# Create migrations
Write-Host "📝 Creating migrations..." -ForegroundColor Yellow
python manage.py makemigrations fact_app

# Apply migrations
Write-Host "🔄 Applying migrations..." -ForegroundColor Yellow
python manage.py migrate

# Collect static files
Write-Host "📂 Collecting static files..." -ForegroundColor Yellow
python manage.py collectstatic --noinput

# Create superuser
Write-Host "👤 Creating superuser..." -ForegroundColor Yellow
Write-Host "Note: Leave empty to skip" -ForegroundColor Gray
python manage.py createsuperuser

Write-Host "✅ Installation complete!" -ForegroundColor Green
Write-Host "You can now run: python manage.py runserver" -ForegroundColor Cyan
