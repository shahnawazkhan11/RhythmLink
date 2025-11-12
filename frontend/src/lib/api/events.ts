// ============================================================================
// EVENTS API
// All events-related API calls
// ============================================================================

import { apiClient } from './client';
import type { Event, Venue, EventType, PaginatedResponse } from '@/types/api';

// ============================================================================
// EVENTS
// ============================================================================

/**
 * Get all events with optional filters
 * GET /api/events/events/
 */
export async function getEvents(params?: {
  page?: number;
  date?: string;
  venue?: number;
  is_active?: boolean;
  search?: string;
}): Promise<PaginatedResponse<Event>> {
  return apiClient.get<PaginatedResponse<Event>>('/api/events/events/', params);
}

/**
 * Get single event by ID
 * GET /api/events/events/{id}/
 */
export async function getEvent(id: number): Promise<Event> {
  return apiClient.get<Event>(`/api/events/events/${id}/`);
}

/**
 * Create new event
 * POST /api/events/events/
 */
export async function createEvent(data: FormData): Promise<Event> {
  return apiClient.post<Event>('/api/events/events/', data);
}

/**
 * Update event
 * PUT /api/events/events/{id}/
 */
export async function updateEvent(id: number, data: FormData): Promise<Event> {
  return apiClient.put<Event>(`/api/events/events/${id}/`, data);
}

/**
 * Partially update event
 * PATCH /api/events/events/{id}/
 */
export async function patchEvent(id: number, data: Partial<Event>): Promise<Event> {
  return apiClient.patch<Event>(`/api/events/events/${id}/`, data);
}

/**
 * Delete event
 * DELETE /api/events/events/{id}/
 */
export async function deleteEvent(id: number): Promise<void> {
  return apiClient.delete<void>(`/api/events/events/${id}/`);
}

// ============================================================================
// VENUES
// ============================================================================

/**
 * Get all venues
 * GET /api/events/venues/
 */
export async function getVenues(params?: {
  page?: number;
  search?: string;
  is_active?: boolean;
}): Promise<PaginatedResponse<Venue>> {
  return apiClient.get<PaginatedResponse<Venue>>('/api/events/venues/', params);
}

/**
 * Get single venue by ID
 * GET /api/events/venues/{id}/
 */
export async function getVenue(id: number): Promise<Venue> {
  return apiClient.get<Venue>(`/api/events/venues/${id}/`);
}

/**
 * Create new venue
 * POST /api/events/venues/
 */
export async function createVenue(data: Partial<Venue>): Promise<Venue> {
  return apiClient.post<Venue>('/api/events/venues/', data);
}

/**
 * Update venue
 * PUT /api/events/venues/{id}/
 */
export async function updateVenue(id: number, data: Partial<Venue>): Promise<Venue> {
  return apiClient.put<Venue>(`/api/events/venues/${id}/`, data);
}

/**
 * Delete venue
 * DELETE /api/events/venues/{id}/
 */
export async function deleteVenue(id: number): Promise<void> {
  return apiClient.delete<void>(`/api/events/venues/${id}/`);
}

// ============================================================================
// EVENT TYPES
// ============================================================================

/**
 * Get all event types
 * GET /api/events/event-types/
 */
export async function getEventTypes(): Promise<EventType[]> {
  return apiClient.get<EventType[]>('/api/events/event-types/');
}

/**
 * Get single event type by ID
 * GET /api/events/event-types/{id}/
 */
export async function getEventType(id: number): Promise<EventType> {
  return apiClient.get<EventType>(`/api/events/event-types/${id}/`);
}

/**
 * Create new event type
 * POST /api/events/event-types/
 */
export async function createEventType(data: { name: string; description?: string }): Promise<EventType> {
  return apiClient.post<EventType>('/api/events/event-types/', data);
}

// ============================================================================
// EVENTS API OBJECT (ALTERNATIVE EXPORT)
// ============================================================================

export const eventsAPI = {
  // Events
  getAll: getEvents,
  getById: getEvent,
  create: createEvent,
  update: updateEvent,
  patch: patchEvent,
  delete: deleteEvent,
  
  // Venues
  venues: {
    getAll: getVenues,
    getById: getVenue,
    create: createVenue,
    update: updateVenue,
    delete: deleteVenue,
  },
  
  // Event Types
  eventTypes: {
    getAll: getEventTypes,
    getById: getEventType,
    create: createEventType,
  },
};
