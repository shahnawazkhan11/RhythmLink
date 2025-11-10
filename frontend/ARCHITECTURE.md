# 🏗️ RhythmLink Frontend Architecture

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         NEXT.JS APP                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌──────────────┐         ┌──────────────┐                      │
│  │  Login Page  │         │ Register Page│                       │
│  │              │         │              │                       │
│  │  /login      │         │  /register   │                       │
│  └──────┬───────┘         └──────┬───────┘                      │
│         │                        │                               │
│         └────────────┬───────────┘                               │
│                      │                                           │
│         ┌────────────▼────────────┐                             │
│         │     Auth Modules        │                              │
│         │  ┌─────────────────┐   │                              │
│         │  │  LoginForm.tsx  │   │                              │
│         │  └─────────────────┘   │                              │
│         │  ┌─────────────────┐   │                              │
│         │  │ RegisterForm.tsx│   │                              │
│         │  └─────────────────┘   │                              │
│         └────────────┬────────────┘                             │
│                      │                                           │
│         ┌────────────▼────────────┐                             │
│         │     UI Components       │                              │
│         │  • Button               │                              │
│         │  • Input                │                              │
│         │  • Select               │                              │
│         │  • Alert                │                              │
│         └────────────┬────────────┘                             │
│                      │                                           │
│         ┌────────────▼────────────┐                             │
│         │      useAuth Hook       │                              │
│         │  • useAuth()            │                              │
│         │  • useRequireAuth()     │                              │
│         │  • useRequireRole()     │                              │
│         │  • useGuestOnly()       │                              │
│         └────────────┬────────────┘                             │
│                      │                                           │
│         ┌────────────▼────────────┐                             │
│         │    Zustand Store        │                              │
│         │  • user                 │                              │
│         │  • isAuthenticated      │                              │
│         │  • login()              │                              │
│         │  • register()           │                              │
│         │  • logout()             │                              │
│         └────────────┬────────────┘                             │
│                      │                                           │
│         ┌────────────▼────────────┐                             │
│         │       API Layer         │                              │
│         │  ┌──────────────────┐  │                              │
│         │  │   client.ts      │  │                              │
│         │  │  (Fetch Wrapper) │  │                              │
│         │  └────────┬─────────┘  │                              │
│         │           │             │                              │
│         │  ┌────────▼─────────┐  │                              │
│         │  │    auth.ts       │  │                              │
│         │  │  • login()       │  │                              │
│         │  │  • register()    │  │                              │
│         │  │  • logout()      │  │                              │
│         │  │  • getProfile()  │  │                              │
│         │  └──────────────────┘  │                              │
│         └────────────┬────────────┘                             │
└──────────────────────┼─────────────────────────────────────────┘
                       │
                       │ HTTP Requests
                       │ (with CSRF Token)
                       │
┌──────────────────────▼─────────────────────────────────────────┐
│                    DJANGO BACKEND                                │
│                   http://localhost:8000                          │
├─────────────────────────────────────────────────────────────────┤
│  • POST /api/accounts/register/                                  │
│  • POST /api/accounts/login/                                     │
│  • POST /api/accounts/logout/                                    │
│  • GET  /api/accounts/profile/                                   │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Authentication Flow

### Registration Flow
```
User Input (RegisterForm)
    │
    ├─► Form Validation (validators.ts)
    │   └─► If invalid → Show errors
    │
    ├─► If valid → useAuth.register()
    │       │
    │       └─► authStore.register()
    │               │
    │               └─► authAPI.register()
    │                       │
    │                       └─► apiClient.post()
    │                               │
    │                               └─► fetch() with CSRF
    │                                       │
    │                                       ├─► Django Backend
    │                                       │       │
    │                                       │       └─► Create User
    │                                       │
    │                                       └─► Response
    │                                               │
    │                                               ├─► Success
    │                                               │   └─► Set user in store
    │                                               │       └─► Redirect to /
    │                                               │
    │                                               └─► Error
    │                                                   └─► Show error message
```

### Login Flow
```
User Input (LoginForm)
    │
    ├─► Form Validation
    │   └─► If invalid → Show errors
    │
    ├─► If valid → useAuth.login()
    │       │
    │       └─► authStore.login()
    │               │
    │               └─► authAPI.login()
    │                       │
    │                       └─► apiClient.post()
    │                               │
    │                               └─► fetch() with CSRF
    │                                       │
    │                                       ├─► Django Backend
    │                                       │       │
    │                                       │       └─► Verify credentials
    │                                       │               └─► Create session
    │                                       │
    │                                       └─► Response
    │                                               │
    │                                               ├─► Success
    │                                               │   └─► Set user in store
    │                                               │       └─► Save to localStorage
    │                                               │           └─► Redirect based on role
    │                                               │
    │                                               └─► Error
    │                                                   └─► Show error message
```

### Protected Route Flow
```
User visits /manager
    │
    ├─► middleware.ts (runs first)
    │   └─► Can add auth checks here
    │
    ├─► Page Component loads
    │   │
    │   └─► useRequireRole(['manager'])
    │           │
    │           ├─► Check authStore.isAuthenticated
    │           │   └─► If false → redirect to /login
    │           │
    │           └─► Check authStore.user.role
    │               └─► If not 'manager' → redirect to /
    │
    └─► Render protected content
```

## 🗂️ Data Flow

### State Management
```
┌─────────────────────────────────────────┐
│         Zustand Store (authStore)        │
├─────────────────────────────────────────┤
│ State:                                   │
│  • user: UserWithProfile | null          │
│  • isAuthenticated: boolean              │
│  • isLoading: boolean                    │
│  • error: string | null                  │
│                                          │
│ Actions:                                 │
│  • login(username, password)             │
│  • register(data)                        │
│  • logout()                              │
│  • fetchProfile()                        │
│  • setUser(user)                         │
│  • setError(error)                       │
│                                          │
│ Computed:                                │
│  • getRole() → UserRole                  │
│  • isManager() → boolean                 │
│  • isCustomer() → boolean                │
│  • isAdmin() → boolean                   │
└─────────────────────────────────────────┘
         │
         ├─► Persisted to localStorage
         │   (key: 'rhythmlink-auth-storage')
         │
         └─► Consumed by components via useAuth()
```

### Component Hierarchy
```
Page (login/register)
    │
    └─► Auth Module (LoginForm/RegisterForm)
            │
            ├─► UI Components
            │   ├─► Input (email, password, etc.)
            │   ├─► Button (submit)
            │   ├─► Select (role)
            │   └─► Alert (errors)
            │
            └─► Hooks
                └─► useAuth()
                    └─► authStore
```

## 🔐 Security Layers

```
┌─────────────────────────────────────────┐
│         Security Measures                │
├─────────────────────────────────────────┤
│                                          │
│  Layer 1: Client-side Validation         │
│  ├─► Email format                        │
│  ├─► Password strength                   │
│  ├─► Phone number format                 │
│  └─► Required fields                     │
│                                          │
│  Layer 2: API Client                     │
│  ├─► CSRF token from cookies            │
│  ├─► Credentials included               │
│  └─► Error handling                      │
│                                          │
│  Layer 3: Django Backend                 │
│  ├─► Session authentication             │
│  ├─► CSRF verification                  │
│  ├─► Password hashing                   │
│  ├─► Input sanitization                 │
│  └─► Database validation                │
│                                          │
│  Layer 4: Route Protection               │
│  ├─► Middleware checks                  │
│  ├─► Hook-based guards                  │
│  └─► Role verification                  │
│                                          │
└─────────────────────────────────────────┘
```

## 📦 Module Dependencies

```
┌──────────────┐
│   Pages      │
└──────┬───────┘
       │
       │ uses
       ▼
┌──────────────┐
│   Modules    │
└──────┬───────┘
       │
       │ uses
       ▼
┌──────────────┐     ┌──────────────┐
│ UI Components│     │    Hooks     │
└──────┬───────┘     └──────┬───────┘
       │                    │
       │                    │ uses
       │                    ▼
       │             ┌──────────────┐
       │             │    Store     │
       │             └──────┬───────┘
       │                    │
       │                    │ uses
       │                    ▼
       │             ┌──────────────┐
       │             │   API Layer  │
       │             └──────┬───────┘
       │                    │
       │ both use           │
       └────────────────────┴────────►
                            │
                            ▼
                     ┌──────────────┐
                     │    Utils     │
                     │  • Validators│
                     │  • Formatters│
                     └──────────────┘
```

## 🎯 Key Design Patterns

### 1. Separation of Concerns
- **UI Layer**: Components only handle rendering
- **Business Logic**: In stores and hooks
- **Data Access**: API layer handles all HTTP

### 2. Single Responsibility
- Each component does one thing well
- Reusable across different contexts

### 3. Dependency Injection
- Components receive dependencies via props
- Hooks inject store functionality

### 4. Error Handling
- Centralized in API client
- User-friendly messages
- Field-specific validation

### 5. Type Safety
- Full TypeScript coverage
- Interface-driven development
- Compile-time error checking

## 📱 Responsive Design

All components use Tailwind CSS with responsive classes:
- Mobile-first approach
- Breakpoints: `sm:`, `md:`, `lg:`, `xl:`
- Flexible grid layouts
- Touch-friendly buttons

## 🔄 State Synchronization

```
Component State ←→ Zustand Store ←→ localStorage ←→ Backend Session
                   (real-time)      (persistent)     (server-side)
```

## 🎨 Styling Architecture

```
Tailwind CSS (Utility Classes)
    │
    ├─► Global Styles (app/globals.css)
    │
    ├─► Component-level Classes
    │   └─► Inline with JSX
    │
    └─► Responsive Design
        └─► Mobile-first with breakpoints
```

This architecture ensures:
- ✅ Scalability
- ✅ Maintainability
- ✅ Type Safety
- ✅ Security
- ✅ Performance
- ✅ Developer Experience
