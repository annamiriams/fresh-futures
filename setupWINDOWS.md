# Prerequisites

Windows 10/11
Git for Windows installed
Python 3.8+ installed
Git access to the project repository

# Step 1: Install PostgreSQL 17 + PostGIS

## Option A (in line with GA installation process):

sudo apt-get --purge remove postgresql-16
sudo apt install postgresql-17
psql --version
### Should show: psql (PostgreSQL) 17.5 (Ubuntu 17.5-1.pgdg24.04+1)
### Make sure you have version 17, not 16

## Option B: PostgreSQL Installer (Recommended per original guide, but bypassing due to the above)

### Download PostgreSQL 17 from 
https://www.postgresql.org/download/windows/
### Run the installer
### During installation:

### Set a password for the postgres user (remember this!)
### Keep default port 5432
### When prompted to launch Stack Builder, click Yes

### In Stack Builder:
Select your PostgreSQL installation
Expand "Spatial Extensions"
Check PostGIS Bundle
Follow installation prompts

## Option B: Using Chocolatey (if you have it)
powershell
### Install PostgreSQL and PostGIS
choco install postgresql --params '/Password:your_password_here'
choco install postgis

### Verify Installation
Open Command Prompt or PowerShell:
cmd
psql --version
### Should show: psql (PostgreSQL) 17.x

# Step 2: Create Database
Open Command Prompt as Administrator and run:

cmd
## Set environment variable for easier psql access
set PGPASSWORD=your_postgres_password

## Create the project database
createdb -U postgres fresh_futures_db

## Enable PostGIS extension
### This next line didn't work
psql -U postgres -d fresh_futures_db -c "CREATE EXTENSION postgis; SELECT PostGIS_Version();"

### install postgis-3
sudo apt-get install postgresql-17-postgis-3 postgresql-17-postgis-3-scripts

### enable extension (replaces the non-working line above)
sudo -u postgres psql -d fresh_futures_db -c "CREATE EXTENSION postgis; SELECT PostGIS_Version();"

Expected output:
CREATE EXTENSION
            postgis_version            
---------------------------------------
 3.5 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
(1 row)

### To test postgis version without enabling the extension above, use this:
psql
SELECT * FROM pg_available_extensions WHERE name = 'postgis';

# Step 3: Set Up Django Environment
cmd
## Navigate to your project directory
cd fresh-futures

# no need to checkout branch because this is now merged with the main branch
## Switch to the location integration branch
git checkout casey/location-integration
git pull origin casey/location-integration

## Install Python dependencies
pip install pipenv
pipenv install django psycopg2-binary python-dotenv

## Activate virtual environment
pipenv shell

# Step 4: Configure Environment Variables
Create a .env file in your project root with your database credentials:

DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoiY2FzZXlqb2luZXIiLCJhIjoiY20zdWU4a2puMGh3MDJqc2N6a2VvODh5cyJ9.example_token_here
SECRET_KEY=your_secret_key

# Step 5: Test Django Setup
cmd
## Run Django migrations
<!-- python manage.py migrate -->
python3 manage.py migrate

## Test Django shell
python manage.py shell

## In the Django shell, test GeoDjango:
python
>>> from django.contrib.gis.geos import Point
>>> point = Point(-122.4194, 37.7749)
>>> print(f"Created point: {point}")
Created point: POINT (-122.4194 37.7749)
>>> exit()

# Troubleshooting
## PostgreSQL Connection Issues
cmd
## Check if PostgreSQL service is running
net start postgresql-x64-17

## Or using Services app:
## Press Win+R, type "services.msc", find "postgresql-x64-17"
PostGIS Extension Issues

cmd

## Verify PostGIS is available
psql -U postgres -c "SELECT name FROM pg_available_extensions WHERE name='postgis';"

## If not found, reinstall PostGIS through Stack Builder

## Path Issues
Add PostgreSQL bin directory to your PATH:

Search "Environment Variables" in Start Menu
Click "Environment Variables" button
In System Variables, find "Path"
Add: C:\Program Files\PostgreSQL\17\bin

## Django Import Errors
cmd
## Make sure virtual environment is active
pipenv shell

## Check installed packages
pipenv run pip list | findstr django

## Permission Issues

Run Command Prompt as Administrator when creating databases
Make sure your Windows user has sufficient privileges

## Alternative: Using WSL2 (Windows Subsystem for Linux)
If you encounter issues with Windows setup, you can use WSL2 with Ubuntu and follow the macOS/Linux instructions:

powershell
## Install WSL2 with Ubuntu
wsl --install -d Ubuntu

## After setup, use the Linux commands from the original guide
Success Checklist

✅ PostgreSQL 17 installed and running
✅ PostGIS extension working (shows version when queried)
✅ Database fresh_futures_db created
✅ Django shell loads without errors
✅ GeoDjango Point creation works
✅ Environment variables configured
✅ pipenv shell activates without errors

Additional Windows Notes

Use Command Prompt or PowerShell instead of Terminal
File paths use backslashes (\) instead of forward slashes (/)
Some commands may require Administrator privileges
PostgreSQL service should auto-start with Windows