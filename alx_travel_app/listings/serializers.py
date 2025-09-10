from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ReviewSerializer(serializers.ModelSerializer):
    """Serializer for Review model."""
    guest = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'guest', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class ListingSerializer(serializers.ModelSerializer):
    """Serializer for the Listing model."""
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'price', 'location', 'property_type',
            'bedrooms', 'bathrooms', 'max_guests', 'amenities', 'is_available',
            'host', 'reviews', 'average_rating', 'review_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'host']
    
    def get_average_rating(self, obj):
        """Calculate average rating for the listing."""
        reviews = obj.reviews.all()
        if reviews:
            return round(sum(review.rating for review in reviews) / len(reviews), 2)
        return 0
    
    def get_review_count(self, obj):
        """Get total number of reviews for the listing."""
        return obj.reviews.count()


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for the Booking model."""
    listing = ListingSerializer(read_only=True)
    guest = UserSerializer(read_only=True)
    listing_id = serializers.IntegerField(write_only=True)
    guest_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'guest', 'listing_id', 'guest_id',
            'check_in', 'check_out', 'total_price', 'status',
            'special_requests', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate booking data."""
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data


class BookingCreateSerializer(serializers.ModelSerializer):
    """Simplified serializer for creating bookings."""
    
    class Meta:
        model = Booking
        fields = [
            'listing', 'guest', 'check_in', 'check_out', 
            'total_price', 'special_requests'
        ]
    
    def validate(self, data):
        """Validate booking data."""
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return data 