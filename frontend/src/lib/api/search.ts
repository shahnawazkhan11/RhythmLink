// ============================================================================
// SEARCH API
// All search-related API calls
// ============================================================================

import { apiClient } from './client';
import type { SearchResult, PopularSearch } from '@/types/api';

// ============================================================================
// SEARCH & AUTOCOMPLETE
// ============================================================================

/**
 * Autocomplete search across events, artists, and venues
 * GET /api/search/autocomplete/?q={query}
 */
export async function autocomplete(query: string): Promise<SearchResult> {
  return apiClient.get<SearchResult>('/api/search/autocomplete/', { q: query });
}

/**
 * Get popular searches
 * GET /api/search/popular/?limit={number}
 */
export async function getPopularSearches(limit: number = 10): Promise<PopularSearch[]> {
  return apiClient.get<PopularSearch[]>('/api/search/popular/', { limit });
}

// ============================================================================
// SEARCH API OBJECT (ALTERNATIVE EXPORT)
// ============================================================================

export const searchAPI = {
  autocomplete,
  getPopularSearches,
};
