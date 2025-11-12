// ============================================================================
// ANALYTICS API
// All analytics-related API calls
// ============================================================================

import { apiClient } from './client';
import type { EventAnalytics, ManagerDashboard } from '@/types/api';

// ============================================================================
// EVENT ANALYTICS
// ============================================================================

/**
 * Get analytics for a specific event
 * GET /api/analytics/dashboard/{event_id}/
 */
export async function getEventAnalytics(eventId: number): Promise<EventAnalytics> {
  return apiClient.get<EventAnalytics>(`/api/analytics/dashboard/${eventId}/`);
}

// ============================================================================
// MANAGER DASHBOARD
// ============================================================================

/**
 * Get manager dashboard data (requires manager role)
 * GET /api/analytics/manager-dashboard/
 */
export async function getManagerDashboard(): Promise<ManagerDashboard> {
  return apiClient.get<ManagerDashboard>('/api/analytics/manager-dashboard/');
}

// ============================================================================
// ANALYTICS API OBJECT (ALTERNATIVE EXPORT)
// ============================================================================

export const analyticsAPI = {
  getEventAnalytics,
  getManagerDashboard,
};
