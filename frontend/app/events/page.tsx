// ============================================================================
// EVENTS LIST PAGE
// Browse all events with search and filters
// ============================================================================

'use client';

import React, { useState, useEffect } from 'react';
import { useEvents } from '@/hooks/useEvents';
import { EventCard } from '@/components/features/EventCard';
import { SearchBar } from '@/components/ui/SearchBar';
import { Pagination } from '@/components/ui/Pagination';
import { SkeletonCard } from '@/components/ui/Skeleton';
import { NoEventsFound } from '@/components/ui/EmptyState';
import { useRouter } from 'next/navigation';

export default function EventsPage() {
  const router = useRouter();
  const { events, loading, error, fetchEvents } = useEvents();
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showAll, setShowAll] = useState(false);

  useEffect(() => {
    const loadEvents = async () => {
      try {
        const params: any = {
          page: currentPage,
        };
        
        // Only add search if it has value
        if (searchQuery && searchQuery.trim()) {
          params.search = searchQuery.trim();
        }
        
        // Filter by active unless "show all" is toggled
        if (!showAll) {
          params.is_active = true;
        }
        
        const response = await fetchEvents(params);
        // Calculate total pages (assuming 20 items per page from backend)
        if (response.count) {
          setTotalPages(Math.ceil(response.count / 20));
        }
      } catch (err) {
        console.error('Failed to load events:', err);
      }
    };

    loadEvents();
  }, [currentPage, searchQuery, showAll]);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    setCurrentPage(1); // Reset to first page on new search
  };

  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <div className="mb-8 flex justify-between items-start">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Discover Events</h1>
          <p className="text-gray-600">Find and book tickets for upcoming events</p>
        </div>
        <button
          onClick={() => setShowAll(!showAll)}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
            showAll
              ? 'bg-blue-600 text-white hover:bg-blue-700'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          {showAll ? 'Show Active Only' : 'Show All Events'}
        </button>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <SearchBar
          value={searchQuery}
          onChange={setSearchQuery}
          onSearch={handleSearch}
          placeholder="Search events by name, venue, or type..."
          className="max-w-2xl"
        />
      </div>

      {/* Error State */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Events Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[...Array(6)].map((_, i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      ) : events.length > 0 ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
            {events.map((event) => (
              <EventCard
                key={event.id}
                event={event}
                onView={(id) => router.push(`/events/${id}`)}
              />
            ))}
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <Pagination
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          )}
        </>
      ) : (
        <NoEventsFound />
      )}
    </div>
  );
}
