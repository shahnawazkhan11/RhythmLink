// ============================================================================
// MY BOOKINGS PAGE
// User's booking history
// ============================================================================

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useRequireAuth } from '@/hooks/useAuth';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Alert } from '@/components/ui/Alert';
import { bookingsAPI } from '@/lib/api/bookings';
import { getErrorMessage } from '@/lib/api/client';
import { formatCurrency, formatDate, formatTime } from '@/lib/utils/formatters';
import type { Booking } from '@/types/api';

export default function MyBookingsPage() {
  useRequireAuth();
  
  const router = useRouter();
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadBookings();
  }, []);

  const loadBookings = async () => {
    try {
      const response = await bookingsAPI.getMyBookings();
      setBookings(response.results || response as any);
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelBooking = async (bookingId: number) => {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
      await bookingsAPI.cancel(bookingId);
      await loadBookings();
    } catch (err) {
      setError(getErrorMessage(err));
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'confirmed':
        return 'bg-green-100 text-green-800';
      case 'pending':
        return 'bg-yellow-100 text-yellow-800';
      case 'cancelled':
        return 'bg-red-100 text-red-800';
      case 'refunded':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 py-8">
        <div className="container mx-auto px-4">
          <div className="text-center py-12">
            <div className="text-gray-600">Loading your bookings...</div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">My Bookings</h1>
          <p className="text-gray-600">View and manage your event bookings</p>
        </div>

        {error && (
          <div className="mb-6">
            <Alert type="error" message={error} onClose={() => setError(null)} />
          </div>
        )}

        {bookings.length === 0 ? (
          <Card>
            <CardBody>
              <div className="text-center py-12">
                <p className="text-gray-500 mb-4">You don't have any bookings yet</p>
                <Button
                  variant="primary"
                  onClick={() => router.push('/events')}
                >
                  Browse Events
                </Button>
              </div>
            </CardBody>
          </Card>
        ) : (
          <div className="grid grid-cols-1 gap-6">
            {bookings.map((booking) => (
              <Card key={booking.id}>
                <CardBody>
                  <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-4">
                    <div className="flex-1">
                      <div className="flex items-start justify-between mb-2">
                        <h3 className="text-xl font-semibold text-gray-900">
                          {booking.event_details?.name || `Event #${booking.event}`}
                        </h3>
                        <span className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(booking.status)}`}>
                          {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
                        </span>
                      </div>
                      
                      {booking.event_details && (
                        <div className="space-y-1 text-sm text-gray-600 mb-4">
                          <p>
                            <span className="font-medium">Date:</span>{' '}
                            {formatDate(booking.event_details.date)}
                          </p>
                          <p>
                            <span className="font-medium">Time:</span>{' '}
                            {formatTime(booking.event_details.start_time)} - {formatTime(booking.event_details.end_time)}
                          </p>
                          <p>
                            <span className="font-medium">Venue:</span>{' '}
                            {booking.event_details.venue_name}
                          </p>
                        </div>
                      )}

                      <div className="flex items-center gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Tickets:</span>{' '}
                          <span className="font-medium">{booking.tickets.length}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Total:</span>{' '}
                          <span className="font-medium text-blue-600">
                            {formatCurrency(parseFloat(booking.total_amount))}
                          </span>
                        </div>
                        <div>
                          <span className="text-gray-600">Booked:</span>{' '}
                          <span className="font-medium">
                            {formatDate(booking.booking_date)}
                          </span>
                        </div>
                      </div>

                      {booking.payment_reference && (
                        <div className="mt-2 text-xs text-gray-500">
                          Payment Reference: {booking.payment_reference}
                        </div>
                      )}

                      {booking.special_requests && (
                        <div className="mt-3 p-3 bg-gray-50 rounded">
                          <p className="text-xs text-gray-600 mb-1">Special Requests:</p>
                          <p className="text-sm text-gray-700">{booking.special_requests}</p>
                        </div>
                      )}
                    </div>

                    <div className="flex md:flex-col gap-2">
                      <Button
                        variant="secondary"
                        size="sm"
                        onClick={() => router.push(`/events/${booking.event}`)}
                      >
                        View Event
                      </Button>
                      
                      {booking.status === 'confirmed' && (
                        <Button
                          variant="danger"
                          size="sm"
                          onClick={() => handleCancelBooking(booking.id)}
                        >
                          Cancel
                        </Button>
                      )}
                    </div>
                  </div>
                </CardBody>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
