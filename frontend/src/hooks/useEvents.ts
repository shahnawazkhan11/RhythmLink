// ============================================================================
// EVENTS HOOK
// Custom hook for managing events data
// ============================================================================

'use client';

import { useState, useEffect, useCallback } from 'react';
import { Event, PaginatedResponse } from '@/types/api';
import * as eventsAPI from '@/lib/api/events';

export function useEvents() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEvents = useCallback(async (params?: Record<string, any>) => {
    setLoading(true);
    setError(null);
    try {
      const response = await eventsAPI.getEvents(params);
      setEvents(response.results);
      return response;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to fetch events';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { events, loading, error, fetchEvents, setEvents };
}

export function useEvent(id: number) {
  const [event, setEvent] = useState<Event | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchEvent = useCallback(async () => {
    if (!id) return;
    setLoading(true);
    setError(null);
    try {
      const data = await eventsAPI.getEvent(id);
      setEvent(data);
      return data;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to fetch event';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [id]);

  useEffect(() => {
    if (id) {
      fetchEvent();
    }
  }, [id, fetchEvent]);

  return { event, loading, error, fetchEvent, setEvent };
}

export function useCreateEvent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const createEvent = useCallback(async (eventData: FormData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await eventsAPI.createEvent(eventData);
      return data;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to create event';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { createEvent, loading, error };
}

export function useUpdateEvent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateEvent = useCallback(async (id: number, eventData: FormData) => {
    setLoading(true);
    setError(null);
    try {
      const data = await eventsAPI.updateEvent(id, eventData);
      return data;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to update event';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { updateEvent, loading, error };
}

export function useDeleteEvent() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const deleteEvent = useCallback(async (id: number) => {
    setLoading(true);
    setError(null);
    try {
      await eventsAPI.deleteEvent(id);
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to delete event';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  return { deleteEvent, loading, error };
}
