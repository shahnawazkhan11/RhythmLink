// ============================================================================
// REGISTER PAGE
// Public registration page
// ============================================================================

'use client';

import { RegisterForm } from '@/modules/auth/RegisterForm';
import { useGuestOnly } from '@/hooks/useAuth';

export default function RegisterPage() {
  // Redirect if already authenticated
  useGuestOnly('/');

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4 py-12">
      <RegisterForm />
    </div>
  );
}
