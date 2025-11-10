// ============================================================================
// LOGIN PAGE
// Public login page
// ============================================================================

'use client';

import { LoginForm } from '@/modules/auth/LoginForm';
import { useGuestOnly } from '@/hooks/useAuth';

export default function LoginPage() {
  // Redirect if already authenticated
  useGuestOnly('/');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <LoginForm />
    </div>
  );
}
