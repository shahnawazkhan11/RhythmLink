from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import typo_tolerant_search


@api_view(['GET'])
def autocomplete_search(request):
    """
    Autocomplete search endpoint with typo tolerance
    GET /api/search/autocomplete/?q=concert
    """
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return Response({
            'query': query,
            'results': [],
            'count': 0,
            'message': 'Query too short (minimum 2 characters)'
        })
    
    try:
        results = typo_tolerant_search(query, limit=10)
        
        return Response({
            'query': query,
            'results': results,
            'count': len(results)
        })
    except Exception as e:
        return Response({
            'query': query,
            'results': [],
            'count': 0,
            'error': str(e)
        }, status=500)
from django.db.models import Q, F
from rest_framework import generics
from rest_framework.response import Response
from events.models import Event, Venue
from artists.models import Artist
from .models import SearchHistory, PopularSearches


class AutocompleteView(generics.ListAPIView):
    """Autocomplete search across artists, events, and venues"""
    
    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return Response({
                'query': query,
                'results': [],
                'message': 'Query too short (minimum 2 characters)'
            })
        
        # Prefix matching across different entities
        artists = Artist.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query),
            is_active=True
        ).values('id', 'name', 'genre__name')[:5]
        
        events = Event.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query),
            is_active=True
        ).values('id', 'name', 'date', 'venue__name')[:5]
        
        venues = Venue.objects.filter(
            Q(name__istartswith=query) | Q(name__icontains=query) | Q(city__icontains=query),
            is_active=True
        ).values('id', 'name', 'city', 'capacity')[:5]
        
        # Format results
        results = []
        
        for artist in artists:
            results.append({
                'type': 'artist',
                'id': artist['id'],
                'name': artist['name'],
                'genre': artist['genre__name'],
                'url': f'/api/artists/artists/{artist["id"]}/'
            })
        
        for event in events:
            results.append({
                'type': 'event',
                'id': event['id'],
                'name': event['name'],
                'date': event['date'],
                'venue': event['venue__name'],
                'url': f'/api/events/events/{event["id"]}/'
            })
        
        for venue in venues:
            results.append({
                'type': 'venue',
                'id': venue['id'],
                'name': venue['name'],
                'city': venue['city'],
                'capacity': venue['capacity'],
                'url': f'/api/events/venues/{venue["id"]}/'
            })
        
        # Track search history (if user is authenticated)
        if request.user.is_authenticated:
            SearchHistory.objects.create(
                user=request.user,
                search_query=query,
                result_clicked=False
            )
        
        # Update popular searches
        popular_search, created = PopularSearches.objects.get_or_create(
            keyword=query.lower()
        )
        if not created:
            popular_search.search_count = F('search_count') + 1
            popular_search.save()
        
        return Response({
            'query': query,
            'count': len(results),
            'results': results
        })


class PopularSearchesView(generics.ListAPIView):
    """Get most popular search terms"""
    
    def get(self, request):
        limit = int(request.GET.get('limit', 10))
        
        popular = PopularSearches.objects.all().order_by('-search_count')[:limit]
        
        results = [{
            'keyword': item.keyword,
            'search_count': item.search_count,
            'last_searched': item.last_searched
        } for item in popular]
        
        return Response({
            'popular_searches': results
        })