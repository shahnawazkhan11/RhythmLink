# 🎯 Quick Start Guide - RhythmLink Authentication

## ⚡ Installation (3 steps)

### 1. Install Dependencies
```bash
cd frontend
pnpm install zustand
```

### 2. Verify Environment
The `.env.local` file should already exist with:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Start Development
```bash
# Terminal 1: Start Django backend
cd backend
python manage.py runserver

# Terminal 2: Start Next.js frontend
cd frontend
pnpm dev
```

## 🧪 Test Authentication

### Test Login
1. Go to: `http://localhost:3000/login`
2. Enter credentials from your Django database
3. Click "Sign In"

### Test Registration
1. Go to: `http://localhost:3000/register`
2. Fill in all fields
3. Select role: **Customer** or **Manager**
4. Click "Create Account"

## 📁 What Was Created

### Core Files
```
src/
├── types/api.ts                 # TypeScript interfaces for API
├── lib/
│   ├── api/
│   │   ├── client.ts           # Fetch wrapper (NO AXIOS)
│   │   └── auth.ts             # Auth API functions
│   └── utils/
│       ├── validators.ts       # Form validation
│       └── formatters.ts       # Data formatting
├── store/authStore.ts          # Zustand state management
├── hooks/useAuth.ts            # Auth hooks
├── components/ui/              # Reusable UI components
│   ├── Button.tsx
│   ├── Input.tsx
│   ├── Select.tsx
│   └── Alert.tsx
├── modules/auth/               # Auth feature modules
│   ├── LoginForm.tsx
│   └── RegisterForm.tsx
└── app/(public)/               # Public pages
    ├── login/page.tsx
    └── register/page.tsx
```

## 🔑 Key Features

### ✅ Authentication Flow
- [x] Login with username/password
- [x] Register with role selection (Customer/Manager)
- [x] Auto-redirect after login based on role
- [x] Session persistence with localStorage
- [x] Logout functionality

### ✅ Form Validation
- [x] Username: 3-30 chars, alphanumeric + underscores
- [x] Email: Valid email format
- [x] Password: Min 8 chars, uppercase, lowercase, number
- [x] Phone: 10-15 digits
- [x] Date of Birth: Must be 13+ years old

### ✅ Security
- [x] CSRF token handling
- [x] Session-based authentication
- [x] Secure password validation
- [x] Role-based access control

## 🎨 Using Components

### Button
```tsx
import { Button } from '@/components/ui/Button';

<Button variant="primary" size="lg" isLoading={loading}>
  Submit
</Button>
```

### Input
```tsx
import { Input } from '@/components/ui/Input';

<Input
  label="Email"
  type="email"
  error={errors.email}
  required
/>
```

### Auth Hook
```tsx
import { useAuth } from '@/hooks/useAuth';

const { user, isAuthenticated, login, logout } = useAuth();
```

## 🛡️ Protected Routes

### Require Authentication
```tsx
import { useRequireAuth } from '@/hooks/useAuth';

export default function ProtectedPage() {
  useRequireAuth('/login'); // Redirect if not logged in
  return <div>Protected Content</div>;
}
```

### Require Specific Role
```tsx
import { useRequireRole } from '@/hooks/useAuth';

export default function ManagerPage() {
  useRequireRole(['manager'], '/'); // Only managers
  return <div>Manager Dashboard</div>;
}
```

## 🐛 Common Issues

### Issue: CORS Error
**Solution:** Add to Django `settings.py`:
```python
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_CREDENTIALS = True
```

### Issue: CSRF Token Missing
**Solution:** 
1. Check browser cookies for `csrftoken`
2. Verify Django CSRF middleware is enabled
3. Ensure `credentials: 'include'` in fetch

### Issue: Zustand Not Found
**Solution:** 
```bash
pnpm install zustand
```

### Issue: TypeScript Errors
**Solution:**
```bash
pnpm install
```

## 📚 API Endpoints

All endpoints are prefixed with `/api/accounts/`:

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register/` | Register new user |
| POST | `/login/` | Login user |
| POST | `/logout/` | Logout user |
| GET | `/profile/` | Get user profile |
| PATCH | `/profile/` | Update profile |

## 🎯 Next Steps

### Create Protected Pages
1. **Manager Dashboard** → `src/app/manager/page.tsx`
2. **User Dashboard** → `src/app/user/page.tsx`
3. **Event Listings** → `src/app/(public)/events/page.tsx`

### Add Features
1. Password reset flow
2. Email verification
3. Profile management
4. Social login
5. Two-factor authentication

### API Integration
Create API modules for:
- Events → `src/lib/api/events.ts`
- Bookings → `src/lib/api/bookings.ts`
- Pricing → `src/lib/api/pricing.ts`
- Search → `src/lib/api/search.ts`

## 💡 Tips

1. **Always use `@/` imports** for clean paths
2. **Never call fetch directly** in components - use API functions
3. **Use hooks** for reusable logic
4. **Follow the folder structure** strictly
5. **Validate forms** before submitting
6. **Handle errors** gracefully with Alert component

## ✅ Checklist

Before testing:
- [ ] Zustand installed (`pnpm install zustand`)
- [ ] `.env.local` configured
- [ ] Django backend running (port 8000)
- [ ] Next.js dev server running (port 3000)
- [ ] Test user created in Django admin

## 🚀 You're Ready!

Your authentication system is complete and ready to use. Start building the rest of your application by following the same patterns established here.

For detailed documentation, see `AUTHENTICATION_README.md`.

Happy coding! 🎉
