from django.shortcuts import render, get_object_or_404
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction
from .models import Booking, Customer, Ticket, Feedback
from events.models import Event


class BookingCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Get or create customer profile
            customer, created = Customer.objects.get_or_create(user=request.user)
            
            # Extract booking data
            event_id = request.data.get('event')
            ticket_ids = request.data.get('tickets', [])
            total_amount = request.data.get('total_amount')
            special_requests = request.data.get('special_requests', '')
            
            # Validate
            if not event_id or not ticket_ids:
                return Response(
                    {'error': 'Event and tickets are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            event = get_object_or_404(Event, id=event_id)
            
            # Create booking in transaction
            with transaction.atomic():
                # Create booking
                booking = Booking.objects.create(
                    customer=customer,
                    event=event,
                    total_amount=total_amount,
                    status='confirmed',
                    special_requests=special_requests
                )
                
                # Update tickets and add to booking
                tickets = Ticket.objects.filter(id__in=ticket_ids, status='available')
                if tickets.count() != len(ticket_ids):
                    raise Exception('Some tickets are no longer available')
                
                tickets.update(status='booked')
                booking.tickets.set(tickets)
                
                return Response({
                    'id': booking.id,
                    'customer': customer.id,
                    'event': event.id,
                    'event_name': event.name,
                    'tickets': list(ticket_ids),
                    'total_amount': str(booking.total_amount),
                    'booking_date': booking.booking_date,
                    'status': booking.status,
                    'special_requests': booking.special_requests
                }, status=status.HTTP_201_CREATED)
                
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomerBookingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            customer = Customer.objects.get(user=request.user)
            bookings = Booking.objects.filter(customer=customer).order_by('-booking_date')
            
            results = []
            for booking in bookings:
                results.append({
                    'id': booking.id,
                    'customer': customer.id,
                    'customer_name': request.user.get_full_name() or request.user.username,
                    'event': booking.event.id,
                    'event_name': booking.event.name,
                    'event_details': {
                        'id': booking.event.id,
                        'name': booking.event.name,
                        'date': booking.event.date,
                        'start_time': booking.event.start_time,
                        'end_time': booking.event.end_time,
                        'venue_name': booking.event.venue.name,
                    },
                    'tickets': [ticket.id for ticket in booking.tickets.all()],
                    'total_amount': str(booking.total_amount),
                    'booking_date': booking.booking_date,
                    'status': booking.status,
                    'payment_reference': booking.payment_reference,
                    'special_requests': booking.special_requests,
                })
            
            return Response({'results': results})
            
        except Customer.DoesNotExist:
            return Response({'results': []})


class TicketListView(generics.ListAPIView):
    """Get available tickets for an event"""
    
    def get(self, request):
        event_id = request.query_params.get('event')
        ticket_status = request.query_params.get('status', 'available')
        
        if not event_id:
            return Response(
                {'error': 'Event ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        tickets = Ticket.objects.filter(event_id=event_id, status=ticket_status)
        
        results = []
        for ticket in tickets:
            results.append({
                'id': ticket.id,
                'event': ticket.event.id,
                'event_name': ticket.event.name,
                'seat_number': ticket.seat_number,
                'section': ticket.section,
                'price': str(ticket.final_price),
                'status': ticket.status,
            })
        
        return Response(results)


class BookingDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(user=request.user)
            booking = get_object_or_404(Booking, id=pk, customer=customer)
            
            return Response({
                'id': booking.id,
                'customer': customer.id,
                'event': booking.event.id,
                'event_name': booking.event.name,
                'tickets': [ticket.id for ticket in booking.tickets.all()],
                'total_amount': str(booking.total_amount),
                'booking_date': booking.booking_date,
                'status': booking.status,
                'payment_reference': booking.payment_reference,
                'special_requests': booking.special_requests,
            })
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def patch(self, request, pk):
        try:
            customer = Customer.objects.get(user=request.user)
            booking = get_object_or_404(Booking, id=pk, customer=customer)
            
            # Allow cancellation
            if 'status' in request.data and request.data['status'] == 'cancelled':
                booking.status = 'cancelled'
                # Release tickets
                booking.tickets.update(status='available')
                booking.save()
                
                return Response({
                    'id': booking.id,
                    'status': booking.status,
                    'message': 'Booking cancelled successfully'
                })
            
            return Response(
                {'error': 'Invalid update'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Customer.DoesNotExist:
            return Response(
                {'error': 'Customer profile not found'},
                status=status.HTTP_404_NOT_FOUND
            )