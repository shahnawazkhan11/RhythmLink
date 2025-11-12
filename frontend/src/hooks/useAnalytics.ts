// ============================================================================
// ANALYTICS HOOK
// Custom hook for analytics and dashboard data
// ============================================================================

'use client';

import { useState, useEffect, useCallback } from 'react';
import { EventAnalytics, ManagerDashboard } from '@/types/api';
import * as analyticsAPI from '@/lib/api/analytics';

export function useManagerDashboard() {
  const [dashboard, setDashboard] = useState<ManagerDashboard | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboard = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsAPI.getManagerDashboard();
      setDashboard(data);
      return data;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to fetch dashboard data';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return { dashboard, loading, error, fetchDashboard };
}

export function useEventAnalytics(eventId: number) {
  const [analytics, setAnalytics] = useState<EventAnalytics | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = useCallback(async () => {
    if (!eventId) return;
    setLoading(true);
    setError(null);
    try {
      const data = await analyticsAPI.getEventAnalytics(eventId);
      setAnalytics(data);
      return data;
    } catch (err: any) {
      const errorMsg = err.message || 'Failed to fetch event analytics';
      setError(errorMsg);
      throw err;
    } finally {
      setLoading(false);
    }
  }, [eventId]);

  useEffect(() => {
    if (eventId) {
      fetchAnalytics();
    }
  }, [eventId, fetchAnalytics]);

  return { analytics, loading, error, fetchAnalytics };
}
