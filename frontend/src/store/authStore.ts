// ============================================================================
// AUTHENTICATION STORE
// Zustand store for managing authentication state
// NOTE: Run `pnpm install zustand` before using this file
// ============================================================================

import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import type { UserWithProfile, UserRole } from '@/types/api';
import { authAPI } from '@/lib/api/auth';
import { getErrorMessage } from '@/lib/api/client';

// ============================================================================
// TYPES
// ============================================================================

interface AuthState {
  // State
  user: UserWithProfile | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;

  // Actions
  setUser: (user: UserWithProfile | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  register: (data: any) => Promise<void>;
  fetchProfile: () => Promise<void>;
  clearError: () => void;
  
  // Computed
  getRole: () => UserRole | null;
  isManager: () => boolean;
  isCustomer: () => boolean;
  isAdmin: () => boolean;
}

// ============================================================================
// STORE
// ============================================================================

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      // Initial State
      user: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      // Setters
      setUser: (user) => {
        set({
          user,
          isAuthenticated: !!user,
          error: null,
        });
      },

      setLoading: (loading) => {
        set({ isLoading: loading });
      },

      setError: (error) => {
        set({ error });
      },

      clearError: () => {
        set({ error: null });
      },

      // Login Action
      login: async (username, password) => {
        set({ isLoading: true, error: null });
        try {
          const response = await authAPI.login({ username, password });
          set({
            user: response.user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage = getErrorMessage(error);
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          throw error;
        }
      },

      // Logout Action
      logout: async () => {
        set({ isLoading: true, error: null });
        try {
          await authAPI.logout();
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          // Even if logout fails, clear local state
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      },

      // Register Action
      register: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const user = await authAPI.register(data);
          // After successful registration, auto-login by setting user
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage = getErrorMessage(error);
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          throw error;
        }
      },

      // Fetch Profile Action
      fetchProfile: async () => {
        set({ isLoading: true, error: null });
        try {
          const user = await authAPI.getProfile();
          set({
            user,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          const errorMessage = getErrorMessage(error);
          set({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: errorMessage,
          });
          throw error;
        }
      },

      // Computed Properties
      getRole: () => {
        const { user } = get();
        return user?.role || null;
      },

      isManager: () => {
        return get().getRole() === 'manager';
      },

      isCustomer: () => {
        return get().getRole() === 'customer';
      },

      isAdmin: () => {
        return get().getRole() === 'admin';
      },
    }),
    {
      name: 'rhythmlink-auth-storage',
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        user: state.user,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
);

// ============================================================================
// SELECTORS (for performance optimization)
// ============================================================================

export const selectUser = (state: AuthState) => state.user;
export const selectIsAuthenticated = (state: AuthState) => state.isAuthenticated;
export const selectIsLoading = (state: AuthState) => state.isLoading;
export const selectError = (state: AuthState) => state.error;
export const selectUserRole = (state: AuthState) => state.getRole();
