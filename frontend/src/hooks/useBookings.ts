// ============================================================================
// BOOKINGS HOOK
// Custom hook for managing bookings data
// ============================================================================

'use client';

import { useState, useEffect, useCallback } from 'react';
import { Booking } from '@/types/api';
import * as bookingsAPI from '@/lib/api/bookings';

export function useBookings() {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBookings = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await bookingsAPI.getMyBookings();
      setBookings(response.results);
      return response;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to fetch bookings';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchBookings();
  }, [fetchBookings]);

  return { bookings, loading, error, fetchBookings, setBookings };
}

export function useCreateBooking() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createBooking = useCallback(
    async (bookingData: {
      event: number;
      tickets: number[];
      total_amount: string;
      special_requests?: string;
    }) => {
      setLoading(true);
      setError(null);
      try {
        const data = await bookingsAPI.createBooking(bookingData);
        return data;
      } catch (err: any) {
        const errorMsg = err.message || 'Failed to create booking';
        setError(errorMsg);
        throw err;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  return { createBooking, loading, error };
}
