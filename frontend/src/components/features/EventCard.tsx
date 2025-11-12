// ============================================================================
// EVENT CARD COMPONENT
// Display event information in card format
// ============================================================================

'use client';

import React from 'react';
import { Card, CardHeader, CardBody, CardFooter } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { Event } from '@/types/api';
import { formatDate, formatCurrency } from '@/lib/utils/formatters';

interface EventCardProps {
  event: Event;
  onView?: (id: number) => void;
  onBook?: (id: number) => void;
  showActions?: boolean;
  className?: string;
}

export function EventCard({
  event,
  onView,
  onBook,
  showActions = true,
  className = '',
}: EventCardProps) {
  const eventDateTime = `${event.date} ${event.start_time}`;
  const isActive = event.is_active;

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex justify-between items-start">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">{event.name}</h3>
            <p className="text-sm text-gray-500">{event.venue_name || 'Venue'}</p>
          </div>
          <Badge variant={isActive ? 'success' : 'danger'}>
            {isActive ? 'Active' : 'Inactive'}
          </Badge>
        </div>
      </CardHeader>

      <CardBody>
        {event.description && (
          <p className="text-sm text-gray-700 mb-4 line-clamp-3">{event.description}</p>
        )}

        <div className="space-y-2">
          <div className="flex items-center text-sm text-gray-600">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
              />
            </svg>
            <span>{formatDate(eventDateTime)}</span>
          </div>

          <div className="flex items-center text-sm text-gray-600">
            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span>
              {event.start_time} - {event.end_time}
            </span>
          </div>

          {event.event_type_name && (
            <div className="flex items-center text-sm text-gray-600">
              <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"
                />
              </svg>
              <span>{event.event_type_name}</span>
            </div>
          )}

          {event.ticket_price && (
            <div className="text-lg font-semibold text-blue-600 mt-2">
              {formatCurrency(parseFloat(event.ticket_price))}
            </div>
          )}
        </div>
      </CardBody>

      {showActions && (
        <CardFooter>
          <div className="flex space-x-2">
            {onView && (
              <Button variant="secondary" onClick={() => onView(event.id)} className="flex-1">
                View Details
              </Button>
            )}
            {onBook && isActive && (
              <Button variant="primary" onClick={() => onBook(event.id)} className="flex-1">
                Book Now
              </Button>
            )}
          </div>
        </CardFooter>
      )}
    </Card>
  );
}
