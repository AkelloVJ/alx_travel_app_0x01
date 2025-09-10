# ALX Travel App API

A comprehensive Django REST Framework API for managing property listings, bookings, and reviews. This project provides full CRUD operations for a travel booking platform similar to Airbnb.

## Features

- **Property Listings Management**: Create, read, update, and delete property listings
- **Booking System**: Handle property reservations with status management
- **Review System**: Allow guests to rate and review properties
- **User Authentication**: Secure API with user-based permissions
- **Advanced Filtering**: Search and filter listings, bookings, and reviews
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **RESTful Design**: Follows REST conventions for clean API design

## API Endpoints

### Listings
- `GET /api/listings/` - List all property listings
- `POST /api/listings/` - Create a new listing (authenticated users only)
- `GET /api/listings/{id}/` - Retrieve a specific listing
- `PUT /api/listings/{id}/` - Update a listing (host only)
- `PATCH /api/listings/{id}/` - Partially update a listing (host only)
- `DELETE /api/listings/{id}/` - Delete a listing (host only)
- `GET /api/listings/{id}/bookings/` - Get bookings for a specific listing
- `GET /api/listings/{id}/reviews/` - Get reviews for a specific listing

### Bookings
- `GET /api/bookings/` - List user's bookings (own bookings + host's listing bookings)
- `POST /api/bookings/` - Create a new booking (authenticated users only)
- `GET /api/bookings/{id}/` - Retrieve a specific booking
- `PUT /api/bookings/{id}/` - Update a booking (guest or host only)
- `PATCH /api/bookings/{id}/` - Partially update a booking (guest or host only)
- `DELETE /api/bookings/{id}/` - Delete a booking (guest or host only)
- `PATCH /api/bookings/{id}/confirm/` - Confirm a booking (host only)
- `PATCH /api/bookings/{id}/cancel/` - Cancel a booking (guest or host only)

### Reviews
- `GET /api/reviews/` - List reviews (own reviews + reviews for user's listings)
- `POST /api/reviews/` - Create a new review (authenticated users only)
- `GET /api/reviews/{id}/` - Retrieve a specific review
- `PUT /api/reviews/{id}/` - Update a review (author only)
- `PATCH /api/reviews/{id}/` - Partially update a review (author only)
- `DELETE /api/reviews/{id}/` - Delete a review (author only)

## Filtering and Search

### Listings
- **Filter by**: `property_type`, `is_available`, `bedrooms`, `bathrooms`, `host`
- **Search in**: `title`, `description`, `location`, `amenities`
- **Order by**: `price`, `created_at`, `updated_at`, `average_rating`

### Bookings
- **Filter by**: `status`, `guest`, `listing`, `check_in`, `check_out`
- **Search in**: `listing__title`, `listing__location`, `special_requests`
- **Order by**: `check_in`, `check_out`, `total_price`, `created_at`

### Reviews
- **Filter by**: `listing`, `guest`, `rating`
- **Search in**: `comment`, `listing__title`
- **Order by**: `rating`, `created_at`

## Authentication

The API uses Django's built-in authentication system:
- **Session Authentication**: For web interface
- **Basic Authentication**: For API testing

## Permissions

- **Listings**: Read-only for anonymous users, full access for authenticated users
- **Bookings**: Requires authentication, users can only see their own bookings and bookings for their listings
- **Reviews**: Requires authentication, users can only see their own reviews and reviews for their listings

## API Documentation

Interactive API documentation is available at:
- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **JSON Schema**: `http://localhost:8000/swagger.json`
- **YAML Schema**: `http://localhost:8000/swagger.yaml`

## Installation and Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd alx_travel_app_0x01
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirement.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create superuser** (optional):
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

7. **Access the API**:
   - API Base URL: `http://localhost:8000/api/`
   - Admin Panel: `http://localhost:8000/admin/`
   - API Documentation: `http://localhost:8000/swagger/`

## Testing the API

### Using curl

#### Create a Listing
```bash
curl -X POST http://localhost:8000/api/listings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "title": "Beautiful Apartment in Downtown",
    "description": "A modern apartment with great city views",
    "price": "150.00",
    "location": "Downtown City",
    "property_type": "apartment",
    "bedrooms": 2,
    "bathrooms": 1,
    "max_guests": 4,
    "amenities": "WiFi, Air Conditioning, Kitchen"
  }'
```

#### Create a Booking
```bash
curl -X POST http://localhost:8000/api/bookings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "listing": 1,
    "check_in": "2024-02-01",
    "check_out": "2024-02-05",
    "total_price": "600.00",
    "special_requests": "Late check-in requested"
  }'
```

#### Create a Review
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic <base64-encoded-credentials>" \
  -d '{
    "listing": 1,
    "booking": 1,
    "rating": 5,
    "comment": "Excellent stay! Highly recommended."
  }'
```

### Using Postman

1. Import the API collection (if available)
2. Set up authentication in Postman
3. Test all CRUD operations for each endpoint
4. Verify filtering and search functionality

## Data Models

### Listing
- `title`: Property title
- `description`: Detailed description
- `price`: Price per night
- `location`: Property location
- `property_type`: Type of property (apartment, house, etc.)
- `bedrooms`: Number of bedrooms
- `bathrooms`: Number of bathrooms
- `max_guests`: Maximum number of guests
- `amenities`: Available amenities
- `is_available`: Availability status
- `host`: Property host (User)

### Booking
- `listing`: Associated property
- `guest`: Booking guest (User)
- `check_in`: Check-in date
- `check_out`: Check-out date
- `total_price`: Total booking price
- `status`: Booking status (pending, confirmed, cancelled, completed)
- `special_requests`: Special requests from guest

### Review
- `listing`: Reviewed property
- `guest`: Review author (User)
- `booking`: Associated booking
- `rating`: Rating (1-5 stars)
- `comment`: Review comment

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.