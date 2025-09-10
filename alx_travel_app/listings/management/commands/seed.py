from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random
from decimal import Decimal
from listings.models import Listing, Booking, Review


class Command(BaseCommand):
    help = 'Seed the database with sample data for listings, bookings, and reviews'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Number of users to create (default: 10)',
        )
        parser.add_argument(
            '--listings',
            type=int,
            default=20,
            help='Number of listings to create (default: 20)',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Review.objects.all().delete()
            Booking.objects.all().delete()
            Listing.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Existing data cleared.'))

        # Create users
        self.stdout.write('Creating users...')
        users = self.create_users(options['users'])
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users.'))

        # Create listings
        self.stdout.write('Creating listings...')
        listings = self.create_listings(options['listings'], users)
        self.stdout.write(self.style.SUCCESS(f'Created {len(listings)} listings.'))

        # Create bookings
        self.stdout.write('Creating bookings...')
        bookings = self.create_bookings(listings, users)
        self.stdout.write(self.style.SUCCESS(f'Created {len(bookings)} bookings.'))

        # Create reviews
        self.stdout.write('Creating reviews...')
        reviews = self.create_reviews(bookings)
        self.stdout.write(self.style.SUCCESS(f'Created {len(reviews)} reviews.'))

        self.stdout.write(
            self.style.SUCCESS('Database seeding completed successfully!')
        )

    def create_users(self, count):
        """Create sample users."""
        users = []
        first_names = [
            'John', 'Jane', 'Mike', 'Sarah', 'David', 'Lisa', 'Chris', 'Emma',
            'Alex', 'Maria', 'Tom', 'Anna', 'James', 'Sophie', 'Robert', 'Lucy'
        ]
        last_names = [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller',
            'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez',
            'Wilson', 'Anderson', 'Thomas'
        ]

        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            username = f"{first_name.lower()}{last_name.lower()}{i}"
            email = f"{username}@example.com"
            
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='password123'
            )
            users.append(user)

        return users

    def create_listings(self, count, users):
        """Create sample listings."""
        listings = []
        property_types = ['apartment', 'house', 'condo', 'villa', 'studio']
        
        locations = [
            'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
            'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
            'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
            'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC', 'San Francisco, CA',
            'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC'
        ]

        titles = [
            'Cozy Apartment in Downtown', 'Beautiful House with Garden',
            'Modern Condo with City View', 'Luxury Villa by the Beach',
            'Charming Studio in Historic District', 'Spacious Family Home',
            'Elegant Apartment with Balcony', 'Rustic Cabin in the Woods',
            'Contemporary Loft', 'Traditional House with Pool',
            'Penthouse with Panoramic Views', 'Cottage by the Lake',
            'Urban Apartment Near Metro', 'Mountain Retreat',
            'Beachfront Condo', 'Historic Brownstone',
            'Modern Townhouse', 'Garden Apartment',
            'Luxury Penthouse', 'Cozy Bungalow'
        ]

        descriptions = [
            'A beautiful and comfortable space perfect for your stay.',
            'Modern amenities and stunning views await you here.',
            'Experience luxury and comfort in this amazing property.',
            'Perfect location with easy access to all attractions.',
            'A home away from home with all the comforts you need.',
            'Stunning architecture and thoughtful design throughout.',
            'Prime location with excellent transportation links.',
            'Peaceful retreat in the heart of the city.',
            'Spacious and well-appointed for your perfect getaway.',
            'Charming property with character and modern conveniences.'
        ]

        amenities_list = [
            'WiFi, Air Conditioning, Kitchen, Parking',
            'WiFi, Pool, Gym, Balcony',
            'WiFi, Hot Tub, Fireplace, Garden',
            'WiFi, Air Conditioning, Kitchen, Washer',
            'WiFi, Pool, Gym, Balcony, Parking',
            'WiFi, Hot Tub, Fireplace, Garden, Pool',
            'WiFi, Air Conditioning, Kitchen, Balcony',
            'WiFi, Pool, Gym, Parking, Washer',
            'WiFi, Hot Tub, Fireplace, Garden, Pool, Gym',
            'WiFi, Air Conditioning, Kitchen, Balcony, Parking'
        ]

        for i in range(count):
            listing = Listing.objects.create(
                title=random.choice(titles),
                description=random.choice(descriptions),
                price=Decimal(random.uniform(50, 500)).quantize(Decimal('0.01')),
                location=random.choice(locations),
                property_type=random.choice(property_types),
                bedrooms=random.randint(1, 5),
                bathrooms=random.randint(1, 3),
                max_guests=random.randint(1, 8),
                amenities=random.choice(amenities_list),
                is_available=random.choice([True, True, True, False]),  # 75% available
                host=random.choice(users)
            )
            listings.append(listing)

        return listings

    def create_bookings(self, listings, users):
        """Create sample bookings."""
        bookings = []
        statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        status_weights = [0.1, 0.6, 0.25, 0.05]  # Weighted distribution

        for _ in range(random.randint(15, 30)):  # Random number of bookings
            listing = random.choice(listings)
            guest = random.choice(users)
            
            # Generate random dates
            start_date = timezone.now().date() + timedelta(days=random.randint(-30, 60))
            end_date = start_date + timedelta(days=random.randint(1, 14))
            
            # Calculate total price
            nights = (end_date - start_date).days
            total_price = listing.price * nights
            
            special_requests = random.choice([
                '', 'Late check-in requested', 'Early check-in if possible',
                'Quiet hours please', 'Extra towels needed', '',
                'Pet-friendly accommodation', 'Wheelchair accessible needed', ''
            ])

            booking = Booking.objects.create(
                listing=listing,
                guest=guest,
                check_in=start_date,
                check_out=end_date,
                total_price=total_price,
                status=random.choices(statuses, weights=status_weights)[0],
                special_requests=special_requests
            )
            bookings.append(booking)

        return bookings

    def create_reviews(self, bookings):
        """Create sample reviews."""
        reviews = []
        comments = [
            'Excellent stay! Highly recommended.',
            'Great location and very clean.',
            'Perfect for our family vacation.',
            'Beautiful property with amazing views.',
            'Host was very responsive and helpful.',
            'Would definitely stay here again.',
            'Clean, comfortable, and well-equipped.',
            'Great value for money.',
            'Lovely place with character.',
            'Perfect location for exploring the city.',
            'Amazing amenities and great service.',
            'Very comfortable and spacious.',
            'Host went above and beyond.',
            'Beautiful property, highly recommend.',
            'Great experience overall.',
            'Clean, modern, and well-maintained.',
            'Perfect for a weekend getaway.',
            'Excellent communication from host.',
            'Lovely place with great atmosphere.',
            'Would book again in a heartbeat.'
        ]

        # Only create reviews for completed bookings
        completed_bookings = [b for b in bookings if b.status == 'completed']
        
        for booking in completed_bookings[:len(completed_bookings)//2]:  # Review half of completed bookings
            review = Review.objects.create(
                listing=booking.listing,
                guest=booking.guest,
                booking=booking,
                rating=random.randint(3, 5),  # Mostly positive reviews
                comment=random.choice(comments)
            )
            reviews.append(review)

        return reviews
