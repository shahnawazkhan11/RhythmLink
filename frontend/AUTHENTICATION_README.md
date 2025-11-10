# RhythmLink Frontend - Authentication System

## 📋 Overview
Complete authentication system for RhythmLink built with Next.js, TypeScript, and Tailwind CSS.

## 🏗️ Architecture

### Folder Structure
```
src/
├── types/
│   └── api.ts                    # TypeScript interfaces
├── lib/
│   ├── api/
│   │   ├── client.ts            # Fetch wrapper with CSRF handling
│   │   └── auth.ts              # Authentication API functions
│   └── utils/
│       ├── validators.ts        # Form validation utilities
│       └── formatters.ts        # Data formatting utilities
├── store/
│   └── authStore.ts             # Zustand authentication store
├── hooks/
│   └── useAuth.ts               # Reusable auth hooks
├── components/
│   └── ui/
│       ├── Button.tsx           # Reusable button component
│       ├── Input.tsx            # Reusable input component
│       ├── Select.tsx           # Reusable select component
│       └── Alert.tsx            # Alert/notification component
├── modules/
│   └── auth/
│       ├── LoginForm.tsx        # Login form module
│       └── RegisterForm.tsx     # Registration form module
├── app/
│   └── (public)/
│       ├── login/
│       │   └── page.tsx         # Login page
│       └── register/
│           └── page.tsx         # Register page
└── middleware.ts                # Route protection middleware
```

## 🚀 Setup Instructions

### 1. Install Dependencies

```bash
# Using pnpm (recommended)
pnpm install zustand

# Or using npm
npm install zustand

# Or using yarn
yarn add zustand
```

### 2. Environment Variables

The `.env.local` file is already created. Make sure the backend URL is correct:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development Server

```bash
# Start Next.js development server
pnpm dev

# Make sure Django backend is also running
cd ../backend
python manage.py runserver
```

## 🔑 Features Implemented

### ✅ Authentication API
- **Login**: Session-based authentication
- **Register**: User registration with role selection (Customer/Manager)
- **Logout**: Clear session and local storage
- **Profile**: Fetch current user profile

### ✅ State Management
- **Zustand Store**: Global auth state with persistence
- **localStorage**: Automatic state persistence across sessions
- **Role-based Access**: Check user role (customer, manager, admin)

### ✅ Form Validation
- **Username**: 3-30 characters, alphanumeric + underscores
- **Email**: Valid email format
- **Password**: Min 8 chars, uppercase, lowercase, number
- **Phone**: 10-15 digits
- **Date of Birth**: Must be 13+ years old

### ✅ UI Components
- **Button**: Multiple variants (primary, secondary, danger, ghost)
- **Input**: With label, error messages, and helper text
- **Select**: Dropdown with validation
- **Alert**: Success/error/warning/info notifications

### ✅ Routing & Protection
- **Public Routes**: Login, Register
- **Protected Routes**: User dashboard, Manager dashboard
- **Auto-redirect**: Logged-in users redirected from auth pages

## 📝 Usage Examples

### Login
```typescript
const { login, isLoading, error } = useAuth();

await login('username', 'password');
```

### Register
```typescript
const { register, isLoading, error } = useAuth();

await register({
  username: 'johndoe',
  email: 'john@example.com',
  password: 'Password123',
  first_name: 'John',
  last_name: 'Doe',
  role: 'customer',
  phone: '+1234567890',
  date_of_birth: '1990-01-01',
});
```

### Check Authentication
```typescript
const { isAuthenticated, user, role } = useAuth();

if (isAuthenticated) {
  console.log('User:', user);
  console.log('Role:', role); // 'customer', 'manager', or 'admin'
}
```

### Protected Page
```typescript
export default function ProtectedPage() {
  useRequireAuth('/login'); // Redirect to login if not authenticated
  
  return <div>Protected content</div>;
}
```

### Role-based Access
```typescript
export default function ManagerPage() {
  useRequireRole(['manager', 'admin'], '/'); // Only managers and admins
  
  return <div>Manager dashboard</div>;
}
```

## 🎨 Component Examples

### Using Button
```tsx
<Button 
  variant="primary" 
  size="lg" 
  isLoading={isLoading}
  onClick={handleClick}
>
  Submit
</Button>
```

### Using Input
```tsx
<Input
  label="Email"
  name="email"
  type="email"
  value={email}
  onChange={handleChange}
  error={errors.email}
  required
  placeholder="Enter your email"
/>
```

### Using Alert
```tsx
<Alert 
  type="error" 
  message="Login failed. Please check your credentials."
  onClose={clearError}
/>
```

## 🔐 Security Features

### CSRF Protection
- Automatically includes CSRF token from cookies
- Required for POST, PUT, PATCH, DELETE requests

### Session-based Auth
- Uses Django's session authentication
- Cookies sent with `credentials: 'include'`

### Password Validation
- Minimum 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 number

### Role-based Access Control
- Customer: Browse events, buy tickets
- Manager: Create/manage events, view analytics
- Admin: Full system access

## 🧪 Testing

### Test Login
1. Navigate to `http://localhost:3000/login`
2. Enter credentials
3. Should redirect to home on success

### Test Registration
1. Navigate to `http://localhost:3000/register`
2. Fill in all required fields
3. Select role (Customer/Manager)
4. Should auto-login and redirect on success

## 📚 API Endpoints Used

- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `GET /api/accounts/profile/` - Get user profile

## 🐛 Troubleshooting

### CORS Errors
Make sure Django backend has CORS configured:
```python
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
```

### CSRF Token Missing
- Check cookies in browser DevTools
- Ensure `credentials: 'include'` is set in fetch
- Verify Django CSRF middleware is enabled

### TypeScript Errors
Run `pnpm install` to ensure all dependencies are installed, including Zustand.

### Authentication Not Persisting
- Check localStorage in DevTools
- Verify Zustand persist middleware is configured
- Clear browser cache and retry

## 🔄 Next Steps

### Additional Features to Implement
1. **Password Reset**: Forgot password flow
2. **Email Verification**: Verify email on registration
3. **Profile Management**: Update user profile
4. **Session Management**: View active sessions
5. **Social Login**: Google/Facebook OAuth
6. **Two-Factor Auth**: Enhanced security

### Pages to Create
1. **Home Page**: Event listings
2. **Manager Dashboard**: Event management
3. **User Dashboard**: Booking history
4. **Event Details**: View/book events
5. **Profile Page**: User settings

## 📖 References

- [Next.js Documentation](https://nextjs.org/docs)
- [Zustand Documentation](https://docs.pmnd.rs/zustand)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Django REST Framework](https://www.django-rest-framework.org/)

## ✅ Checklist

- [x] TypeScript interfaces defined
- [x] API client with fetch wrapper
- [x] CSRF token handling
- [x] Authentication API functions
- [x] Zustand store setup
- [x] Auth hooks created
- [x] UI components (Button, Input, Select, Alert)
- [x] Login form with validation
- [x] Register form with validation
- [x] Login page
- [x] Register page
- [x] Middleware for route protection
- [x] Environment variables configured
- [ ] Install Zustand dependency
- [ ] Test login flow
- [ ] Test registration flow
- [ ] Create additional protected pages

## 📝 Notes

- Remember to run `pnpm install zustand` before testing
- Backend must be running on port 8000
- All API calls use native `fetch()` (NO AXIOS)
- Follow the folder structure strictly as per instructions
- State management uses Zustand with localStorage persistence
- Forms have comprehensive validation
- Role-based access control implemented
