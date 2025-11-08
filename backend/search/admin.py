from django.contrib import admin
from .models import SearchHistory, PopularSearches


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'search_query', 'result_clicked', 'search_timestamp']
    list_filter = ['result_clicked', 'search_timestamp']
    search_fields = ['search_query', 'user__username']
    readonly_fields = ['search_timestamp']


@admin.register(PopularSearches)
class PopularSearchesAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'search_count', 'last_searched']
    search_fields = ['keyword']
    readonly_fields = ['last_searched']
    ordering = ['-search_count']