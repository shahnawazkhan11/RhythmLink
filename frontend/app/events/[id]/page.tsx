// ============================================================================
// EVENT DETAIL PAGE
// Display single event details with booking option
// ============================================================================

'use client';

import React from 'react';
import { useParams } from 'next/navigation';
import { BookTickets } from '@/modules/bookings/BookTickets';

export default function EventDetailPage() {
  const params = useParams();
  const eventId = parseInt(params.id as string);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <BookTickets eventId={eventId} />
      </div>
    </div>
  );
}
