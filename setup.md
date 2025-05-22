Fresh Futures Location Setup Guide
This guide will help you set up PostGIS and GeoDjango for the location features in Fresh Futures.

Prerequisites

macOS with Homebrew installed
Git access to the project repository

Step 1: Install PostgreSQL 17 + PostGIS

bash# 

# Install PostgreSQL 17

brew install postgresql@17

# If you have other PostgreSQL versions, unlink them first:
brew unlink postgresql@14 postgresql@16

# Link PostgreSQL 17 as your default
brew link postgresql@17

# Add PostgreSQL 17 to your PATH (recommended)
echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Start PostgreSQL service
brew services start postgresql@17

# Install PostGIS
brew install postgis

# Verify PostgreSQL is working
psql --version
# Should show: psql (PostgreSQL) 17.x


Step 2: Create Database

bash# 

# Create the project database
createdb fresh_futures_db

# Enable PostGIS extension
psql fresh_futures_db -c "CREATE EXTENSION postgis; SELECT PostGIS_Version();"

# Expected output:
CREATE EXTENSION
            postgis_version            
---------------------------------------
 3.5 USE_GEOS=1 USE_PROJ=1 USE_STATS=1
(1 row)


Step 3: Set Up Django Environment

bash# 

# Navigate to your project directory
cd fresh-futures

# Switch to the location integration branch
git checkout casey/location-integration
git pull origin casey/location-integration

# Install Python dependencies
pipenv install django psycopg2-binary python-dotenv


# Activate virtual environment
pipenv shell

Step 4: Configure Environment Variables

bash# 

# Edit your .env file with your database credentials:
envDB_USER=your_mac_username
DB_PASSWORD=
MAPBOX_ACCESS_TOKEN=pk.eyJ1IjoiY2FzZXlqb2luZXIiLCJhIjoiY20zdWU4a2puMGh3MDJqc2N6a2VvODh5cyJ9.example_token_here

# To find your Mac username: run whoami in terminal


Step 5: Test Django Setup

bash# 

Run Django migrations
python manage.py migrate

# Test Django shell
python manage.py shell

# In the Django shell, test GeoDjango:

python

>>> from django.contrib.gis.geos import Point
>>> point = Point(-122.4194, 37.7749)
>>> print(f"Created point: {point}")
Created point: POINT (-122.4194 37.7749)
>>> exit()

# Troubleshooting
PostgreSQL Connection Issues

bash#

# Check if PostgreSQL is running
brew services list | grep postgresql

# Restart if needed
brew services restart postgresql@17

# Check your username
whoami


# PostGIS Extension Issues
bash# 

# Verify PostGIS is installed
brew list postgis

# Recreate database if needed
dropdb fresh_futures_db
createdb fresh_futures_db
psql fresh_futures_db -c "CREATE EXTENSION postgis;"

# Django Import Errors
bash#

# Make sure virtual environment is active
pipenv shell

# Check installed packages
pipenv run pip list | grep django


# Success Checklist

 PostgreSQL 17 installed and running
 PostGIS extension working (shows version when queried)
 Database fresh_futures_db created
 Django shell loads without errors
 GeoDjango Point creation works
 Environment variables configured


Once your setup is complete, you can start integrating location features into your assigned components:

Anna: Add location fields to Garden model
Amen: Add location selection to garden forms
Wen: Add location to user registration
Casey: Map components and BeetBot integration