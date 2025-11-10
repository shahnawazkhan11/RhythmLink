// ============================================================================
// VALIDATORS
// Form validation utilities
// ============================================================================

/**
 * Validate email format
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validate password strength
 * Requirements: At least 8 characters, 1 uppercase, 1 lowercase, 1 number
 */
export function isValidPassword(password: string): {
  isValid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push('Password must be at least 8 characters long');
  }

  if (!/[A-Z]/.test(password)) {
    errors.push('Password must contain at least one uppercase letter');
  }

  if (!/[a-z]/.test(password)) {
    errors.push('Password must contain at least one lowercase letter');
  }

  if (!/[0-9]/.test(password)) {
    errors.push('Password must contain at least one number');
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}

/**
 * Validate username
 * Requirements: 3-30 characters, alphanumeric and underscores only
 */
export function isValidUsername(username: string): {
  isValid: boolean;
  error?: string;
} {
  if (username.length < 3) {
    return { isValid: false, error: 'Username must be at least 3 characters long' };
  }

  if (username.length > 30) {
    return { isValid: false, error: 'Username must be at most 30 characters long' };
  }

  if (!/^[a-zA-Z0-9_]+$/.test(username)) {
    return {
      isValid: false,
      error: 'Username can only contain letters, numbers, and underscores',
    };
  }

  return { isValid: true };
}

/**
 * Validate phone number
 * Basic validation for various formats
 */
export function isValidPhone(phone: string): boolean {
  // Remove all non-digit characters
  const digitsOnly = phone.replace(/\D/g, '');
  
  // Check if it has 10-15 digits
  return digitsOnly.length >= 10 && digitsOnly.length <= 15;
}

/**
 * Validate date of birth
 * Must be at least 13 years old
 */
export function isValidDateOfBirth(dateString: string): {
  isValid: boolean;
  error?: string;
} {
  const date = new Date(dateString);
  const today = new Date();
  
  // Check if valid date
  if (isNaN(date.getTime())) {
    return { isValid: false, error: 'Invalid date format' };
  }
  
  // Calculate age
  let age = today.getFullYear() - date.getFullYear();
  const monthDiff = today.getMonth() - date.getMonth();
  
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < date.getDate())) {
    age--;
  }
  
  if (age < 13) {
    return { isValid: false, error: 'You must be at least 13 years old' };
  }
  
  if (age > 120) {
    return { isValid: false, error: 'Please enter a valid date of birth' };
  }
  
  return { isValid: true };
}

/**
 * Validate required field
 */
export function isRequired(value: string, fieldName: string = 'This field'): {
  isValid: boolean;
  error?: string;
} {
  const trimmed = value.trim();
  
  if (!trimmed) {
    return { isValid: false, error: `${fieldName} is required` };
  }
  
  return { isValid: true };
}

/**
 * Validate form data
 */
export interface ValidationRule {
  validator: (value: any) => { isValid: boolean; error?: string; errors?: string[] };
  message?: string;
}

export interface ValidationRules {
  [field: string]: ValidationRule[];
}

export function validateForm(
  data: Record<string, any>,
  rules: ValidationRules
): {
  isValid: boolean;
  errors: Record<string, string>;
} {
  const errors: Record<string, string> = {};

  Object.entries(rules).forEach(([field, fieldRules]) => {
    const value = data[field];

    for (const rule of fieldRules) {
      const result = rule.validator(value);

      if (!result.isValid) {
        errors[field] = result.error || result.errors?.[0] || rule.message || 'Invalid value';
        break; // Stop at first error for this field
      }
    }
  });

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
  };
}
