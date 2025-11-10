// ============================================================================
// AUTHENTICATION API
// All authentication-related API calls
// ============================================================================

import { apiClient } from './client';
import type {
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  UserWithProfile,
} from '@/types/api';

// ============================================================================
// AUTHENTICATION ENDPOINTS
// ============================================================================

/**
 * Register a new user
 * POST /api/accounts/register/
 */
export async function register(data: RegisterRequest): Promise<UserWithProfile> {
  return apiClient.post<UserWithProfile>('/api/accounts/register/', data);
}

/**
 * Login user
 * POST /api/accounts/login/
 */
export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  return apiClient.post<LoginResponse>('/api/accounts/login/', credentials);
}

/**
 * Logout user
 * POST /api/accounts/logout/
 */
export async function logout(): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>('/api/accounts/logout/');
}

/**
 * Get current user profile
 * GET /api/accounts/profile/
 */
export async function getProfile(): Promise<UserWithProfile> {
  return apiClient.get<UserWithProfile>('/api/accounts/profile/');
}

/**
 * Update user profile
 * PATCH /api/accounts/profile/
 */
export async function updateProfile(data: Partial<UserWithProfile>): Promise<UserWithProfile> {
  return apiClient.patch<UserWithProfile>('/api/accounts/profile/', data);
}

/**
 * Change password
 * POST /api/accounts/change-password/
 */
export async function changePassword(data: {
  old_password: string;
  new_password: string;
}): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>('/api/accounts/change-password/', data);
}

/**
 * Request password reset
 * POST /api/accounts/password-reset/
 */
export async function requestPasswordReset(email: string): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>('/api/accounts/password-reset/', { email });
}

/**
 * Confirm password reset
 * POST /api/accounts/password-reset-confirm/
 */
export async function confirmPasswordReset(data: {
  token: string;
  new_password: string;
}): Promise<{ message: string }> {
  return apiClient.post<{ message: string }>('/api/accounts/password-reset-confirm/', data);
}

// ============================================================================
// AUTH API OBJECT (ALTERNATIVE EXPORT PATTERN)
// ============================================================================

export const authAPI = {
  register,
  login,
  logout,
  getProfile,
  updateProfile,
  changePassword,
  requestPasswordReset,
  confirmPasswordReset,
};
