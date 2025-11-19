# 🎫 Ticket Booking Flow - Complete Guide

## ✅ Current Setup (WORKING)

### 1. **Backend is Ready**
- ✅ Tickets created via command: `python manage.py create_tickets --tickets-per-event 50`
- ✅ Booking API endpoints configured
- ✅ Token authentication working

### 2. **Frontend is Ready**
- ✅ Event listing page at `/events`
- ✅ Event detail page at `/events/[id]` shows booking interface
- ✅ User bookings page at `/user/bookings`

---

## 🚀 How to Book Tickets (Customer Flow)

### Step 1: View Events
1. Go to `http://localhost:3000/events`
2. You'll see all active events with "Book Tickets" button

### Step 2: Click on Event
1. Click "Book Tickets" button on any event card
2. You'll be taken to `http://localhost:3000/events/[event-id]`

### Step 3: Select Tickets
1. You'll see:
   - Event details (name, date, time, venue, price)
   - Available tickets grid (showing up to 20 tickets)
   - Each ticket is clickable
2. Click on tickets to select them (they turn blue when selected)
3. You can select multiple tickets (up to max_tickets_per_customer limit)
4. See the booking summary with total amount

### Step 4: Confirm Booking
1. Click "Confirm Booking" button
2. If not logged in → redirected to login page
3. If logged in → booking created immediately
4. Success message appears
5. Auto-redirect to "My Bookings" page

### Step 5: View Your Bookings
1. Go to `http://localhost:3000/user/bookings`
2. See all your bookings with:
   - Event details
   - Number of tickets
   - Total amount
   - Booking status
   - Option to cancel (if status is "confirmed")

---

## 📋 Test Scenario

### For Customer User:

```bash
# 1. Make sure you have tickets
cd backend
python manage.py create_tickets --tickets-per-event 50

# 2. Login as customer at http://localhost:3000/login
# (or register new customer at http://localhost:3000/register with role="customer")

# 3. Browse events at http://localhost:3000/events

# 4. Click "Book Tickets" on any event

# 5. Select 2-3 tickets by clicking on them

# 6. Click "Confirm Booking"

# 7. Check your bookings at http://localhost:3000/user/bookings
```

---

## 🎯 What Happens Behind the Scenes

### When You Book Tickets:

1. **Frontend** sends POST request to `/api/customers/book/`:
   ```json
   {
     "event": 1,
     "tickets": [1, 2, 3],
     "total_amount": "150.00"
   }
   ```

2. **Backend** (Django):
   - Gets/creates Customer profile for logged-in user
   - Creates Booking record
   - Updates selected tickets from "available" → "booked"
   - Returns booking confirmation

3. **Database** records:
   - New row in `customers_booking` table
   - Tickets updated in `customers_ticket` table
   - Linked via ManyToMany relationship

---

## 🔍 Verify Everything is Working

### Check in Django Admin:
1. Go to `http://localhost:8000/admin/`
2. Check "Bookings" - you should see new booking
3. Check "Tickets" - selected tickets should show status="booked"

### Check in Frontend:
1. Go to `/user/bookings` - see your booking
2. Event card should show booking details
3. Can cancel booking (tickets return to "available")

---

## ✨ Features Available

### Customer Can:
- ✅ Browse all active events
- ✅ View event details
- ✅ See available tickets in real-time
- ✅ Select multiple tickets (visual feedback)
- ✅ See total cost before confirming
- ✅ Book tickets (creates database record)
- ✅ View all their bookings
- ✅ Cancel bookings (tickets become available again)

### Manager Can:
- ✅ Create new events
- ✅ View dashboard with analytics
- ✅ Manage events

---

## 🎉 You're All Set!

The booking system is **fully functional**. Just:
1. ✅ Make sure backend is running (`python manage.py runserver`)
2. ✅ Make sure frontend is running (`pnpm run dev`)
3. ✅ Tickets are created for events
4. ✅ Users can book tickets!

**Try it now!** 🚀
