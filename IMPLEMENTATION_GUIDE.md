# Event Management & Booking Implementation

## ✅ Features Implemented

### 1. Manager Features
- **Create Events**: Managers can create new events with details like name, date, time, venue, and pricing
- **Dashboard**: View all managed events, analytics, and bookings
- **Event Management**: Access to event creation form at `/manager/events/create`

### 2. Customer Features
- **Browse Events**: View all available events at `/events`
- **Book Tickets**: Select and book tickets for events at `/events/[id]`
- **View Bookings**: See all bookings and their status at `/user/bookings`
- **Cancel Bookings**: Cancel confirmed bookings

### 3. Authentication
- Token-based authentication (fixed)
- No more browser auth dialog
- Proper role-based access control

## 📁 Files Created/Modified

### Frontend
- `src/modules/events/CreateEventForm.tsx` - Event creation form
- `src/modules/bookings/BookTickets.tsx` - Ticket booking component
- `app/manager/events/create/page.tsx` - Create event page
- `app/events/[id]/page.tsx` - Event detail with booking
- `app/user/bookings/page.tsx` - User bookings page
- `src/lib/api/events.ts` - Events API (already existed, verified)
- `src/lib/api/bookings.ts` - Bookings API (already existed, verified)

### Backend
- `customers/views.py` - Updated with full booking functionality
- `customers/urls.py` - Added booking endpoints
- `customers/management/commands/create_tickets.py` - Command to create tickets
- `core/settings.py` - Fixed authentication (TokenAuthentication)

## 🚀 How to Test

### Step 1: Setup Backend

1. Start Django server:
   ```bash
   cd backend
   python manage.py runserver
   ```

2. Create tickets for events (run this command):
   ```bash
   python manage.py create_tickets --tickets-per-event 50
   ```

### Step 2: Setup Frontend

1. Start Next.js dev server:
   ```bash
   cd frontend
   pnpm run dev
   ```

### Step 3: Test Manager Flow

1. **Login as Manager**:
   - Go to `http://localhost:3000/login`
   - Login with a manager account
   
2. **Create Event**:
   - Navigate to `http://localhost:3000/manager`
   - Click "Create Event" button
   - Fill in all required fields:
     - Event Name
     - Date and Time
     - Venue (select from dropdown)
     - Event Type (select from dropdown)
     - Ticket Price
   - Submit the form
   
3. **Run ticket creation** (after creating event):
   ```bash
   python manage.py create_tickets --event-id [EVENT_ID] --tickets-per-event 50
   ```

### Step 4: Test Customer Flow

1. **Logout and Register as Customer**:
   - Logout from manager account
   - Go to `/register`
   - Register with role = "customer"
   
2. **Browse Events**:
   - Navigate to `http://localhost:3000/events`
   - You should see the event created by the manager
   
3. **Book Tickets**:
   - Click on an event
   - Select tickets (you can select multiple)
   - Click "Confirm Booking"
   - You should see a success message
   
4. **View Bookings**:
   - Click "My Bookings" in the header
   - Or go to `http://localhost:3000/user/bookings`
   - See your booking with details
   - Can cancel if status is "confirmed"

## 🔧 API Endpoints

### Events
- `GET /api/events/events/` - List all events
- `GET /api/events/events/{id}/` - Get event details
- `POST /api/events/events/` - Create event (Manager only)
- `PATCH /api/events/events/{id}/` - Update event (Manager only)
- `DELETE /api/events/events/{id}/` - Delete event (Manager only)

### Venues
- `GET /api/events/venues/` - List all venues
- `POST /api/events/venues/` - Create venue (Manager only)

### Event Types
- `GET /api/events/event-types/` - List all event types

### Bookings
- `POST /api/customers/book/` - Create booking (Authenticated)
- `GET /api/customers/my-bookings/` - Get user's bookings (Authenticated)
- `GET /api/customers/bookings/{id}/` - Get booking details (Authenticated)
- `PATCH /api/customers/bookings/{id}/` - Cancel booking (Authenticated)

### Tickets
- `GET /api/customers/tickets/?event={id}&status=available` - Get available tickets

## ⚠️ Prerequisites

Before testing, ensure you have:

1. **Venues in Database**: Events need venues. Create some using Django admin:
   ```
   http://localhost:8000/admin/events/venue/
   ```

2. **Event Types in Database**: Events need types. Create some using Django admin:
   ```
   http://localhost:8000/admin/events/eventtype/
   ```
   Examples: Concert, Festival, Live Performance, etc.

3. **Manager Profile**: Users with role="manager" need an EventManager profile. Create in Django admin:
   ```
   http://localhost:8000/admin/events/eventmanager/
   ```

4. **Customer Profile**: Automatically created when booking (handled in code)

## 🐛 Troubleshooting

### Issue: "You do not have permission to perform this action"
**Solution**: Make sure TokenAuthentication is enabled in settings.py and you've restarted the Django server.

### Issue: No tickets available
**Solution**: Run the create_tickets management command:
```bash
python manage.py create_tickets
```

### Issue: Cannot create event - no venues/event types
**Solution**: Create venues and event types in Django admin first.

### Issue: Browser auth dialog still appears
**Solution**: Clear browser cache and cookies, make sure BasicAuthentication is removed from settings.

## 📝 Next Steps (Optional Enhancements)

1. Add image upload for event posters
2. Add payment integration
3. Add email notifications for bookings
4. Add event search and filters
5. Add ticket QR codes
6. Add dynamic pricing based on demand
7. Add reviews/ratings for events
8. Add artist assignment to events

## 🎉 Summary

You now have a fully functional event management and booking system where:
- **Managers** can create and manage events
- **Customers** can browse events and book tickets
- **Both** have proper authentication and role-based access
- The frontend and backend are properly connected via REST API with token authentication
