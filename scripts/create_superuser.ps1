param(
    [string]$Username = $env:SUPERUSER_USERNAME,
    [string]$Email = $env:SUPERUSER_EMAIL,
    [string]$Password = $env:SUPERUSER_PASSWORD
)

if (-not $Username) { $Username = 'admin' }
if (-not $Email) { $Email = 'admin@example.com' }
if (-not $Password) { $Password = 'adminpass' }

$env:SUPERUSER_USERNAME = $Username
$env:SUPERUSER_EMAIL = $Email
$env:SUPERUSER_PASSWORD = $Password

Write-Host "Creating dev superuser: $Username <$Email> (development only)"
python .\scripts\create_dev_superuser.py
