// ============================================================================
// USE AUTH HOOK
// Reusable authentication hook
// ============================================================================

'use client';

import { useAuthStore } from '@/store/authStore';
import { useRouter } from 'next/navigation';
import { useEffect } from 'react';

/**
 * Main authentication hook
 * Provides all auth state and actions
 */
export function useAuth() {
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    register,
    fetchProfile,
    clearError,
    getRole,
    isManager,
    isCustomer,
    isAdmin,
  } = useAuthStore();

  return {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    logout,
    register,
    fetchProfile,
    clearError,
    role: getRole(),
    isManager: isManager(),
    isCustomer: isCustomer(),
    isAdmin: isAdmin(),
  };
}

/**
 * Hook to require authentication
 * Redirects to login if not authenticated
 */
export function useRequireAuth(redirectTo: string = '/login') {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      router.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, router, redirectTo]);

  return { isAuthenticated, isLoading };
}

/**
 * Hook to require specific role
 * Redirects if user doesn't have required role
 */
export function useRequireRole(
  allowedRoles: ('manager' | 'customer' | 'admin')[],
  redirectTo: string = '/'
) {
  const { user, isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (!isAuthenticated) {
        router.push('/login');
      } else if (user && !allowedRoles.includes(user.role)) {
        router.push(redirectTo);
      }
    }
  }, [isAuthenticated, isLoading, user, allowedRoles, router, redirectTo]);

  return { user, isAuthenticated, isLoading };
}

/**
 * Hook to redirect if already authenticated
 * Useful for login/register pages
 */
export function useGuestOnly(redirectTo: string = '/') {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.push(redirectTo);
    }
  }, [isAuthenticated, isLoading, router, redirectTo]);

  return { isAuthenticated, isLoading };
}
