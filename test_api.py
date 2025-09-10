#!/usr/bin/env python3
"""
Test script for ALX Travel App API
This script demonstrates how to test the API endpoints using requests.
"""

import requests
import json
from datetime import datetime, timedelta
import base64

# Configuration
BASE_URL = "http://localhost:8000/api"
ADMIN_USERNAME = "admin"  # Change this to your admin username
ADMIN_PASSWORD = "admin"  # Change this to your admin password

def get_auth_header():
    """Get authentication header for API requests."""
    credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()
    return {"Authorization": f"Basic {encoded_credentials}"}

def test_listings():
    """Test listing endpoints."""
    print("=== Testing Listings ===")
    
    # Test GET /api/listings/
    print("1. Testing GET /api/listings/")
    response = requests.get(f"{BASE_URL}/listings/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test POST /api/listings/
    print("2. Testing POST /api/listings/")
    listing_data = {
        "title": "Beautiful Apartment in Downtown",
        "description": "A modern apartment with great city views and all amenities",
        "price": "150.00",
        "location": "Downtown City",
        "property_type": "apartment",
        "bedrooms": 2,
        "bathrooms": 1,
        "max_guests": 4,
        "amenities": "WiFi, Air Conditioning, Kitchen, Parking"
    }
    
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"
    
    response = requests.post(f"{BASE_URL}/listings/", 
                           headers=headers, 
                           data=json.dumps(listing_data))
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        listing = response.json()
        print(f"Created listing: {listing['id']}")
        return listing['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_bookings(listing_id):
    """Test booking endpoints."""
    print("\n=== Testing Bookings ===")
    
    if not listing_id:
        print("No listing ID available, skipping booking tests")
        return None
    
    # Test POST /api/bookings/
    print("1. Testing POST /api/bookings/")
    check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    booking_data = {
        "listing": listing_id,
        "check_in": check_in,
        "check_out": check_out,
        "total_price": "450.00",
        "special_requests": "Late check-in requested"
    }
    
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"
    
    response = requests.post(f"{BASE_URL}/bookings/", 
                           headers=headers, 
                           data=json.dumps(booking_data))
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        booking = response.json()
        print(f"Created booking: {booking['id']}")
        return booking['id']
    else:
        print(f"Error: {response.text}")
        return None

def test_reviews(listing_id, booking_id):
    """Test review endpoints."""
    print("\n=== Testing Reviews ===")
    
    if not listing_id or not booking_id:
        print("No listing or booking ID available, skipping review tests")
        return
    
    # Test POST /api/reviews/
    print("1. Testing POST /api/reviews/")
    review_data = {
        "listing": listing_id,
        "booking": booking_id,
        "rating": 5,
        "comment": "Excellent stay! The apartment was clean, modern, and perfectly located. Highly recommended!"
    }
    
    headers = get_auth_header()
    headers["Content-Type"] = "application/json"
    
    response = requests.post(f"{BASE_URL}/reviews/", 
                           headers=headers, 
                           data=json.dumps(review_data))
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        review = response.json()
        print(f"Created review: {review['id']}")
    else:
        print(f"Error: {response.text}")

def test_filtering():
    """Test filtering and search functionality."""
    print("\n=== Testing Filtering and Search ===")
    
    # Test filtering listings by property type
    print("1. Testing filter by property_type=apartment")
    response = requests.get(f"{BASE_URL}/listings/?property_type=apartment")
    print(f"Status: {response.status_code}")
    print(f"Filtered results: {len(response.json()['results'])} apartments found")
    
    # Test search functionality
    print("\n2. Testing search by title")
    response = requests.get(f"{BASE_URL}/listings/?search=apartment")
    print(f"Status: {response.status_code}")
    print(f"Search results: {len(response.json()['results'])} listings found")
    
    # Test ordering
    print("\n3. Testing ordering by price")
    response = requests.get(f"{BASE_URL}/listings/?ordering=price")
    print(f"Status: {response.status_code}")
    if response.json()['results']:
        print(f"First listing price: ${response.json()['results'][0]['price']}")

def test_custom_actions(listing_id, booking_id):
    """Test custom actions like confirm and cancel bookings."""
    print("\n=== Testing Custom Actions ===")
    
    if not booking_id:
        print("No booking ID available, skipping custom action tests")
        return
    
    headers = get_auth_header()
    
    # Test confirm booking
    print("1. Testing confirm booking")
    response = requests.patch(f"{BASE_URL}/bookings/{booking_id}/confirm/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Booking confirmed successfully")
    else:
        print(f"Error: {response.text}")
    
    # Test cancel booking
    print("\n2. Testing cancel booking")
    response = requests.patch(f"{BASE_URL}/bookings/{booking_id}/cancel/", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Booking cancelled successfully")
    else:
        print(f"Error: {response.text}")

def main():
    """Main test function."""
    print("ALX Travel App API Test Script")
    print("=" * 40)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/listings/")
        print(f"Server is running. Status: {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server.")
        print("Make sure the Django server is running on http://localhost:8000")
        return
    
    # Run tests
    listing_id = test_listings()
    booking_id = test_bookings(listing_id)
    test_reviews(listing_id, booking_id)
    test_filtering()
    test_custom_actions(listing_id, booking_id)
    
    print("\n" + "=" * 40)
    print("Test completed!")
    print("\nTo view the API documentation, visit:")
    print("http://localhost:8000/swagger/")

if __name__ == "__main__":
    main()
