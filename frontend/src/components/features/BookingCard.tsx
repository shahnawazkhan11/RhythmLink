// ============================================================================
// BOOKING CARD COMPONENT
// Display booking information
// ============================================================================

'use client';

import React from 'react';
import { Card, CardHeader, CardBody, CardFooter } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { Booking } from '@/types/api';
import { formatDate, formatCurrency } from '@/lib/utils/formatters';

interface BookingCardProps {
  booking: Booking;
  onView?: (id: number) => void;
  onCancel?: (id: number) => void;
  showActions?: boolean;
  className?: string;
}

export function BookingCard({
  booking,
  onView,
  onCancel,
  showActions = true,
  className = '',
}: BookingCardProps) {
  const statusVariant = {
    pending: 'warning' as const,
    confirmed: 'success' as const,
    cancelled: 'danger' as const,
    refunded: 'info' as const,
  };

  const canCancel = booking.status === 'pending' || booking.status === 'confirmed';

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {booking.event_details?.name || booking.event_name || 'Event'}
            </h3>
            <p className="text-sm text-gray-500">
              Booking #{booking.id} • {formatDate(booking.booking_date)}
            </p>
          </div>
          <Badge variant={statusVariant[booking.status]}>
            {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
          </Badge>
        </div>
      </CardHeader>

      <CardBody>
        <div className="space-y-2">
          {booking.event_details && (
            <>
              <div className="flex items-center text-sm text-gray-600">
                <svg
                  className="w-4 h-4 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
                  />
                </svg>
                <span>
                  {formatDate(`${booking.event_details.date} ${booking.event_details.start_time}`)}
                </span>
              </div>

              <div className="flex items-center text-sm text-gray-600">
                <svg
                  className="w-4 h-4 mr-2"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                  />
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                  />
                </svg>
                <span>{booking.event_details.venue_name || 'Venue'}</span>
              </div>
            </>
          )}

          <div className="flex items-center text-sm text-gray-600">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M15 5v2m0 4v2m0 4v2M5 5a2 2 0 00-2 2v3a2 2 0 110 4v3a2 2 0 002 2h14a2 2 0 002-2v-3a2 2 0 110-4V7a2 2 0 00-2-2H5z"
              />
            </svg>
            <span>
              {booking.ticket_details?.length || booking.tickets.length} ticket
              {(booking.ticket_details?.length || booking.tickets.length) !== 1 ? 's' : ''}
            </span>
          </div>

          {booking.payment_reference && (
            <div className="flex items-center text-sm text-gray-600">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z"
                />
              </svg>
              <span className="text-xs">Ref: {booking.payment_reference}</span>
            </div>
          )}

          <div className="text-lg font-semibold text-blue-600 mt-3">
            Total: {formatCurrency(parseFloat(booking.total_amount))}
          </div>
        </div>
      </CardBody>

      {showActions && (
        <CardFooter>
          <div className="flex space-x-2">
            {onView && (
              <Button variant="secondary" onClick={() => onView(booking.id)} className="flex-1">
                View Details
              </Button>
            )}
            {onCancel && canCancel && (
              <Button variant="danger" onClick={() => onCancel(booking.id)} className="flex-1">
                Cancel Booking
              </Button>
            )}
          </div>
        </CardFooter>
      )}
    </Card>
  );
}
