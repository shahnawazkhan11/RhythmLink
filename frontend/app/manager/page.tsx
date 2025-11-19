// ============================================================================
// MANAGER DASHBOARD PAGE
// Main dashboard for managers to view analytics and manage events
// ============================================================================

'use client';

import React from 'react';
import { useRequireRole } from '@/hooks/useAuth';
import { useManagerDashboard } from '@/hooks/useAnalytics';
import { Card, CardHeader, CardBody } from '@/components/ui/Card';
import { Tabs, TabsList, TabsTrigger, TabsContent } from '@/components/ui/Tabs';
import { EventCard } from '@/components/features/EventCard';
import { BookingCard } from '@/components/features/BookingCard';
import { Skeleton, SkeletonCard } from '@/components/ui/Skeleton';
import { formatCurrency } from '@/lib/utils/formatters';
import { useRouter } from 'next/navigation';

export default function ManagerDashboardPage() {
  // Require manager role
  useRequireRole(['manager']);

  const router = useRouter();
  const { dashboard, loading, error } = useManagerDashboard();

  if (loading) {
    return (
      <div className="container mx-auto px-4 py-8">
        <Skeleton variant="text" className="w-64 mb-6" height={32} />
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          {[...Array(4)].map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
        <SkeletonCard />
      </div>
    );
  }

  if (error || !dashboard) {
    return (
      <div className="container mx-auto px-4 py-8">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">
            {error || 'Failed to load dashboard data'}
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8 flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Manager Dashboard</h1>
          <p className="text-gray-600">Manage your events and view analytics</p>
        </div>
        <button
          onClick={() => router.push('/manager/events/create')}
          className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
        >
          + Create Event
        </button>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Total Events</div>
            <div className="text-2xl font-bold text-gray-900">{dashboard.total_events}</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Active Events</div>
            <div className="text-2xl font-bold text-green-600">{dashboard.active_events}</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Total Bookings</div>
            <div className="text-2xl font-bold text-blue-600">{dashboard.total_bookings}</div>
          </CardBody>
        </Card>

        <Card>
          <CardBody>
            <div className="text-sm text-gray-600 mb-1">Total Revenue</div>
            <div className="text-2xl font-bold text-purple-600">
              {formatCurrency(parseFloat(dashboard.total_revenue))}
            </div>
          </CardBody>
        </Card>
      </div>

      {/* Tabs */}
      <Tabs defaultTab="overview">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="events">Upcoming Events</TabsTrigger>
          <TabsTrigger value="bookings">Recent Bookings</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Top Performing Events */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold">Top Performing Events</h3>
              </CardHeader>
              <CardBody>
                {dashboard.top_performing_events && dashboard.top_performing_events.length > 0 ? (
                  <div className="space-y-3">
                    {dashboard.top_performing_events.slice(0, 5).map((item) => (
                      <div
                        key={item.event.id}
                        className="flex justify-between items-center p-3 bg-gray-50 rounded-lg cursor-pointer hover:bg-gray-100"
                        onClick={() => router.push(`/events/${item.event.id}`)}
                      >
                        <div>
                          <div className="font-medium text-gray-900">{item.event.name}</div>
                          <div className="text-sm text-gray-600">
                            {item.tickets_sold} tickets sold
                          </div>
                        </div>
                        <div className="text-right">
                          <div className="font-semibold text-green-600">
                            {formatCurrency(parseFloat(item.revenue))}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">No events yet</p>
                )}
              </CardBody>
            </Card>

            {/* Revenue Trend */}
            <Card>
              <CardHeader>
                <h3 className="text-lg font-semibold">Revenue Trend</h3>
              </CardHeader>
              <CardBody>
                {dashboard.revenue_trend && dashboard.revenue_trend.length > 0 ? (
                  <div className="space-y-2">
                    {dashboard.revenue_trend.slice(-7).map((item) => (
                      <div key={item.date} className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">{item.date}</span>
                        <span className="font-medium text-gray-900">
                          {formatCurrency(parseFloat(item.revenue))}
                        </span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-500 text-center py-8">No revenue data yet</p>
                )}
              </CardBody>
            </Card>
          </div>
        </TabsContent>

        {/* Upcoming Events Tab */}
        <TabsContent value="events">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dashboard.upcoming_events && dashboard.upcoming_events.length > 0 ? (
              dashboard.upcoming_events.map((event) => (
                <EventCard
                  key={event.id}
                  event={event}
                  onView={(id) => router.push(`/events/${id}`)}
                />
              ))
            ) : (
              <div className="col-span-full">
                <p className="text-gray-500 text-center py-8">No upcoming events</p>
              </div>
            )}
          </div>
        </TabsContent>

        {/* Recent Bookings Tab */}
        <TabsContent value="bookings">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {dashboard.recent_bookings && dashboard.recent_bookings.length > 0 ? (
              dashboard.recent_bookings.map((booking) => (
                <BookingCard key={booking.id} booking={booking} showActions={false} />
              ))
            ) : (
              <div className="col-span-full">
                <p className="text-gray-500 text-center py-8">No recent bookings</p>
              </div>
            )}
          </div>
        </TabsContent>

        {/* Analytics Tab */}
        <TabsContent value="analytics">
          <Card>
            <CardBody>
              <p className="text-gray-500 text-center py-8">
                Advanced analytics coming soon...
              </p>
            </CardBody>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
