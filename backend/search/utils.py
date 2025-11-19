# Search utility functions for typo-tolerant search
from difflib import SequenceMatcher
from django.db.models import Q
from events.models import Event, Venue
from artists.models import Artist


def fuzzy_match(query, text, threshold=0.6):
    """
    Check if query matches text with fuzzy matching
    Returns True if similarity is above threshold
    """
    if not query or not text:
        return False
    
    query = query.lower()
    text = text.lower()
    
    # Exact substring match
    if query in text:
        return True
    
    # Fuzzy match using SequenceMatcher
    ratio = SequenceMatcher(None, query, text).ratio()
    return ratio >= threshold


def calculate_similarity(query, text):
    """Calculate similarity score between query and text"""
    if not query or not text:
        return 0.0
    
    query = query.lower()
    text = text.lower()
    
    # Exact match bonus
    if query == text:
        return 1.0
    
    # Substring match bonus
    if query in text:
        return 0.9 + (len(query) / len(text)) * 0.1
    
    # Fuzzy similarity
    return SequenceMatcher(None, query, text).ratio()


def typo_tolerant_search(query, limit=10):
    """
    Perform typo-tolerant search across events, venues, and artists
    Returns suggestions with scores
    """
    if not query or len(query) < 2:
        return []
    
    results = []
    query_lower = query.lower()
    
    # Search events
    events = Event.objects.filter(
        Q(is_active=True)
    ).select_related('venue', 'event_type')[:100]
    
    for event in events:
        max_score = 0
        matched_field = None
        
        # Check event name
        name_score = calculate_similarity(query_lower, event.name)
        if name_score > max_score:
            max_score = name_score
            matched_field = 'event name'
        
        # Check venue name
        venue_score = calculate_similarity(query_lower, event.venue.name) * 0.8
        if venue_score > max_score:
            max_score = venue_score
            matched_field = 'venue'
        
        # Check event type
        type_score = calculate_similarity(query_lower, event.event_type.name) * 0.7
        if type_score > max_score:
            max_score = type_score
            matched_field = 'event type'
        
        # Check venue city
        city_score = calculate_similarity(query_lower, event.venue.city) * 0.6
        if city_score > max_score:
            max_score = city_score
            matched_field = 'city'
        
        # Check description (partial)
        if event.description and len(event.description) < 200:
            desc_score = calculate_similarity(query_lower, event.description) * 0.5
            if desc_score > max_score:
                max_score = desc_score
                matched_field = 'description'
        
        # Only include results with reasonable scores
        if max_score >= 0.5:
            results.append({
                'type': 'event',
                'id': event.id,
                'title': event.name,
                'subtitle': f"{event.venue.name} • {event.date}",
                'score': max_score,
                'matched_field': matched_field,
                'url': f'/events/{event.id}',
                'price': str(event.ticket_price) if event.ticket_price else None,
            })
    
    # Search artists
    artists = Artist.objects.all()[:100]
    
    for artist in artists:
        full_name = f"{artist.first_name} {artist.last_name}".strip() if artist.last_name else artist.first_name
        score = calculate_similarity(query_lower, full_name)
        
        if score >= 0.5:
            results.append({
                'type': 'artist',
                'id': artist.id,
                'title': full_name,
                'subtitle': f"{artist.genre.name if artist.genre else 'Artist'}",
                'score': score,
                'matched_field': 'artist name',
                'url': f'/artists/{artist.id}',
            })
    
    # Search venues
    venues = Venue.objects.filter(is_active=True)[:50]
    
    for venue in venues:
        name_score = calculate_similarity(query_lower, venue.name)
        city_score = calculate_similarity(query_lower, venue.city) * 0.7
        
        max_score = max(name_score, city_score)
        matched_field = 'venue name' if name_score > city_score else 'city'
        
        if max_score >= 0.5:
            results.append({
                'type': 'venue',
                'id': venue.id,
                'title': venue.name,
                'subtitle': f"{venue.city}, {venue.state}",
                'score': max_score,
                'matched_field': matched_field,
                'url': f'/venues/{venue.id}',
            })
    
    # Sort by score and limit
    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]
