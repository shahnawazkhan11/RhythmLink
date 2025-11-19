// ============================================================================
// BOOK TICKETS MODULE
// Component for customers to book tickets for an event
// ============================================================================

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Alert';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { bookingsAPI } from '@/lib/api/bookings';
import { eventsAPI } from '@/lib/api/events';
import { getErrorMessage } from '@/lib/api/client';
import { formatCurrency, formatDate, formatTime } from '@/lib/utils/formatters';
import type { Event, Ticket } from '@/types/api';

interface BookTicketsProps {
  eventId: number;
}

export function BookTickets({ eventId }: BookTicketsProps) {
  const router = useRouter();
  const { isAuthenticated, user } = useAuth();
  const [event, setEvent] = useState<Event | null>(null);
  const [availableTickets, setAvailableTickets] = useState<Ticket[]>([]);
  const [selectedTickets, setSelectedTickets] = useState<number[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [isBooking, setIsBooking] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  // Load event and available tickets
  useEffect(() => {
    const loadData = async () => {
      try {
        const [eventData, ticketsData] = await Promise.all([
          eventsAPI.getById(eventId),
          bookingsAPI.tickets.getAvailable(eventId),
        ]);
        setEvent(eventData);
        setAvailableTickets(ticketsData);
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, [eventId]);

  const handleTicketToggle = (ticketId: number) => {
    setSelectedTickets(prev => {
      if (prev.includes(ticketId)) {
        return prev.filter(id => id !== ticketId);
      }
      
      // Check max tickets per customer limit
      if (event && prev.length >= event.max_tickets_per_customer) {
        setError(`You can only book up to ${event.max_tickets_per_customer} tickets per event`);
        return prev;
      }
      
      return [...prev, ticketId];
    });
    setError(null);
  };

  const calculateTotal = () => {
    return selectedTickets.reduce((total, ticketId) => {
      const ticket = availableTickets.find(t => t.id === ticketId);
      return total + (ticket ? parseFloat(ticket.price) : 0);
    }, 0);
  };

  const handleBooking = async () => {
    if (!isAuthenticated) {
      router.push(`/login?redirect=/events/${eventId}`);
      return;
    }

    if (selectedTickets.length === 0) {
      setError('Please select at least one ticket');
      return;
    }

    setIsBooking(true);
    setError(null);

    try {
      await bookingsAPI.create({
        event: eventId,
        tickets: selectedTickets,
        total_amount: calculateTotal().toFixed(2),
      });
      
      setSuccess(true);
      setTimeout(() => {
        router.push('/user/bookings');
      }, 2000);
    } catch (err: any) {
      setError(getErrorMessage(err));
    } finally {
      setIsBooking(false);
    }
  };

  if (isLoading) {
    return (
      <div className="text-center py-8">
        <div className="text-gray-600">Loading tickets...</div>
      </div>
    );
  }

  if (!event) {
    return (
      <div className="text-center py-8">
        <Alert type="error" message="Event not found" />
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      {/* Event Info */}
      <Card className="mb-6">
        <CardHeader>
          <h2 className="text-2xl font-bold text-gray-900">{event.name}</h2>
        </CardHeader>
        <CardBody>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-gray-600">Date</p>
              <p className="font-medium">{formatDate(event.date)}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Time</p>
              <p className="font-medium">
                {formatTime(event.start_time)} - {formatTime(event.end_time)}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Venue</p>
              <p className="font-medium">{event.venue_name}</p>
            </div>
            <div>
              <p className="text-sm text-gray-600">Price</p>
              <p className="font-medium text-blue-600">{formatCurrency(parseFloat(event.ticket_price))}</p>
            </div>
          </div>
          {event.description && (
            <div className="mt-4">
              <p className="text-sm text-gray-600">Description</p>
              <p className="text-gray-700">{event.description}</p>
            </div>
          )}
        </CardBody>
      </Card>

      {/* Alerts */}
      {error && (
        <div className="mb-6">
          <Alert type="error" message={error} onClose={() => setError(null)} />
        </div>
      )}

      {success && (
        <div className="mb-6">
          <Alert type="success" message="Booking successful! Redirecting to your bookings..." />
        </div>
      )}

      {/* Available Tickets */}
      <Card className="mb-6">
        <CardHeader>
          <h3 className="text-xl font-semibold">Available Tickets</h3>
          <p className="text-sm text-gray-600 mt-1">
            {availableTickets.length} tickets available • Max {event.max_tickets_per_customer} per customer
          </p>
        </CardHeader>
        <CardBody>
          {availableTickets.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-500">No tickets available for this event</p>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {availableTickets.slice(0, 20).map((ticket) => (
                <button
                  key={ticket.id}
                  onClick={() => handleTicketToggle(ticket.id)}
                  disabled={isBooking || success}
                  className={`
                    p-4 rounded-lg border-2 transition-all
                    ${selectedTickets.includes(ticket.id)
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-blue-300'
                    }
                    ${isBooking || success ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
                  `}
                >
                  <div className="text-sm font-medium text-gray-900">
                    {ticket.seat_number || `Ticket #${ticket.id}`}
                  </div>
                  <div className="text-xs text-gray-600 mt-1">
                    {formatCurrency(parseFloat(ticket.price))}
                  </div>
                </button>
              ))}
            </div>
          )}
          
          {availableTickets.length > 20 && (
            <p className="text-sm text-gray-500 mt-4 text-center">
              Showing 20 of {availableTickets.length} available tickets
            </p>
          )}
        </CardBody>
      </Card>

      {/* Booking Summary */}
      {selectedTickets.length > 0 && (
        <Card className="mb-6">
          <CardHeader>
            <h3 className="text-xl font-semibold">Booking Summary</h3>
          </CardHeader>
          <CardBody>
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Tickets Selected:</span>
                <span className="font-medium">{selectedTickets.length}</span>
              </div>
              <div className="flex justify-between text-lg font-bold">
                <span>Total Amount:</span>
                <span className="text-blue-600">{formatCurrency(calculateTotal())}</span>
              </div>
            </div>
          </CardBody>
        </Card>
      )}

      {/* Action Buttons */}
      <div className="flex gap-4">
        <Button
          variant="primary"
          size="lg"
          className="flex-1"
          onClick={handleBooking}
          isLoading={isBooking}
          disabled={isBooking || success || selectedTickets.length === 0 || availableTickets.length === 0}
        >
          {!isAuthenticated ? 'Login to Book' : 'Confirm Booking'}
        </Button>
        
        <Button
          variant="secondary"
          size="lg"
          onClick={() => router.back()}
          disabled={isBooking}
        >
          Cancel
        </Button>
      </div>
    </div>
  );
}
