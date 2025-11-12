// ============================================================================
// PAGINATION COMPONENT
// Page navigation
// ============================================================================

'use client';

import React from 'react';
import { Button } from './Button';

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  className?: string;
  showFirstLast?: boolean;
}

export function Pagination({
  currentPage,
  totalPages,
  onPageChange,
  className = '',
  showFirstLast = true,
}: PaginationProps) {
  const pages = getPageNumbers(currentPage, totalPages);

  return (
    <div className={`flex items-center justify-center space-x-2 ${className}`}>
      {/* First page */}
      {showFirstLast && currentPage > 1 && (
        <Button
          variant="secondary"
          size="sm"
          onClick={() => onPageChange(1)}
          aria-label="First page"
        >
          ««
        </Button>
      )}

      {/* Previous page */}
      <Button
        variant="secondary"
        size="sm"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}
        aria-label="Previous page"
      >
        «
      </Button>

      {/* Page numbers */}
      {pages.map((page, index) =>
        page === '...' ? (
          <span key={`ellipsis-${index}`} className="px-2 text-gray-500">
            ...
          </span>
        ) : (
          <Button
            key={page}
            variant={currentPage === page ? 'primary' : 'secondary'}
            size="sm"
            onClick={() => onPageChange(Number(page))}
            aria-label={`Page ${page}`}
            aria-current={currentPage === page ? 'page' : undefined}
          >
            {page}
          </Button>
        )
      )}

      {/* Next page */}
      <Button
        variant="secondary"
        size="sm"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}
        aria-label="Next page"
      >
        »
      </Button>

      {/* Last page */}
      {showFirstLast && currentPage < totalPages && (
        <Button
          variant="secondary"
          size="sm"
          onClick={() => onPageChange(totalPages)}
          aria-label="Last page"
        >
          »»
        </Button>
      )}
    </div>
  );
}

function getPageNumbers(current: number, total: number): (number | string)[] {
  const delta = 2;
  const range: (number | string)[] = [];
  const rangeWithDots: (number | string)[] = [];

  for (let i = 1; i <= total; i++) {
    if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
      range.push(i);
    }
  }

  let prev = 0;
  for (const i of range) {
    if (typeof i === 'number') {
      if (prev && i - prev > 1) {
        rangeWithDots.push('...');
      }
      rangeWithDots.push(i);
      prev = i;
    }
  }

  return rangeWithDots;
}
