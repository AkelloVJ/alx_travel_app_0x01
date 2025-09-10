# ALX Travel App - Milestone 2: Models, Serializers, and Seeders

This project implements the backend components for a travel booking platform using Django and Django REST Framework. This milestone focuses on creating database models, serializers for API data representation, and a management command for database seeding.

## Features Implemented

### 1. Database Models

#### Listing Model
- **Fields**: title, description, price, location, property_type, bedrooms, bathrooms, max_guests, amenities, is_available, host
- **Relationships**: One-to-Many with User (host), One-to-Many with Booking, One-to-Many with Review
- **Constraints**: Price validation (minimum 0), property type choices, positive integer fields

#### Booking Model
- **Fields**: listing, guest, check_in, check_out, total_price, status, special_requests
- **Relationships**: Many-to-One with Listing, Many-to-One with User (guest), One-to-Many with Review
- **Constraints**: Unique constraint on listing + check_in + check_out, date validation

#### Review Model
- **Fields**: listing, guest, booking, rating, comment
- **Relationships**: Many-to-One with Listing, Many-to-One with User (guest), Many-to-One with Booking
- **Constraints**: Rating validation (1-5 stars), unique constraint on listing + guest + booking

### 2. Serializers

#### ListingSerializer
- Full representation with nested host and reviews
- Calculated fields: average_rating, review_count
- Read-only fields for timestamps and host

#### BookingSerializer
- Full representation with nested listing and guest
- Write-only fields for listing_id and guest_id
- Date validation for check-in/check-out

#### ReviewSerializer
- Simple representation with nested guest information
- Read-only fields for timestamps

### 3. Database Seeder

#### Management Command: `seed`
- **Location**: `listings/management/commands/seed.py`
- **Features**:
  - Creates sample users with realistic names
  - Generates property listings with various types and locations
  - Creates bookings with realistic date ranges and statuses
  - Generates reviews for completed bookings
  - Configurable parameters for number of users and listings
  - Clear option to remove existing data

#### Usage:
```bash
# Basic seeding
python manage.py seed

# Custom parameters
python manage.py seed --users 10 --listings 20

# Clear existing data first
python manage.py seed --clear --users 5 --listings 10
```

## Project Structure

```
alx_travel_app_0x00/
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── listings/
│   ├── __init__.py
│   ├── models.py          # Listing, Booking, Review models
│   ├── serializers.py     # DRF serializers
│   ├── management/
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed.py    # Database seeder command
│   ├── admin.py
│   ├── apps.py
│   ├── migrations/
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirement.txt
└── README.md
```

## Setup Instructions

1. **Activate Virtual Environment**:
   ```bash
   source venv/bin/activate
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

3. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Seed Database**:
   ```bash
   python manage.py seed
   ```

5. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## Database Schema

The project uses SQLite for development (configurable to MySQL/PostgreSQL for production). The database includes:

- **Users**: Django's built-in User model for authentication
- **Listings**: Property listings with detailed information
- **Bookings**: Reservation records linking users to listings
- **Reviews**: Rating and review system for completed bookings

## API Endpoints

The serializers are ready for use with Django REST Framework views. The project structure supports:

- Listing CRUD operations
- Booking management
- Review system
- User authentication and authorization

## Testing

The seeder command has been tested and verified to:
- Create realistic sample data
- Maintain referential integrity
- Handle various edge cases
- Support configurable data volumes

## Next Steps

This milestone provides the foundation for:
- API view implementation
- Authentication and authorization
- Frontend integration
- Advanced features like search and filtering