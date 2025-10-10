# RhythmLink - Artist & Event Management System

**Phase 2 Implementation - Complete** ✅

A comprehensive Django-based event management system implementing dynamic pricing, real-time analytics, and intelligent search for DBMS course project.

---

## 🎯 Phase 2 Features Implemented

### ✅ 1. Dynamic Pricing System
**Status: Complete**

- **Database Schema:**
  - `PriceTier` model with tier ranges, prices, and manager tracking
  - `PriceHistory` audit log for all price changes
  - `Ticket` model extended with `base_price`, `final_price`, `current_tier`

- **Business Logic:**
  - Automatic price calculation based on booking percentage
  - Django signals auto-update prices on booking/cancellation
  - Tier overlap validation
  - Service class (`DynamicPricingService`) for centralized pricing logic

- **API Endpoints:**
  - `GET /api/pricing/tiers/<event_id>/` - View all price tiers
  - `GET /api/pricing/current-price/<event_id>/` - Get current price & tier

- **DBMS Concepts:**
  - Constraints: Unique tier ranges, percentage validation
  - Triggers: Django signals (equivalent to database triggers)
  - Stored Procedures: Service methods for complex calculations
  - Indexes: On event, status, tier fields

---

### ✅ 2. Event Popularity Dashboard
**Status: Complete**

- **Database Schema:**
  - `EventAnalytics` - Aggregated metrics per event
  - `ManagerDashboardConfig` - Customizable manager preferences
  - `DashboardSnapshot` - Daily historical data

- **Metrics Implemented:**
  - Total bookings vs available seats
  - Revenue (total and by price tier)
  - Booking velocity (bookings per day)
  - Average customer rating
  - Genre-wise performance
  - Venue utilization rates

- **API Endpoints:**
  - `GET /api/analytics/dashboard/<event_id>/` - Detailed event metrics
  - `GET /api/analytics/manager-dashboard/` - Manager overview

- **Management Command:**
  - `python manage.py refresh_analytics` - Update all analytics data

- **DBMS Concepts:**
  - Complex aggregations (SUM, AVG, COUNT, GROUP BY)
  - Multi-table joins
  - Materialized view pattern (EventAnalytics)
  - Time-series queries

---

### ✅ 3. Autocomplete & Smart Search
**Status: Complete**

- **Database Schema:**
  - `SearchHistory` - Track user searches and clicks
  - `PopularSearches` - Aggregate popular search terms

- **Features:**
  - Real-time prefix matching across Artists, Events, Venues
  - Case-insensitive search
  - Search history tracking (authenticated users)
  - Popular searches analytics

- **API Endpoints:**
  - `GET /api/search/autocomplete/?q=query` - Get search suggestions
  - `GET /api/search/popular/` - View popular search terms

- **DBMS Concepts:**
  - LIKE/ILIKE pattern matching
  - Full-text search indexes
  - Query optimization with indexes
  - Incremental aggregation (F expressions)

---

## 🗃️ Database Schema (Phase 2)

### Core Entities (Phase 1 Foundation)
- **Genre** - Music genres
- **Artist** - Artist/band information
- **EventType** - Concert, Festival, etc.
- **Venue** - Event locations with capacity
- **Event** - Main event details
- **Performs** - Artist-event relationship
- **EventManager** - Manager profiles
- **Customer** - Customer profiles
- **Ticket** - Ticket inventory
- **Booking** - Customer bookings
- **Feedback** - Customer reviews

### Phase 2 Additions
- **PriceTier** - Dynamic pricing tiers
- **PriceHistory** - Price change audit log
- **EventAnalytics** - Aggregated event metrics
- **ManagerDashboardConfig** - Dashboard customization
- **DashboardSnapshot** - Historical metrics
- **SearchHistory** - User search tracking
- **PopularSearches** - Search analytics
- **UserProfile** - Extended user with roles (Manager/Audience)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Django 5.2+
- Virtual environment

### Installation

**1. Activate Virtual Environment:**
```bash
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Windows CMD
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

**2. Install Dependencies:**
```bash
pip install django djangorestframework Pillow
```

**3. Run Automated Setup:**
```bash
python setup.py
```

Or manually:
```bash
python manage.py makemigrations accounts artists events pricing customers analytics search
python manage.py migrate
```

**4. Create Superuser:**
```bash
python manage.py createsuperuser
```

**5. Populate Sample Data:**
```bash
python manage.py populate_sample_data
```

**6. Refresh Analytics:**
```bash
python manage.py refresh_analytics
```

**7. Run Development Server:**
```bash
python manage.py runserver
```

**8. Access Application:**
- Admin Panel: http://127.0.0.1:8000/admin/
- API Root: http://127.0.0.1:8000/api/

---

## 👥 User Roles

### Event Managers
**Credentials:** `manager1` / `manager123` (or manager2, manager3)

**Capabilities:**
- Create and manage events
- Configure dynamic pricing tiers
- View comprehensive analytics dashboards
- Manage venue and artist assignments
- Monitor booking trends and revenue

### Customers/Audience
**Credentials:** `customer1` / `customer123` (customer1-20 available)

**Capabilities:**
- Browse and search events
- View real-time pricing
- Book tickets with dynamic pricing
- Provide event feedback
- View booking history

---

## 📊 API Endpoints

### Dynamic Pricing
```http
GET /api/pricing/tiers/<event_id>/
GET /api/pricing/current-price/<event_id>/
```

### Analytics Dashboard
```http
GET /api/analytics/dashboard/<event_id>/
GET /api/analytics/manager-dashboard/
```

### Smart Search
```http
GET /api/search/autocomplete/?q=<query>
GET /api/search/popular/?limit=10
```

### Events
```http
GET /api/events/events/
GET /api/events/venues/
GET /api/events/event-types/
```

### Artists
```http
GET /api/artists/artists/
GET /api/artists/genres/
```

---

## 🎓 DBMS Concepts Demonstrated

### Normalization
- All tables in 3NF
- Functional dependencies documented
- No update/insert/delete anomalies

### Indexing
```python
# Strategic indexes implemented
- Artist.name (search)
- Event.date, Event.venue (filtering)
- Ticket.event, Ticket.status (availability)
- Booking.customer, Booking.date (history)
- SearchHistory.user, SearchHistory.timestamp
```

### Constraints
- Primary keys on all tables
- Foreign key relationships with CASCADE/RESTRICT
- UNIQUE constraints (email, seat_number per event)
- Validators (rating 1-5, capacity > 0)
- unique_together for composite keys

### Triggers (Django Signals)
```python
# Implemented signals
1. update_pricing_on_booking - Auto-update prices on new booking
2. update_pricing_on_cancellation - Auto-update on cancellation
3. assign_user_groups - Auto-assign roles on user creation
```

### Stored Procedures (Service Classes)
```python
1. DynamicPricingService.calculate_current_tier()
2. DynamicPricingService.update_ticket_prices()
3. DynamicPricingService.create_default_price_tiers()
```

### Views (ORM Queries & API Views)
```python
1. Event dashboard with aggregated metrics
2. Manager overview across all events
3. Available tickets view
4. Search autocomplete with ranking
```

---

## 💰 Dynamic Pricing Example

```python
# Manager creates tiers:
Early Bird:  0-30% capacity  → ₹500
Regular:    31-70% capacity  → ₹700
Premium:    71-100% capacity → ₹1000

# System automatically adjusts:
25% booked → Current Price: ₹500 (Early Bird)
45% booked → Current Price: ₹700 (Regular)
80% booked → Current Price: ₹1000 (Premium)
```

---

## 📈 Sample Analytics Queries

### Revenue by Event
```python
Event.objects.annotate(
    total_revenue=Sum('bookings__total_amount'),
    tickets_sold=Count('bookings')
).order_by('-total_revenue')
```

### Booking Percentage
```python
event.tickets.filter(status='booked').count() / event.tickets.count() * 100
```

### Venue Utilization
```python
Venue.objects.annotate(
    events_count=Count('events'),
    total_bookings=Sum('events__bookings')
)
```

---

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Manual Testing Workflow
1. Create an event via admin
2. Set up price tiers (Early/Regular/Premium)
3. Create bookings to test dynamic pricing
4. View analytics dashboard
5. Test search autocomplete
6. Verify price changes in history

---

## 📦 Sample Data Generated

When running `populate_sample_data`:
- **10 Genres** (Rock, Pop, Hip Hop, etc.)
- **10 Artists** (Arijit Singh, A.R. Rahman, etc.)
- **8 Venues** across major Indian cities
- **8 Events** with realistic names and dates
- **3 Manager Users** with assigned events
- **20 Customer Users** with varied preferences
- **Price Tiers** for all events (3 tiers each)
- **Tickets** for each event (up to 200 per event)
- **Bookings** (10-40% capacity per event)
- **Feedback** (70% of bookings have ratings)

---

## 🎯 Phase 2 Deliverables

### ✅ Completed
1. **Updated ER Diagram** - Implemented in Django models
2. **DDL Scripts** - Django migrations
3. **Stored Procedures** - Service classes and methods
4. **Dashboard Queries** - ORM aggregations and analytics
5. **Search Functionality** - Autocomplete with history
6. **Test Cases** - Management commands and data validation

### 📊 Evaluation Criteria Met

**Database Design (30%):** ✅
- Price_Tier, EventAnalytics, SearchHistory tables
- Proper normalization and relationships

**SQL Complexity (30%):** ✅
- Aggregate queries (SUM, AVG, COUNT, GROUP BY)
- Multi-table joins
- Complex filtering and annotations

**Normalization (15%):** ✅
- All tables in 3NF
- No redundancy or anomalies

**Functionality (25%):** ✅
- Working dynamic pricing with automatic updates
- Dashboard with real metrics
- Smart search with autocomplete

---

## 🔜 Phase 3 Roadmap

### Planned Features
1. **Recommendation Engine**
   - Collaborative filtering
   - Genre-based matching
   - Artist similarity

2. **Notification System**
   - Booking confirmations
   - Event reminders
   - Price drop alerts

---

## 📝 License

MIT License - Educational Project

---

## 🤝 Support

For questions:
- Check admin panel: http://127.0.0.1:8000/admin/
- Review management commands: `python manage.py help`
- Inspect API endpoints: http://127.0.0.1:8000/api/

---

**Built with ❤️ for DBMS Project - Phase 2 Complete** ✅
