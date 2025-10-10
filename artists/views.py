from django.shortcuts import render
from rest_framework import viewsets
from .models import Genre, Artist
from .serializers import GenreSerializer, ArtistSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer