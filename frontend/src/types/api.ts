// ============================================================================
// RHYTHMLINK API TYPES
// TypeScript interfaces for backend API models
// ============================================================================

// ============================================================================
// USER & AUTHENTICATION
// ============================================================================

export type UserRole = 'customer' | 'manager' | 'admin';

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  is_active: boolean;
  date_joined: string;
}

export interface UserProfile {
  id: number;
  user: number;
  phone: string;
  date_of_birth: string;
  profile_picture?: string;
  bio?: string;
  created_at: string;
  updated_at: string;
}

export interface UserWithProfile extends User {
  profile: UserProfile;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  role: UserRole;
  phone: string;
  date_of_birth: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  user: UserWithProfile;
  message: string;
}

// ============================================================================
// GENRE & ARTISTS
// ============================================================================

export interface Genre {
  id: number;
  name: string;
  description?: string;
  created_at: string;
}

export interface Artist {
  id: number;
  name: string;
  genre: number;
  genre_name?: string;
  contact_email: string;
  contact_phone: string;
  bio?: string;
  image?: string;
  followers?: number;
  popularity?: number;
  social_media_links?: {
    facebook?: string;
    instagram?: string;
    twitter?: string;
    spotify?: string;
  };
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Album {
  id: number;
  artist: number;
  artist_name?: string;
  title: string;
  release_date: string;
  cover_image?: string;
  description?: string;
  created_at: string;
}

export interface Track {
  id: number;
  album: number;
  album_title?: string;
  artist_name?: string;
  title: string;
  duration: number;
  track_number?: number;
  audio_file?: string;
  created_at: string;
}

// ============================================================================
// VENUES & EVENTS
// ============================================================================

export interface Venue {
  id: number;
  name: string;
  location: string;
  address: string;
  city: string;
  state: string;
  capacity: number;
  amenities: string[];
  contact_email: string;
  contact_phone: string;
  latitude?: number;
  longitude?: number;
  is_active: boolean;
  created_at: string;
}

export interface EventType {
  id: number;
  name: string;
  description?: string;
}

export interface Event {
  id: number;
  name: string;
  description: string;
  date: string;
  start_time: string;
  end_time: string;
  venue: number;
  venue_name?: string;
  venue_details?: Venue;
  event_type: number;
  event_type_name?: string;
  poster_image?: string;
  ticket_price: string;
  max_tickets_per_customer: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

// ============================================================================
// TICKETS & BOOKINGS
// ============================================================================

export type TicketStatus = 'available' | 'booked' | 'cancelled';
export type BookingStatus = 'pending' | 'confirmed' | 'cancelled' | 'refunded';

export interface Ticket {
  id: number;
  event: number;
  event_name?: string;
  seat_number: string;
  price: string;
  status: TicketStatus;
  booking?: number;
  created_at: string;
}

export interface Booking {
  id: number;
  customer: number;
  customer_name?: string;
  event: number;
  event_name?: string;
  event_details?: Event;
  tickets: number[];
  ticket_details?: Ticket[];
  total_amount: string;
  booking_date: string;
  status: BookingStatus;
  payment_reference?: string;
  special_requests?: string;
}

export interface BookingRequest {
  event: number;
  tickets: number[];
  total_amount: string;
  special_requests?: string;
}

// ============================================================================
// PRICING
// ============================================================================

export interface PriceTier {
  id: number;
  event: number;
  tier_name: string;
  tickets_sold_threshold: number;
  price_multiplier: string;
  is_active: boolean;
  created_at: string;
}

export interface CurrentPrice {
  event_id: number;
  event_name: string;
  base_price: string;
  current_price: string;
  tickets_sold: number;
  total_tickets: number;
  current_tier: string;
  next_tier?: string;
  tickets_to_next_tier?: number;
  price_increase_percentage: string;
}

// ============================================================================
// SEARCH
// ============================================================================

export interface SearchResult {
  events: Event[];
  artists: Artist[];
  venues: Venue[];
  query: string;
  total_results: number;
}

export interface PopularSearch {
  id: number;
  search_query: string;
  search_count: number;
  last_searched: string;
}

// ============================================================================
// ANALYTICS
// ============================================================================

export interface EventAnalytics {
  event_id: number;
  event_name: string;
  total_bookings: number;
  total_tickets_sold: number;
  total_revenue: string;
  average_booking_value: string;
  booking_status_breakdown: {
    pending: number;
    confirmed: number;
    cancelled: number;
    refunded: number;
  };
  revenue_by_date: Array<{
    date: string;
    revenue: string;
  }>;
  peak_booking_hours: Array<{
    hour: number;
    bookings: number;
  }>;
  customer_demographics?: {
    age_groups: Record<string, number>;
    repeat_customers: number;
  };
}

export interface ManagerDashboard {
  total_events: number;
  active_events: number;
  total_revenue: string;
  total_bookings: number;
  upcoming_events: Event[];
  top_performing_events: Array<{
    event: Event;
    revenue: string;
    tickets_sold: number;
  }>;
  recent_bookings: Booking[];
  revenue_trend: Array<{
    date: string;
    revenue: string;
  }>;
}

// ============================================================================
// FEEDBACK & INTERACTIONS
// ============================================================================

export interface Feedback {
  id: number;
  customer: number;
  customer_name?: string;
  event: number;
  event_name?: string;
  rating: number;
  comment?: string;
  created_at: string;
}

export interface FanInteraction {
  id: number;
  customer: number;
  artist: number;
  interaction_type: 'follow' | 'like' | 'comment' | 'share';
  interaction_date: string;
  metadata?: Record<string, any>;
}

// ============================================================================
// PAGINATION & RESPONSES
// ============================================================================

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface APIError {
  detail?: string;
  message?: string;
  error?: string;
  [key: string]: any;
}

export interface APIResponse<T> {
  data?: T;
  message?: string;
  success: boolean;
}
