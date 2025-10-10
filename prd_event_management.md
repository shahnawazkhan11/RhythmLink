# Project Requirements Document
## Artist & Event Management System with Advanced Features

---

## 1. PROJECT OVERVIEW

### 1.1 Project Title
Artist & Event Management System (AEMS)

### 1.2 Project Type
Database Management System (DBMS) - Project Based Learning

### 1.3 Team Members
- [Team Member 1]
- [Team Member 2]
- [Team Member 3]

### 1.4 Project Duration
3 Evaluation Phases

### 1.5 Project Description
A comprehensive database-driven application for managing artists, events, venues, and customer bookings with intelligent features including dynamic pricing, recommendation engine, analytics dashboards, notifications, and smart search capabilities.

---

## 2. PROJECT OBJECTIVES

### 2.1 Primary Objectives
- Design and implement a normalized relational database for event management
- Develop a scalable system to handle multiple artists, venues, and events
- Implement customer booking and ticketing workflow
- Build advanced features to enhance user experience and business operations

### 2.2 Learning Objectives
- Apply normalization principles (1NF, 2NF, 3NF, BCNF)
- Implement complex SQL queries (joins, subqueries, aggregations)
- Design triggers and stored procedures
- Create views for data abstraction
- Implement database security and transaction management
- Work with indexes for query optimization

---

## 3. EXISTING SYSTEM (PHASE 1 - COMPLETED)

### 3.1 Database Schema
The following tables have been implemented:

**Core Tables:**
- **Artist** (artist_id, name, genre_id, contact)
- **Genre** (genre_id, name)
- **Event** (event_id, name, date, start_time, end_time, venue_id, type_id)
- **Venue** (venue_id, name, location, capacity)
- **Event_Type** (type_id, name)

**Relationship Tables:**
- **Performs** (artist_id, event_id, performance_time)

**Customer Management:**
- **Customer** (customer_id, name, email, phone)
- **Ticket** (ticket_id, event_id, price, seat_no, status)
- **Booking** (booking_id, customer_id, ticket_id, event_id, booking_date)
- **Feedback** (feedback_id, customer_id, event_id, rating, comment)

**Management:**
- **Event_Manager** (manager_id, name, contact, event_id)

### 3.2 Current Capabilities
- Basic CRUD operations for all entities
- Simple booking workflow
- Artist-event association
- Customer feedback collection
- Static ticket pricing

### 3.3 Limitations Identified
- No intelligent pricing mechanism
- No personalized recommendations
- Limited analytics for managers
- No automated customer engagement
- Basic search functionality

---

## 4. PROPOSED ENHANCEMENTS

### 4.1 Feature Set Overview

| Feature | Phase | Priority | Complexity |
|---------|-------|----------|------------|
| Dynamic Pricing System | Phase 2 | High | Medium |
| Event Popularity Dashboard | Phase 2 | High | Medium |
| Autocomplete & Smart Search | Phase 2 | Medium | Low |
| Recommendation Engine | Phase 3 | High | High |
| Notification & Reminder System | Phase 3 | Medium | Medium |

---

## 5. PHASE 2 REQUIREMENTS (EVALUATION 2)

### 5.1 Dynamic Pricing System

#### 5.1.1 Description
Implement a tiered pricing mechanism where ticket prices increase as booking percentage increases.

#### 5.1.2 Business Logic
- Event manager defines pricing tiers (e.g., 0-30%: ₹500, 31-60%: ₹700, 61-100%: ₹1000)
- System automatically calculates current tier based on bookings
- Real-time price display for customers
- Historical pricing data maintained for analytics

#### 5.1.3 Database Changes
```sql
New Table: Price_Tier
- tier_id (PK)
- event_id (FK)
- tier_percentage_start
- tier_percentage_end
- price
- created_by_manager_id (FK)
- created_date

Modified Table: Ticket
- Add: current_tier_id (FK)
- Add: base_price
- Add: final_price (calculated)
```

#### 5.1.4 Key DBMS Concepts
- Database triggers to update prices on new bookings
- Stored procedures for price calculation
- Views for current pricing display
- Integrity constraints for tier overlapping prevention

#### 5.1.5 Queries Required
- Calculate current booking percentage
- Determine active price tier
- Update ticket prices on tier change
- Generate pricing analytics

---

### 5.2 Event Popularity Dashboard

#### 5.2.1 Description
Manager dashboard showing key metrics: booking trends, revenue, customer demographics, feedback summary.

#### 5.2.2 Metrics to Display
- Total bookings vs available seats
- Revenue generated (total and by tier)
- Booking velocity (bookings per day)
- Average customer rating
- Genre-wise performance
- Venue utilization rate

#### 5.2.3 Database Changes
```sql
New Tables:
Event_Analytics (view or materialized view)
- event_id
- total_bookings
- total_revenue
- avg_rating
- booking_percentage
- last_updated

Manager_Dashboard_Config
- manager_id (FK)
- event_id (FK)
- metric_name
- display_order
```

#### 5.2.4 Key DBMS Concepts
- Complex aggregate queries (GROUP BY, HAVING)
- Materialized views for performance
- Scheduled jobs for analytics refresh
- Multi-table joins

#### 5.2.5 Queries Required
- Revenue by event
- Top performing artists
- Customer retention rate
- Feedback sentiment analysis (AVG rating)
- Time-series booking data

---

### 5.3 Autocomplete & Smart Search

#### 5.3.1 Description
Type-ahead search functionality for artists, events, and venues with intelligent suggestions.

#### 5.3.2 Features
- Real-time search suggestions
- Fuzzy matching for typos
- Search history for personalized suggestions
- Popular searches displayed

#### 5.3.3 Database Changes
```sql
New Tables:
Search_History
- search_id (PK)
- customer_id (FK)
- search_query
- result_clicked
- search_timestamp

Popular_Searches
- keyword
- search_count
- last_searched
```

#### 5.3.4 Key DBMS Concepts
- LIKE and ILIKE operators
- Full-text search indexes
- Pattern matching
- Query optimization with indexes

#### 5.3.5 Queries Required
- Prefix matching (name LIKE 'arijit%')
- Ranked search results
- Popular search aggregation
- Search analytics

---

## 6. PHASE 3 REQUIREMENTS (EVALUATION 3)

### 6.1 Recommendation Engine

#### 6.1.1 Description
Personalized event recommendations based on customer preferences, booking history, and genre affinity.

#### 6.1.2 Recommendation Logic
- Genre-based matching (customer's past bookings)
- Artist similarity (customers who liked X also liked Y)
- Location preference
- Price range matching
- Trending events in customer's area

#### 6.1.3 Database Changes
```sql
New Tables:
Customer_Preference
- preference_id (PK)
- customer_id (FK)
- genre_id (FK)
- artist_id (FK)
- preference_score (calculated)
- last_updated

Recommendation_Queue
- recommendation_id (PK)
- customer_id (FK)
- event_id (FK)
- score
- reason (genre_match, artist_match, trending, etc.)
- generated_date

Customer_Event_Interaction
- interaction_id (PK)
- customer_id (FK)
- event_id (FK)
- interaction_type (viewed, bookmarked, booked)
- timestamp
```

#### 6.1.4 Key DBMS Concepts
- Collaborative filtering queries
- Weighted scoring algorithms
- Subqueries and correlated subqueries
- Window functions for ranking
- Batch processing with stored procedures

#### 6.1.5 Queries Required
- Find similar customers (based on booking patterns)
- Calculate genre affinity scores
- Rank events by recommendation score
- Generate "You may also like" suggestions
- Trending events in user's preferred genres

---

### 6.2 Notification & Reminder System

#### 6.2.1 Description
Automated notification system for event reminders, booking confirmations, price alerts, and personalized recommendations.

#### 6.2.2 Notification Types
- Booking confirmation (immediate)
- Event reminder (1 day, 1 week before)
- Price drop alert (when favorite event price decreases)
- New event by favorite artist
- Abandoned booking reminder
- Post-event feedback request

#### 6.2.3 Database Changes
```sql
New Tables:
Notification
- notification_id (PK)
- customer_id (FK)
- notification_type
- title
- message
- related_event_id (FK)
- status (pending, sent, read)
- scheduled_time
- sent_time
- delivery_method (email, SMS, push)

Notification_Preference
- customer_id (FK)
- notification_type
- is_enabled
- preferred_method

Notification_Log
- log_id (PK)
- notification_id (FK)
- delivery_status
- attempt_time
- error_message (if any)
```

#### 6.2.4 Key DBMS Concepts
- Database triggers for event-based notifications
- Scheduled jobs (cron-like) for reminders
- Transaction management for notification delivery
- Audit trails with logging
- Status tracking with enum types

#### 6.2.5 Queries Required
- Fetch pending notifications
- Identify customers needing reminders
- Track notification delivery success rate
- Generate notification schedules
- Customer engagement metrics

---

## 7. TECHNICAL ARCHITECTURE

### 7.1 Database Management System
**Recommended:** MySQL / PostgreSQL

**Justification:**
- Robust transaction support
- Rich set of built-in functions
- Trigger and stored procedure support
- Good documentation and community support
- Industry-standard for such applications

### 7.2 Application Architecture
- **Backend:** Python/Java/Node.js with database connectivity
- **Frontend:** Web-based interface (HTML/CSS/JavaScript) or Desktop application
- **Database Layer:** ORM or direct SQL queries
- **Reporting:** SQL-based reports with visualization libraries

### 7.3 Key Database Features to Implement

#### 7.3.1 Normalization
- Ensure all tables are in 3NF minimum
- Identify and document functional dependencies
- Eliminate redundancy and anomalies

#### 7.3.2 Indexing Strategy
```sql
Indexes to Create:
- Artist: name (for search)
- Event: date, venue_id (for filtering)
- Customer: email (unique), phone
- Booking: customer_id, event_id, booking_date
- Ticket: event_id, status
- Search_History: customer_id, search_timestamp
```

#### 7.3.3 Constraints
- Primary keys on all tables
- Foreign key relationships with CASCADE/RESTRICT rules
- CHECK constraints (e.g., capacity > 0, rating BETWEEN 1 AND 5)
- UNIQUE constraints (e.g., customer email, ticket seat_no per event)
- NOT NULL constraints for mandatory fields

#### 7.3.4 Triggers
```sql
Planned Triggers:
1. update_ticket_price - After booking insert, check tier and update prices
2. send_booking_confirmation - After booking insert, create notification
3. update_event_analytics - After booking/cancellation, refresh analytics
4. prevent_overbooking - Before booking insert, check venue capacity
5. log_price_changes - After price update, maintain audit trail
```

#### 7.3.5 Stored Procedures
```sql
Planned Procedures:
1. sp_calculate_price(event_id, booking_count) - Returns current tier price
2. sp_generate_recommendations(customer_id) - Populates recommendation queue
3. sp_process_pending_notifications() - Batch sends notifications
4. sp_event_revenue_report(event_id) - Generates detailed revenue analysis
5. sp_customer_booking_history(customer_id) - Detailed booking summary
```

#### 7.3.6 Views
```sql
Planned Views:
1. v_event_summary - Event with venue, type, and artist details
2. v_customer_bookings - Customer with their booking details
3. v_available_tickets - Events with available seat count
4. v_manager_dashboard - Manager's events with key metrics
5. v_trending_events - Events sorted by booking velocity
```

---

## 8. SAMPLE QUERIES DEMONSTRATION

### 8.1 Complex Queries for Evaluation

#### Query 1: Events with Maximum Bookings by Genre
```sql
SELECT g.name AS genre, e.name AS event, COUNT(b.booking_id) AS bookings
FROM Event e
JOIN Event_Type et ON e.type_id = et.type_id
JOIN Performs p ON e.event_id = p.event_id
JOIN Artist a ON p.artist_id = a.artist_id
JOIN Genre g ON a.genre_id = g.genre_id
JOIN Booking b ON e.event_id = b.event_id
GROUP BY g.name, e.name
ORDER BY bookings DESC;
```

#### Query 2: Revenue by Event with Dynamic Pricing
```sql
SELECT e.name, SUM(t.final_price) AS total_revenue,
       AVG(t.final_price) AS avg_price,
       COUNT(b.booking_id) AS tickets_sold
FROM Event e
JOIN Ticket t ON e.event_id = t.event_id
JOIN Booking b ON t.ticket_id = b.ticket_id
GROUP BY e.name
ORDER BY total_revenue DESC;
```

#### Query 3: Customer Recommendation Score
```sql
SELECT c.name, e.name AS recommended_event,
       (
           SELECT COUNT(*) FROM Booking b2
           JOIN Customer c2 ON b2.customer_id = c2.customer_id
           WHERE c2.customer_id IN (
               SELECT customer_id FROM Booking WHERE event_id IN (
                   SELECT event_id FROM Booking WHERE customer_id = c.customer_id
               )
           ) AND b2.event_id = e.event_id
       ) AS similarity_score
FROM Customer c
CROSS JOIN Event e
WHERE e.date > CURRENT_DATE
ORDER BY similarity_score DESC
LIMIT 5;
```

#### Query 4: Venue Utilization Analysis
```sql
SELECT v.name, v.capacity,
       COUNT(DISTINCT e.event_id) AS events_hosted,
       COUNT(b.booking_id) AS total_bookings,
       (COUNT(b.booking_id) * 100.0 / (v.capacity * COUNT(DISTINCT e.event_id))) AS utilization_percentage
FROM Venue v
JOIN Event e ON v.venue_id = e.venue_id
LEFT JOIN Booking b ON e.event_id = b.event_id
GROUP BY v.name, v.capacity
ORDER BY utilization_percentage DESC;
```

---

## 9. IMPLEMENTATION TIMELINE

### 9.1 Phase 2 Timeline (3-4 weeks)
| Week | Tasks | Deliverables |
|------|-------|--------------|
| 1 | Design Price_Tier schema, Create triggers for dynamic pricing | ER diagram update, DDL scripts |
| 2 | Implement pricing logic, Test with sample data | Stored procedures, Test cases |
| 3 | Build dashboard queries, Create materialized views | SQL scripts, Dashboard mockup |
| 4 | Implement search functionality, Create indexes | Search module, Performance report |

### 9.2 Phase 3 Timeline (3-4 weeks)
| Week | Tasks | Deliverables |
|------|-------|--------------|
| 1 | Design recommendation tables, Implement preference calculation | Schema updates, Algorithms |
| 2 | Build recommendation engine queries, Test with historical data | Recommendation queries, Accuracy metrics |
| 3 | Design notification system, Create triggers and jobs | Notification schema, Trigger scripts |
| 4 | Integrate all features, End-to-end testing | Complete application, Test report |

---

## 10. EVALUATION CRITERIA MAPPING

### 10.1 Phase 2 Evaluation Points
- **Database Design (30%):** Price_Tier table, Analytics views, Search tables
- **SQL Complexity (30%):** Aggregate queries, Triggers for pricing, Stored procedures
- **Normalization (15%):** Demonstrate 3NF compliance
- **Functionality (25%):** Working dynamic pricing, Dashboard with real data, Search demo

### 10.2 Phase 3 Evaluation Points
- **Advanced Queries (35%):** Recommendation algorithms, Collaborative filtering
- **Database Features (30%):** Triggers for notifications, Scheduled jobs, Transaction management
- **System Integration (20%):** All features working together seamlessly
- **Documentation (15%):** Query optimization, Index usage, Performance analysis

---

## 11. SAMPLE DATA REQUIREMENTS

### 11.1 Minimum Data for Demo
- **Artists:** 50+ (diverse genres)
- **Events:** 30+ (past and future)
- **Customers:** 100+ (with varied booking patterns)
- **Bookings:** 500+ (distributed across events)
- **Feedback:** 200+ (ratings from 1-5)
- **Venues:** 10+

### 11.2 Data Sources
- Real data from Spotify (artists, genres)
- Synthetic booking data generated programmatically
- Realistic event names and venues
- Simulated customer profiles

---

## 12. RISK ANALYSIS & MITIGATION

### 12.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Complex queries slow performance | High | Medium | Use indexes, optimize queries, materialized views |
| Trigger cascading issues | Medium | Medium | Careful trigger design, thorough testing |
| Recommendation algorithm inaccuracy | Medium | High | Start with simple rules, iterate with testing |
| Overbooking due to concurrent bookings | High | Low | Use transactions with proper isolation levels |

### 12.2 Project Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| Feature creep beyond timeline | High | Strict scope management, prioritize core features |
| Learning curve for advanced SQL | Medium | Incremental learning, peer collaboration |
| Data quality issues affecting demos | Medium | Validate synthetic data, create test scripts |

---

## 13. SUCCESS METRICS

### 13.1 Technical Metrics
- All queries execute in < 2 seconds with 1000+ records
- 100% referential integrity maintained
- Zero data anomalies (update, insert, delete)
- All triggers fire correctly on events

### 13.2 Functional Metrics
- Dynamic pricing adjusts correctly for all tier scenarios
- Recommendation engine suggests relevant events (>60% accuracy)
- Notifications sent successfully (>95% delivery rate)
- Search returns results in <500ms

### 13.3 Academic Metrics
- Demonstrate at least 10 complex SQL queries
- Use minimum 5 triggers and 5 stored procedures
- Implement at least 3 views
- Show proper use of indexes with EXPLAIN

---

## 14. DELIVERABLES

### 14.1 Phase 2 Deliverables
1. Updated ER Diagram with new tables
2. DDL scripts for all schema changes
3. Stored procedures for dynamic pricing
4. Dashboard SQL queries with sample output
5. Search functionality demonstration
6. Test cases and results document

### 14.2 Phase 3 Deliverables
1. Complete database schema with all tables
2. Recommendation engine implementation
3. Notification system with triggers
4. Complete application with all features integrated
5. Performance analysis report
6. User manual and technical documentation
7. Final presentation with live demo

---

## 15. CONCLUSION

This enhanced Artist & Event Management System demonstrates comprehensive DBMS concepts through practical application. The phased approach ensures:

1. **Gradual Complexity:** Each phase builds upon previous work
2. **Core Concepts Coverage:** Normalization, queries, triggers, procedures, views, indexes
3. **Real-world Relevance:** Features mimic industry-standard event management systems
4. **Evaluation Readiness:** Clear deliverables mapped to evaluation criteria

The project moves beyond "bare minimum" by incorporating:
- Business logic (dynamic pricing)
- Data analytics (dashboards)
- Machine learning concepts (recommendations)
- System automation (notifications)
- User experience (smart search)

Each feature is designed to showcase different aspects of database management, making this a comprehensive learning experience that meets academic requirements while building practical skills.

---

**Document Version:** 1.0  
**Last Updated:** [Current Date]  
**Status:** Approved for Phase 2 & 3 Implementation