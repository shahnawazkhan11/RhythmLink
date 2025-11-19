// ============================================================================
// SEARCH API
// Autocomplete and typo-tolerant search
// ============================================================================

import { apiClient } from './client';

export interface SearchResult {
  type: 'event' | 'artist' | 'venue';
  id: number;
  title: string;
  subtitle: string;
  score: number;
  matched_field: string;
  url: string;
  price?: string;
}

export interface AutocompleteResponse {
  query: string;
  results: SearchResult[];
  count: number;
  message?: string;
  error?: string;
}

/**
 * Autocomplete search with typo tolerance
 * GET /api/search/autocomplete/?q={query}
 */
export async function autocompleteSearch(query: string): Promise<AutocompleteResponse> {
  return apiClient.get<AutocompleteResponse>(
    `/api/search/autocomplete/?q=${encodeURIComponent(query)}`
  );
}

export const searchAPI = {
  autocomplete: autocompleteSearch,
};
