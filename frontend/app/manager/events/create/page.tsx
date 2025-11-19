// ============================================================================
// CREATE EVENT PAGE
// Page for managers to create new events
// ============================================================================

'use client';

import React from 'react';
import { useRequireRole } from '@/hooks/useAuth';
import { CreateEventForm } from '@/modules/events/CreateEventForm';

export default function CreateEventPage() {
  // Require manager role
  useRequireRole(['manager', 'admin']);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="container mx-auto px-4">
        <CreateEventForm />
      </div>
    </div>
  );
}
