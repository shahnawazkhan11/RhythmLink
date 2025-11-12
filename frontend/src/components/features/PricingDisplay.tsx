// ============================================================================
// PRICING DISPLAY COMPONENT
// Show dynamic pricing information
// ============================================================================

'use client';

import React from 'react';
import { CurrentPrice, PriceTier } from '@/types/api';
import { formatCurrency } from '@/lib/utils/formatters';
import { Card, CardHeader, CardBody } from '../ui/Card';
import { Badge } from '../ui/Badge';

interface PricingDisplayProps {
  pricing: CurrentPrice;
  className?: string;
}

export function PricingDisplay({ pricing, className = '' }: PricingDisplayProps) {
  const soldPercentage = (pricing.tickets_sold / pricing.total_tickets) * 100;
  const priceIncrease = parseFloat(pricing.price_increase_percentage);

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-semibold text-gray-900">Dynamic Pricing</h3>
          <Badge variant={priceIncrease > 0 ? 'warning' : 'success'}>
            {pricing.current_tier}
          </Badge>
        </div>
      </CardHeader>

      <CardBody>
        <div className="space-y-4">
          {/* Current price */}
          <div>
            <div className="flex items-baseline justify-between mb-1">
              <span className="text-2xl font-bold text-blue-600">
                {formatCurrency(parseFloat(pricing.current_price))}
              </span>
              {priceIncrease > 0 && (
                <span className="text-sm text-gray-500 line-through">
                  {formatCurrency(parseFloat(pricing.base_price))}
                </span>
              )}
            </div>
            {priceIncrease > 0 && (
              <p className="text-sm text-orange-600">
                +{priceIncrease.toFixed(0)}% from base price
              </p>
            )}
          </div>

          {/* Tickets sold progress */}
          <div>
            <div className="flex justify-between text-sm text-gray-600 mb-1">
              <span>Tickets Sold</span>
              <span>
                {pricing.tickets_sold} / {pricing.total_tickets}
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                style={{ width: `${soldPercentage}%` }}
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">{soldPercentage.toFixed(1)}% sold</p>
          </div>

          {/* Next tier info */}
          {pricing.next_tier && pricing.tickets_to_next_tier !== undefined && (
            <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
              <p className="text-sm text-yellow-800">
                <strong>Price will increase</strong> after {pricing.tickets_to_next_tier} more
                ticket{pricing.tickets_to_next_tier !== 1 ? 's' : ''} sold
              </p>
              <p className="text-xs text-yellow-700 mt-1">Next tier: {pricing.next_tier}</p>
            </div>
          )}
        </div>
      </CardBody>
    </Card>
  );
}

interface PriceTierListProps {
  tiers: PriceTier[];
  currentTier?: string;
  className?: string;
}

export function PriceTierList({ tiers, currentTier, className = '' }: PriceTierListProps) {
  return (
    <div className={`space-y-2 ${className}`}>
      {tiers.map((tier) => {
        const isActive = tier.tier_name === currentTier;
        const multiplier = parseFloat(tier.price_multiplier);

        return (
          <div
            key={tier.id}
            className={`
              flex justify-between items-center p-3 rounded-lg border
              ${isActive ? 'border-blue-500 bg-blue-50' : 'border-gray-200 bg-white'}
            `}
          >
            <div>
              <div className="flex items-center space-x-2">
                <span className="font-medium text-gray-900">{tier.tier_name}</span>
                {isActive && <Badge variant="info">Current</Badge>}
                {!tier.is_active && <Badge variant="danger">Inactive</Badge>}
              </div>
              <p className="text-sm text-gray-600">
                After {tier.tickets_sold_threshold} tickets sold
              </p>
            </div>
            <div className="text-right">
              <div className="font-semibold text-gray-900">
                {multiplier === 1 ? 'Base' : `${((multiplier - 1) * 100).toFixed(0)}%`}
              </div>
              <p className="text-xs text-gray-500">
                {multiplier === 1 ? 'price' : 'increase'}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
