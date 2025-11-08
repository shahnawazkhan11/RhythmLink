#!/usr/bin/env python
import os
import sys
import django
from pathlib import Path

# Add the project directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

try:
    django.setup()
    print("✅ Django setup successful!")
    
    # Test importing models
    from accounts.models import UserProfile
    print("✅ Accounts models imported successfully!")
    
    from artists.models import Genre, Artist
    print("✅ Artists models imported successfully!")
    
    from events.models import Event, Venue, EventType
    print("✅ Events models imported successfully!")
    
    from customers.models import Customer, Ticket, Booking, Feedback
    print("✅ Customers models imported successfully!")
    
    from pricing.models import PriceTier, PriceHistory
    print("✅ Pricing models imported successfully!")
    
    from analytics.models import EventAnalytics
    print("✅ Analytics models imported successfully!")
    
    from search.models import SearchHistory, PopularSearches
    print("✅ Search models imported successfully!")
    
    print("\n🎉 All models loaded successfully! Ready for makemigrations.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()