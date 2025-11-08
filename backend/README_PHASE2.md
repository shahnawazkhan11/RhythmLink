# RhythmLink - Artist & Event Management System

A comprehensive Django-based event management system with dynamic pricing, analytics, and smart search capabilities.

## 🎯 Project Overview

RhythmLink is an advanced Artist & Event Management System (AEMS) designed to handle the complexities of modern event management. The system supports multiple user roles and implements sophisticated features like dynamic pricing, real-time analytics, and intelligent search functionality.

## 🔥 Phase 2 Features (Current Implementation)

### ✅ Core Features Implemented

1. **User Role Management**
   - **Managers**: Can create/manage events, set pricing tiers, view analytics
   - **Customers/Audience**: Can browse events, book tickets, provide feedback

2. **Dynamic Pricing System**
   - Tiered pricing based on booking percentage
   - Automatic price adjustments as demand increases
   - Price history tracking for analytics

3. **Event Analytics Dashboard**
   - Real-time booking metrics
   - Revenue tracking by tier
   - Customer feedback analytics
   - Venue utilization reports

4. **Smart Search & Autocomplete**
   - Real-time search suggestions
   - Search history tracking
   - Popular searches analytics

## 📁 Project Structure

```
RhythmLink/
├── accounts/          # User management & role-based access
├── artists/           # Artist and genre management
├── events/            # Core events, venues, event types
├── customers/         # Customer profiles, bookings, feedback
├── pricing/           # Dynamic pricing system
├── analytics/         # Dashboard and reporting
├── search/            # Search functionality and analytics
└── core/              # Project settings and configuration
```

## 🗃️ Database Schema

### Core Entities
- **Artists** & **Genres**: Music artist information and classifications
- **Events**, **Venues**, **Event Types**: Core event management
- **Customers**, **Bookings**, **Tickets**: Customer booking workflow
- **Feedback**: Customer review system

### Phase 2 Enhancements
- **Price Tiers**: Dynamic pricing configuration
- **Price History**: Audit trail for price changes
- **Event Analytics**: Aggregated metrics and KPIs
- **Search History**: User search tracking
- **User Profiles**: Role-based access control

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Django 5.2+
- SQLite (default) or PostgreSQL for production

### Installation

1. **Clone and Setup**
```bash
git clone <repository-url>
cd RhythmLink
python -m venv .venv
.venv\Scripts\activate  # Windows
```

2. **Install Dependencies**
```bash
pip install django djangorestframework Pillow
```

3. **Database Setup**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. **Run Development Server**
```bash
python manage.py runserver
```

## 👥 User Roles & Permissions

### Event Managers
- Create and manage events
- Configure dynamic pricing tiers
- View comprehensive analytics dashboards
- Manage venue and artist associations

### Customers/Audience
- Browse and search events
- Book tickets with dynamic pricing
- View booking history
- Provide event feedback

## 💰 Dynamic Pricing System

### How It Works
1. **Tier Configuration**: Managers set up pricing tiers (e.g., 0-30%: $500, 31-70%: $700, 71-100%: $1000)
2. **Automatic Updates**: System calculates current booking percentage and adjusts prices
3. **Real-time Display**: Customers see current tier pricing
4. **History Tracking**: All price changes are logged for analysis

## 📊 Analytics Dashboard Features

### Manager Metrics
- **Booking Trends**: Daily/weekly booking velocity
- **Revenue Analytics**: Total revenue and revenue per tier
- **Customer Insights**: Demographics and preferences
- **Venue Performance**: Utilization rates across venues
- **Feedback Summary**: Average ratings and sentiment analysis

## 🔍 Smart Search Features

### Autocomplete System
- Real-time search suggestions for events, artists, venues
- Typo tolerance and fuzzy matching
- Personalized suggestions based on search history

## 🛠️ API Endpoints

### Events API
```
GET /api/events/events/ - List all events
POST /api/events/events/ - Create event (Manager only)
GET /api/events/venues/ - List venues
```

### Pricing API  
```
GET /api/pricing/tiers/{event_id}/ - Get price tiers for event
GET /api/pricing/current-price/{event_id}/ - Get current price
```

### Analytics API
```
GET /api/analytics/dashboard/{event_id}/ - Event-specific dashboard
GET /api/analytics/manager-dashboard/ - Manager overview
```

---

**Phase 2 Complete - Ready for Development & Testing** ✅