// ============================================================================
// BOOKINGS API
// All bookings-related API calls
// ============================================================================

import { apiClient } from './client';
import type { Booking, BookingRequest, Ticket, Feedback, PaginatedResponse } from '@/types/api';

// ============================================================================
// BOOKINGS
// ============================================================================

/**
 * Create a new booking
 * POST /api/customers/book/
 */
export async function createBooking(data: BookingRequest): Promise<Booking> {
  return apiClient.post<Booking>('/api/customers/book/', data);
}

/**
 * Get my bookings (authenticated user)
 * GET /api/customers/my-bookings/
 */
export async function getMyBookings(params?: {
  page?: number;
  status?: 'pending' | 'confirmed' | 'cancelled' | 'refunded';
}): Promise<PaginatedResponse<Booking>> {
  return apiClient.get<PaginatedResponse<Booking>>('/api/customers/my-bookings/', params);
}

/**
 * Get single booking by ID
 * GET /api/customers/bookings/{id}/
 */
export async function getBooking(id: number): Promise<Booking> {
  return apiClient.get<Booking>(`/api/customers/bookings/${id}/`);
}

/**
 * Cancel a booking
 * PATCH /api/customers/bookings/{id}/
 */
export async function cancelBooking(id: number): Promise<Booking> {
  return apiClient.patch<Booking>(`/api/customers/bookings/${id}/`, {
    status: 'cancelled',
  });
}

/**
 * Update booking
 * PATCH /api/customers/bookings/{id}/
 */
export async function updateBooking(id: number, data: Partial<Booking>): Promise<Booking> {
  return apiClient.patch<Booking>(`/api/customers/bookings/${id}/`, data);
}

// ============================================================================
// TICKETS
// ============================================================================

/**
 * Get available tickets for an event
 * GET /api/customers/tickets/?event={event_id}
 */
export async function getAvailableTickets(eventId: number): Promise<Ticket[]> {
  return apiClient.get<Ticket[]>('/api/customers/tickets/', { event: eventId, status: 'available' });
}

/**
 * Get ticket by ID
 * GET /api/customers/tickets/{id}/
 */
export async function getTicket(id: number): Promise<Ticket> {
  return apiClient.get<Ticket>(`/api/customers/tickets/${id}/`);
}

// ============================================================================
// FEEDBACK
// ============================================================================

/**
 * Create feedback for an event
 * POST /api/customers/feedback/
 */
export async function createFeedback(data: {
  event: number;
  rating: number;
  comment?: string;
}): Promise<Feedback> {
  return apiClient.post<Feedback>('/api/customers/feedback/', data);
}

/**
 * Get my feedback
 * GET /api/customers/my-feedback/
 */
export async function getMyFeedback(params?: {
  page?: number;
}): Promise<PaginatedResponse<Feedback>> {
  return apiClient.get<PaginatedResponse<Feedback>>('/api/customers/my-feedback/', params);
}

/**
 * Get feedback for an event
 * GET /api/customers/feedback/?event={event_id}
 */
export async function getEventFeedback(eventId: number, params?: {
  page?: number;
}): Promise<PaginatedResponse<Feedback>> {
  return apiClient.get<PaginatedResponse<Feedback>>('/api/customers/feedback/', {
    event: eventId,
    ...params,
  });
}

/**
 * Update feedback
 * PATCH /api/customers/feedback/{id}/
 */
export async function updateFeedback(id: number, data: Partial<Feedback>): Promise<Feedback> {
  return apiClient.patch<Feedback>(`/api/customers/feedback/${id}/`, data);
}

/**
 * Delete feedback
 * DELETE /api/customers/feedback/{id}/
 */
export async function deleteFeedback(id: number): Promise<void> {
  return apiClient.delete<void>(`/api/customers/feedback/${id}/`);
}

// ============================================================================
// BOOKINGS API OBJECT (ALTERNATIVE EXPORT)
// ============================================================================

export const bookingsAPI = {
  // Bookings
  create: createBooking,
  getMyBookings,
  getById: getBooking,
  cancel: cancelBooking,
  update: updateBooking,
  
  // Tickets
  tickets: {
    getAvailable: getAvailableTickets,
    getById: getTicket,
  },
  
  // Feedback
  feedback: {
    create: createFeedback,
    getMy: getMyFeedback,
    getForEvent: getEventFeedback,
    update: updateFeedback,
    delete: deleteFeedback,
  },
};
