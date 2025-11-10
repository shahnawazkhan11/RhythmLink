// ============================================================================
// REGISTER FORM MODULE
// Complete registration form with validation and role selection
// ============================================================================

'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Select } from '@/components/ui/Select';
import { Alert } from '@/components/ui/Alert';
import {
  isValidEmail,
  isValidPassword,
  isValidUsername,
  isValidPhone,
  isValidDateOfBirth,
  isRequired,
} from '@/lib/utils/validators';
import Link from 'next/link';
import type { UserRole } from '@/types/api';

interface RegisterFormData {
  username: string;
  email: string;
  password: string;
  confirmPassword: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  phone: string;
  date_of_birth: string;
}

export function RegisterForm() {
  const router = useRouter();
  const { register, isLoading, error, clearError } = useAuth();
  
  const [formData, setFormData] = useState<RegisterFormData>({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    first_name: '',
    last_name: '',
    role: 'customer',
    phone: '',
    date_of_birth: '',
  });
  
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});
  const [showPasswordRequirements, setShowPasswordRequirements] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear field error when user starts typing
    if (formErrors[name]) {
      setFormErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
    
    // Clear API error
    if (error) {
      clearError();
    }
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    // Username validation
    const usernameValidation = isValidUsername(formData.username);
    if (!usernameValidation.isValid) {
      errors.username = usernameValidation.error!;
    }

    // Email validation
    const emailRequired = isRequired(formData.email, 'Email');
    if (!emailRequired.isValid) {
      errors.email = emailRequired.error!;
    } else if (!isValidEmail(formData.email)) {
      errors.email = 'Please enter a valid email address';
    }

    // Password validation
    const passwordValidation = isValidPassword(formData.password);
    if (!passwordValidation.isValid) {
      errors.password = passwordValidation.errors[0];
    }

    // Confirm password
    if (formData.password !== formData.confirmPassword) {
      errors.confirmPassword = 'Passwords do not match';
    }

    // First name
    const firstNameValidation = isRequired(formData.first_name, 'First name');
    if (!firstNameValidation.isValid) {
      errors.first_name = firstNameValidation.error!;
    }

    // Last name
    const lastNameValidation = isRequired(formData.last_name, 'Last name');
    if (!lastNameValidation.isValid) {
      errors.last_name = lastNameValidation.error!;
    }

    // Phone validation
    const phoneRequired = isRequired(formData.phone, 'Phone number');
    if (!phoneRequired.isValid) {
      errors.phone = phoneRequired.error!;
    } else if (!isValidPhone(formData.phone)) {
      errors.phone = 'Please enter a valid phone number';
    }

    // Date of birth validation
    const dobRequired = isRequired(formData.date_of_birth, 'Date of birth');
    if (!dobRequired.isValid) {
      errors.date_of_birth = dobRequired.error!;
    } else {
      const dobValidation = isValidDateOfBirth(formData.date_of_birth);
      if (!dobValidation.isValid) {
        errors.date_of_birth = dobValidation.error!;
      }
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      // Backend expects password2 instead of confirmPassword
      const { confirmPassword, ...registerData } = formData;
      const dataToSend = {
        ...registerData,
        password2: confirmPassword, // Add password2 for backend validation
      };
      await register(dataToSend);
      
      // Redirect based on user role
      if (formData.role === 'manager') {
        router.push('/manager');
      } else {
        router.push('/');
      }
    } catch (err) {
      // Error is already set in the store
      console.log('Registration failed:', err);
    }
  };

  const roleOptions = [
    { value: 'customer', label: 'Customer / Audience' },
    { value: 'manager', label: 'Event Manager' },
  ];

  return (
    <div className="w-full max-w-2xl">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Create Account
          </h1>
          <p className="text-gray-600">
            Join RhythmLink today
          </p>
        </div>

        {error && (
          <div className="mb-6">
            <Alert type="error" message={error} onClose={clearError} />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          {/* Role Selection */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
            <Select
              label="I am registering as"
              name="role"
              value={formData.role}
              onChange={handleChange}
              options={roleOptions}
              required
              disabled={isLoading}
            />
            <p className="mt-2 text-sm text-gray-600">
              {formData.role === 'manager' 
                ? 'As a manager, you can create and manage events, configure pricing, and view analytics.'
                : 'As a customer, you can browse events, buy tickets, and view your booking history.'}
            </p>
          </div>

          {/* Personal Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="First Name"
              name="first_name"
              type="text"
              value={formData.first_name}
              onChange={handleChange}
              error={formErrors.first_name}
              required
              autoComplete="given-name"
              placeholder="John"
              disabled={isLoading}
            />

            <Input
              label="Last Name"
              name="last_name"
              type="text"
              value={formData.last_name}
              onChange={handleChange}
              error={formErrors.last_name}
              required
              autoComplete="family-name"
              placeholder="Doe"
              disabled={isLoading}
            />
          </div>

          {/* Account Information */}
          <Input
            label="Username"
            name="username"
            type="text"
            value={formData.username}
            onChange={handleChange}
            error={formErrors.username}
            required
            autoComplete="username"
            placeholder="johndoe"
            helperText="3-30 characters, letters, numbers, and underscores only"
            disabled={isLoading}
          />

          <Input
            label="Email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            error={formErrors.email}
            required
            autoComplete="email"
            placeholder="john@example.com"
            disabled={isLoading}
          />

          {/* Contact Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Phone Number"
              name="phone"
              type="tel"
              value={formData.phone}
              onChange={handleChange}
              error={formErrors.phone}
              required
              autoComplete="tel"
              placeholder="+1 (555) 123-4567"
              disabled={isLoading}
            />

            <Input
              label="Date of Birth"
              name="date_of_birth"
              type="date"
              value={formData.date_of_birth}
              onChange={handleChange}
              error={formErrors.date_of_birth}
              required
              autoComplete="bday"
              disabled={isLoading}
              helperText="Must be at least 13 years old"
            />
          </div>

          {/* Password */}
          <Input
            label="Password"
            name="password"
            type="password"
            value={formData.password}
            onChange={handleChange}
            onFocus={() => setShowPasswordRequirements(true)}
            onBlur={() => setShowPasswordRequirements(false)}
            error={formErrors.password}
            required
            autoComplete="new-password"
            placeholder="Create a strong password"
            disabled={isLoading}
          />

          {showPasswordRequirements && (
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-3 text-sm">
              <p className="font-medium text-gray-700 mb-2">Password must contain:</p>
              <ul className="space-y-1 text-gray-600">
                <li className={formData.password.length >= 8 ? 'text-green-600' : ''}>
                  • At least 8 characters
                </li>
                <li className={/[A-Z]/.test(formData.password) ? 'text-green-600' : ''}>
                  • One uppercase letter
                </li>
                <li className={/[a-z]/.test(formData.password) ? 'text-green-600' : ''}>
                  • One lowercase letter
                </li>
                <li className={/[0-9]/.test(formData.password) ? 'text-green-600' : ''}>
                  • One number
                </li>
              </ul>
            </div>
          )}

          <Input
            label="Confirm Password"
            name="confirmPassword"
            type="password"
            value={formData.confirmPassword}
            onChange={handleChange}
            error={formErrors.confirmPassword}
            required
            autoComplete="new-password"
            placeholder="Re-enter your password"
            disabled={isLoading}
          />

          {/* Terms and Conditions */}
          <div className="flex items-start">
            <input
              type="checkbox"
              required
              className="w-4 h-4 mt-1 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              disabled={isLoading}
            />
            <label className="ml-2 text-sm text-gray-600">
              I agree to the{' '}
              <Link href="/terms" className="text-blue-600 hover:text-blue-700 font-medium">
                Terms and Conditions
              </Link>{' '}
              and{' '}
              <Link href="/privacy" className="text-blue-600 hover:text-blue-700 font-medium">
                Privacy Policy
              </Link>
            </label>
          </div>

          <Button
            type="submit"
            variant="primary"
            size="lg"
            className="w-full"
            isLoading={isLoading}
            disabled={isLoading}
          >
            Create Account
          </Button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link
              href="/login"
              className="text-blue-600 hover:text-blue-700 font-medium"
            >
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
