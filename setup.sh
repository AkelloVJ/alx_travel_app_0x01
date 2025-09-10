#!/bin/bash

# ALX Travel App Setup Script
echo "Setting up ALX Travel App..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "Installing requirements..."
pip install -r requirement.txt

# Run migrations
echo "Running database migrations..."
python manage.py migrate

# Create superuser (optional)
echo "Creating superuser..."
echo "You can create a superuser by running: python manage.py createsuperuser"

# Collect static files (if needed)
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
echo ""
echo "To start the server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit:"
echo "  - API: http://localhost:8000/api/"
echo "  - Admin: http://localhost:8000/admin/"
echo "  - Swagger: http://localhost:8000/swagger/"
echo "  - ReDoc: http://localhost:8000/redoc/"
