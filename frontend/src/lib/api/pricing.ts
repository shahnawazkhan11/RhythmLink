// ============================================================================
// PRICING API
// All pricing-related API calls
// ============================================================================

import { apiClient } from './client';
import type { PriceTier, CurrentPrice } from '@/types/api';

// ============================================================================
// PRICE TIERS
// ============================================================================

/**
 * Get price tiers for an event
 * GET /api/pricing/tiers/{event_id}/
 */
export async function getPriceTiers(eventId: number): Promise<PriceTier[]> {
  return apiClient.get<PriceTier[]>(`/api/pricing/tiers/${eventId}/`);
}

/**
 * Create price tier for an event
 * POST /api/pricing/tiers/{event_id}/
 */
export async function createPriceTier(
  eventId: number,
  data: {
    tier_name: string;
    tickets_sold_threshold: number;
    price_multiplier: string;
  }
): Promise<PriceTier> {
  return apiClient.post<PriceTier>(`/api/pricing/tiers/${eventId}/`, data);
}

/**
 * Update price tier
 * PATCH /api/pricing/tiers/{event_id}/{tier_id}/
 */
export async function updatePriceTier(
  eventId: number,
  tierId: number,
  data: Partial<PriceTier>
): Promise<PriceTier> {
  return apiClient.patch<PriceTier>(`/api/pricing/tiers/${eventId}/${tierId}/`, data);
}

/**
 * Delete price tier
 * DELETE /api/pricing/tiers/{event_id}/{tier_id}/
 */
export async function deletePriceTier(eventId: number, tierId: number): Promise<void> {
  return apiClient.delete<void>(`/api/pricing/tiers/${eventId}/${tierId}/`);
}

// ============================================================================
// CURRENT PRICE
// ============================================================================

/**
 * Get current price for an event (with dynamic pricing)
 * GET /api/pricing/current-price/{event_id}/
 */
export async function getCurrentPrice(eventId: number): Promise<CurrentPrice> {
  return apiClient.get<CurrentPrice>(`/api/pricing/current-price/${eventId}/`);
}

// ============================================================================
// PRICING API OBJECT (ALTERNATIVE EXPORT)
// ============================================================================

export const pricingAPI = {
  // Price Tiers
  getTiers: getPriceTiers,
  createTier: createPriceTier,
  updateTier: updatePriceTier,
  deleteTier: deletePriceTier,
  
  // Current Price
  getCurrentPrice,
};
