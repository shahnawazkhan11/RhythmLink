// ============================================================================
// API CLIENT
// Reusable fetch wrapper following RhythmLink frontend guidelines
// NO AXIOS - using native fetch() only
// ============================================================================

import type { APIError } from '@/types/api';

// API Configuration
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Get CSRF token from cookies
 * Django uses 'csrftoken' cookie name by default
 */
function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null;
  
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  
  if (parts.length === 2) {
    return parts.pop()?.split(';').shift() || null;
  }
  
  return null;
}

/**
 * Handle API errors and format them consistently
 */
function handleAPIError(error: any): never {
  if (error.response) {
    // Server responded with error status
    const apiError: APIError = {
      message: error.response.detail || error.response.message || 'An error occurred',
      ...error.response,
    };
    throw apiError;
  } else if (error.request) {
    // Request made but no response
    throw {
      message: 'No response from server. Please check your connection.',
      error: 'NETWORK_ERROR',
    };
  } else {
    // Something else happened
    throw {
      message: error.message || 'An unexpected error occurred',
      error: 'UNKNOWN_ERROR',
    };
  }
}

// ============================================================================
// FETCH WRAPPER
// ============================================================================

interface FetchOptions extends RequestInit {
  data?: any;
  params?: Record<string, any>;
}

/**
 * Main fetch wrapper following RhythmLink guidelines
 * Handles CSRF tokens, authentication, and error handling
 */
async function fetchAPI<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { data, params, headers = {}, ...fetchOptions } = options;

  // Build URL with query parameters
  let url = `${API_BASE_URL}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value !== undefined && value !== null) {
        searchParams.append(key, String(value));
      }
    });
    const queryString = searchParams.toString();
    if (queryString) {
      url += `?${queryString}`;
    }
  }

  // Prepare headers
  const requestHeaders: Record<string, string> = {
    ...(headers as Record<string, string>),
  };

  // Add Content-Type for JSON data
  if (data && !(data instanceof FormData)) {
    requestHeaders['Content-Type'] = 'application/json';
  }

  // Add CSRF token for non-GET requests
  const method = fetchOptions.method?.toUpperCase() || 'GET';
  if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
    const csrfToken = getCookie('csrftoken');
    if (csrfToken) {
      requestHeaders['X-CSRFToken'] = csrfToken;
    }
  }

  // Prepare request body
  let body: string | FormData | undefined;
  if (data) {
    if (data instanceof FormData) {
      body = data;
    } else {
      body = JSON.stringify(data);
    }
  }

  try {
    // Make the request
    const response = await fetch(url, {
      ...fetchOptions,
      headers: requestHeaders,
      credentials: 'include', // Important for session-based auth
      body,
    });

    // Handle response
    const contentType = response.headers.get('content-type');
    let responseData: any;

    if (contentType?.includes('application/json')) {
      responseData = await response.json();
    } else {
      responseData = await response.text();
    }

    // Check if request was successful
    if (!response.ok) {
      throw {
        response: responseData,
        status: response.status,
        statusText: response.statusText,
      };
    }

    return responseData as T;
  } catch (error: any) {
    return handleAPIError(error);
  }
}

// ============================================================================
// HTTP METHOD HELPERS
// ============================================================================

export const apiClient = {
  /**
   * GET request
   */
  get: <T>(endpoint: string, params?: Record<string, any>) => {
    return fetchAPI<T>(endpoint, { method: 'GET', params });
  },

  /**
   * POST request
   */
  post: <T>(endpoint: string, data?: any, options: FetchOptions = {}) => {
    return fetchAPI<T>(endpoint, { method: 'POST', data, ...options });
  },

  /**
   * PUT request
   */
  put: <T>(endpoint: string, data?: any, options: FetchOptions = {}) => {
    return fetchAPI<T>(endpoint, { method: 'PUT', data, ...options });
  },

  /**
   * PATCH request
   */
  patch: <T>(endpoint: string, data?: any, options: FetchOptions = {}) => {
    return fetchAPI<T>(endpoint, { method: 'PATCH', data, ...options });
  },

  /**
   * DELETE request
   */
  delete: <T>(endpoint: string, data?: any) => {
    return fetchAPI<T>(endpoint, { method: 'DELETE', data });
  },
};

// ============================================================================
// ERROR HANDLING UTILITIES
// ============================================================================

/**
 * Check if error is an authentication error
 */
export function isAuthError(error: any): boolean {
  return error?.status === 401 || error?.status === 403;
}

/**
 * Get user-friendly error message
 */
export function getErrorMessage(error: any): string {
  if (typeof error === 'string') return error;
  
  if (error?.response?.detail) return error.response.detail;
  if (error?.response?.message) return error.response.message;
  if (error?.message) return error.message;
  
  // Handle validation errors (field-specific errors)
  if (error?.response && typeof error.response === 'object') {
    const firstError = Object.values(error.response)[0];
    if (Array.isArray(firstError)) {
      return firstError[0] as string;
    }
    if (typeof firstError === 'string') {
      return firstError;
    }
  }
  
  return 'An unexpected error occurred';
}

/**
 * Get field-specific validation errors
 */
export function getFieldErrors(error: any): Record<string, string> {
  const fieldErrors: Record<string, string> = {};
  
  if (error?.response && typeof error.response === 'object') {
    Object.entries(error.response).forEach(([field, messages]) => {
      if (Array.isArray(messages)) {
        fieldErrors[field] = messages[0];
      } else if (typeof messages === 'string') {
        fieldErrors[field] = messages;
      }
    });
  }
  
  return fieldErrors;
}
