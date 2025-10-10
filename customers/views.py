from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class BookingCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # Placeholder for booking creation logic
        return render(request, 'customers/booking.html')


class CustomerBookingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Placeholder for customer bookings list
        return render(request, 'customers/bookings.html')