// ============================================================================
// CUSTOMER DASHBOARD PAGE
// Main dashboard for customers to view bookings and discover events
// ============================================================================

'use client';

import React from 'react';
import { useRequireRole } from '@/hooks/useAuth';
import { useBookings } from '@/hooks/useBookings';
import { useEvents } from '@/hooks/useEvents';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';
import { EventCard } from '@/components/features/EventCard';
import { BookingCard } from '@/components/features/BookingCard';
import { Skeleton, SkeletonCard } from '@/components/ui/Skeleton';
import { NoBookingsFound, NoEventsFound } from '@/components/ui/EmptyState';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

export default function CustomerDashboardPage() {
  // Require customer role
  useRequireRole(['customer']);

  const router = useRouter();
  const { user } = useAuth();
  const { bookings, loading: bookingsLoading } = useBookings();
  const { events, loading: eventsLoading, fetchEvents } = useEvents();

  // Fetch featured events on mount
  React.useEffect(() => {
    fetchEvents({ is_active: true });
  }, [fetchEvents]);

  const upcomingBookings = bookings.filter(
    (b) => b.status === 'confirmed' || b.status === 'pending'
  );
  const pastBookings = bookings.filter((b) => b.status === 'cancelled' || b.status === 'refunded');

  if (bookingsLoading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Skeleton variant="text" className="w-64 mb-6" height={32} />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back, {user?.first_name || 'Customer'}!
        </h1>
        <p className="text-gray-600">Manage your bookings and discover new events</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Upcoming Bookings</div>
            <div className="text-2xl font-bold text-blue-600">{upcomingBookings.length}</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Total Bookings</div>
            <div className="text-2xl font-bold text-gray-900">{bookings.length}</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Events Attended</div>
            <div className="text-2xl font-bold text-green-600">{pastBookings.length}</div>
          </CardBody>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultTab="bookings">
        <TabsList>
          <TabsTrigger value="bookings">My Bookings</TabsTrigger>
          <TabsTrigger value="discover">Discover Events</TabsTrigger>
          <TabsTrigger value="history">History</TabsTrigger>
        </TabsList>

        {/* Bookings Tab */}
        <TabsContent value="bookings">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {upcomingBookings.length > 0 ? (
              upcomingBookings.map((booking) => (
                <BookingCard
                  key={booking.id}
                  booking={booking}
                  onView={(id) => router.push(`/bookings/${id}`)}
                  onCancel={(id) => {
                    // Handle cancellation
                    console.log('Cancel booking', id);
                  }}
                />
              ))
            ) : (
              <div className="col-span-full">
                <NoBookingsFound />
              </div>
            )}
          </div>
        </TabsContent>

        {/* Discover Events Tab */}
        <TabsContent value="discover">
          {eventsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[...Array(6)].map((_, i) => (
                <SkeletonCard key={i} />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {events.length > 0 ? (
                events.slice(0, 9).map((event) => (
                  <EventCard
                    key={event.id}
                    event={event}
                    onView={(id) => router.push(`/events/${id}`)}
                    onBook={(id) => router.push(`/events/${id}/book`)}
                  />
                ))
              ) : (
                <div className="col-span-full">
                  <NoEventsFound />
                </div>
              )}
            </div>
          )}
        </TabsContent>

        {/* History Tab */}
        <TabsContent value="history">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pastBookings.length > 0 ? (
              pastBookings.map((booking) => (
                <BookingCard
                  key={booking.id}
                  booking={booking}
                  onView={(id) => router.push(`/bookings/${id}`)}
                  showActions={false}
                />
              ))
            ) : (
              <div className="col-span-full">
                <Card>
                  <CardBody>
                    <p className="text-gray-500 text-center py-8">No booking history yet</p>
                  </CardBody>
                </Card>
              </div>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
}
