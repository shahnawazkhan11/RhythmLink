// ============================================================================
// CREATE EVENT FORM MODULE
// Form for managers to create new events
// ============================================================================

'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Alert } from '@/components/ui/Alert';
import { eventsAPI } from '@/lib/api/events';
import { getErrorMessage } from '@/lib/api/client';
import type { Venue, EventType } from '@/types/api';

export function CreateEventForm() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  
  const [venues, setVenues] = useState<Venue[]>([]);
  const [eventTypes, setEventTypes] = useState<EventType[]>([]);
  const [loadingData, setLoadingData] = useState(true);
  
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    date: '',
    start_time: '',
    end_time: '',
    venue: '',
    event_type: '',
    ticket_price: '',
    max_tickets_per_customer: '10',
    is_active: true,
  });
  
  const [formErrors, setFormErrors] = useState<Record<string, string>>({});

  // Load venues and event types
  useEffect(() => {
    const loadData = async () => {
      try {
        const [venuesResponse, eventTypesData] = await Promise.all([
          eventsAPI.venues.getAll(),
          eventsAPI.eventTypes.getAll(),
        ]);
        setVenues(venuesResponse.results || []);
        // Handle both array and paginated response
        setEventTypes(Array.isArray(eventTypesData) ? eventTypesData : eventTypesData.results || []);
      } catch (err) {
        setError('Failed to load form data');
      } finally {
        setLoadingData(false);
      }
    };
    loadData();
  }, []);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value, type } = e.target;
    const checked = (e.target as HTMLInputElement).checked;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    
    // Clear field error
    if (formErrors[name]) {
      setFormErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[name];
        return newErrors;
      });
    }
    
    if (error) setError(null);
  };

  const validateForm = (): boolean => {
    const errors: Record<string, string> = {};

    if (!formData.name.trim()) errors.name = 'Event name is required';
    if (!formData.date) errors.date = 'Date is required';
    if (!formData.start_time) errors.start_time = 'Start time is required';
    if (!formData.end_time) errors.end_time = 'End time is required';
    if (!formData.venue) errors.venue = 'Venue is required';
    if (!formData.event_type) errors.event_type = 'Event type is required';
    if (!formData.ticket_price || parseFloat(formData.ticket_price) <= 0) {
      errors.ticket_price = 'Valid ticket price is required';
    }

    setFormErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsLoading(true);
    setError(null);

    try {
      // Create JSON data matching the Django model exactly
      const eventData = {
        name: formData.name.trim(),
        description: formData.description.trim(),
        date: formData.date,
        start_time: formData.start_time,
        end_time: formData.end_time,
        venue: parseInt(formData.venue),
        event_type: parseInt(formData.event_type),
        ticket_price: parseFloat(formData.ticket_price).toFixed(2),
        max_tickets_per_customer: parseInt(formData.max_tickets_per_customer),
        is_active: formData.is_active,
      };

      const response = await eventsAPI.create(eventData as any);
      setSuccess(true);
      
      // Redirect to events list after short delay
      setTimeout(() => {
        router.push('/manager');
      }, 2000);
    } catch (err: any) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  if (loadingData) {
    return <div className="text-center py-8">Loading form data...</div>;
  }

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Create New Event</h2>

        {error && (
          <div className="mb-6">
            <Alert type="error" message={error} onClose={() => setError(null)} />
          </div>
        )}

        {success && (
          <div className="mb-6">
            <Alert type="success" message="Event created successfully! Redirecting..." />
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <Input
            label="Event Name"
            name="name"
            type="text"
            value={formData.name}
            onChange={handleChange}
            error={formErrors.name}
            required
            placeholder="Enter event name"
            disabled={isLoading}
          />

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter event description"
              disabled={isLoading}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Date"
              name="date"
              type="date"
              value={formData.date}
              onChange={handleChange}
              error={formErrors.date}
              required
              disabled={isLoading}
            />

            <Input
              label="Ticket Price ($)"
              name="ticket_price"
              type="number"
              step="0.01"
              value={formData.ticket_price}
              onChange={handleChange}
              error={formErrors.ticket_price}
              required
              placeholder="0.00"
              disabled={isLoading}
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input
              label="Start Time"
              name="start_time"
              type="time"
              value={formData.start_time}
              onChange={handleChange}
              error={formErrors.start_time}
              required
              disabled={isLoading}
            />

            <Input
              label="End Time"
              name="end_time"
              type="time"
              value={formData.end_time}
              onChange={handleChange}
              error={formErrors.end_time}
              required
              disabled={isLoading}
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Venue <span className="text-red-500">*</span>
            </label>
            <select
              name="venue"
              value={formData.venue}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              disabled={isLoading}
            >
              <option value="">Select a venue</option>
              {venues.map((venue) => (
                <option key={venue.id} value={venue.id}>
                  {venue.name} - {venue.city} (Capacity: {venue.capacity})
                </option>
              ))}
            </select>
            {formErrors.venue && (
              <p className="mt-1 text-sm text-red-600">{formErrors.venue}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Event Type <span className="text-red-500">*</span>
            </label>
            <select
              name="event_type"
              value={formData.event_type}
              onChange={handleChange}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              required
              disabled={isLoading}
            >
              <option value="">Select event type</option>
              {eventTypes.map((type) => (
                <option key={type.id} value={type.id}>
                  {type.name}
                </option>
              ))}
            </select>
            {formErrors.event_type && (
              <p className="mt-1 text-sm text-red-600">{formErrors.event_type}</p>
            )}
          </div>

          <Input
            label="Max Tickets Per Customer"
            name="max_tickets_per_customer"
            type="number"
            min="1"
            value={formData.max_tickets_per_customer}
            onChange={handleChange}
            required
            disabled={isLoading}
          />

          <div className="flex items-center">
            <input
              type="checkbox"
              name="is_active"
              checked={formData.is_active}
              onChange={handleChange}
              className="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
              disabled={isLoading}
            />
            <label className="ml-2 text-sm text-gray-700">
              Active (visible to customers)
            </label>
          </div>

          <div className="flex gap-4 pt-4">
            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="flex-1"
              isLoading={isLoading}
              disabled={isLoading || success}
            >
              Create Event
            </Button>
            
            <Button
              type="button"
              variant="secondary"
              size="lg"
              onClick={() => router.back()}
              disabled={isLoading}
            >
              Cancel
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
