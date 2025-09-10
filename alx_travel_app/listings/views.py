from django.shortcuts import render
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Listing, Booking, Review
from .serializers import ListingSerializer, BookingSerializer, BookingCreateSerializer, ReviewSerializer


# Create your views here.


class ListingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing listing instances.
    Provides full CRUD operations for property listings.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['property_type', 'is_available', 'bedrooms', 'bathrooms', 'host']
    search_fields = ['title', 'description', 'location', 'amenities']
    ordering_fields = ['price', 'created_at', 'updated_at', 'average_rating']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Set the host to the current user when creating a listing."""
        serializer.save(host=self.request.user)

    @action(detail=True, methods=['get'])
    def bookings(self, request, pk=None):
        """Get all bookings for a specific listing."""
        listing = self.get_object()
        bookings = listing.bookings.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        """Get all reviews for a specific listing."""
        listing = self.get_object()
        reviews = listing.reviews.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances.
    Provides full CRUD operations for property bookings.
    """
    queryset = Booking.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'guest', 'listing', 'check_in', 'check_out']
    search_fields = ['listing__title', 'listing__location', 'special_requests']
    ordering_fields = ['check_in', 'check_out', 'total_price', 'created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'create':
            return BookingCreateSerializer
        return BookingSerializer

    def perform_create(self, serializer):
        """Set the guest to the current user when creating a booking."""
        serializer.save(guest=self.request.user)

    def get_queryset(self):
        """Filter bookings based on user permissions."""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Users can see their own bookings and bookings for their listings
            return queryset.filter(
                Q(guest=self.request.user) | 
                Q(listing__host=self.request.user)
            )
        return queryset.none()

    @action(detail=True, methods=['patch'])
    def confirm(self, request, pk=None):
        """Confirm a booking (host only)."""
        booking = self.get_object()
        if booking.listing.host != request.user:
            return Response(
                {'error': 'Only the listing host can confirm bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        booking.status = 'confirmed'
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        """Cancel a booking."""
        booking = self.get_object()
        if booking.guest != request.user and booking.listing.host != request.user:
            return Response(
                {'error': 'Only the guest or host can cancel bookings.'},
                status=status.HTTP_403_FORBIDDEN
            )
        booking.status = 'cancelled'
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing review instances.
    Provides full CRUD operations for property reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['listing', 'guest', 'rating']
    search_fields = ['comment', 'listing__title']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        """Set the guest to the current user when creating a review."""
        serializer.save(guest=self.request.user)

    def get_queryset(self):
        """Filter reviews based on user permissions."""
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            # Users can see reviews for their listings or their own reviews
            return queryset.filter(
                Q(listing__host=self.request.user) | 
                Q(guest=self.request.user)
            )
        return queryset.none()
