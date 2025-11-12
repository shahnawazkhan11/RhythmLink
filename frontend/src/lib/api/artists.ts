// ============================================================================
// ARTISTS API
// All artists-related API calls
// ============================================================================

import { apiClient } from './client';
import type { Artist, Genre, Album, Track, PaginatedResponse } from '@/types/api';

// ============================================================================
// ARTISTS
// ============================================================================

/**
 * Get all artists with optional filters
 * GET /api/artists/artists/
 */
export async function getArtists(params?: {
  page?: number;
  search?: string;
  genre?: number;
  is_active?: boolean;
}): Promise<PaginatedResponse<Artist>> {
  return apiClient.get<PaginatedResponse<Artist>>('/api/artists/artists/', params);
}

/**
 * Get single artist by ID
 * GET /api/artists/artists/{id}/
 */
export async function getArtist(id: number): Promise<Artist> {
  return apiClient.get<Artist>(`/api/artists/artists/${id}/`);
}

/**
 * Create new artist
 * POST /api/artists/artists/
 */
export async function createArtist(data: FormData): Promise<Artist> {
  return apiClient.post<Artist>('/api/artists/artists/', data);
}

/**
 * Update artist
 * PUT /api/artists/artists/{id}/
 */
export async function updateArtist(id: number, data: FormData): Promise<Artist> {
  return apiClient.put<Artist>(`/api/artists/artists/${id}/`, data);
}

/**
 * Delete artist
 * DELETE /api/artists/artists/{id}/
 */
export async function deleteArtist(id: number): Promise<void> {
  return apiClient.delete<void>(`/api/artists/artists/${id}/`);
}

// ============================================================================
// GENRES
// ============================================================================

/**
 * Get all genres
 * GET /api/artists/genres/
 */
export async function getGenres(): Promise<Genre[]> {
  return apiClient.get<Genre[]>('/api/artists/genres/');
}

/**
 * Get single genre by ID
 * GET /api/artists/genres/{id}/
 */
export async function getGenre(id: number): Promise<Genre> {
  return apiClient.get<Genre>(`/api/artists/genres/${id}/`);
}

/**
 * Create new genre
 * POST /api/artists/genres/
 */
export async function createGenre(data: { name: string; description?: string }): Promise<Genre> {
  return apiClient.post<Genre>('/api/artists/genres/', data);
}

// ============================================================================
// ALBUMS
// ============================================================================

/**
 * Get all albums
 * GET /api/artists/albums/
 */
export async function getAlbums(params?: {
  page?: number;
  artist?: number;
  search?: string;
}): Promise<PaginatedResponse<Album>> {
  return apiClient.get<PaginatedResponse<Album>>('/api/artists/albums/', params);
}

/**
 * Get single album by ID
 * GET /api/artists/albums/{id}/
 */
export async function getAlbum(id: number): Promise<Album> {
  return apiClient.get<Album>(`/api/artists/albums/${id}/`);
}

/**
 * Create new album
 * POST /api/artists/albums/
 */
export async function createAlbum(data: FormData): Promise<Album> {
  return apiClient.post<Album>('/api/artists/albums/', data);
}

// ============================================================================
// TRACKS
// ============================================================================

/**
 * Get all tracks
 * GET /api/artists/tracks/
 */
export async function getTracks(params?: {
  page?: number;
  album?: number;
  artist?: number;
  search?: string;
}): Promise<PaginatedResponse<Track>> {
  return apiClient.get<PaginatedResponse<Track>>('/api/artists/tracks/', params);
}

/**
 * Get single track by ID
 * GET /api/artists/tracks/{id}/
 */
export async function getTrack(id: number): Promise<Track> {
  return apiClient.get<Track>(`/api/artists/tracks/${id}/`);
}

/**
 * Create new track
 * POST /api/artists/tracks/
 */
export async function createTrack(data: FormData): Promise<Track> {
  return apiClient.post<Track>('/api/artists/tracks/', data);
}

// ============================================================================
// ARTISTS API OBJECT (ALTERNATIVE EXPORT)
// ============================================================================

export const artistsAPI = {
  // Artists
  getAll: getArtists,
  getById: getArtist,
  create: createArtist,
  update: updateArtist,
  delete: deleteArtist,
  
  // Genres
  genres: {
    getAll: getGenres,
    getById: getGenre,
    create: createGenre,
  },
  
  // Albums
  albums: {
    getAll: getAlbums,
    getById: getAlbum,
    create: createAlbum,
  },
  
  // Tracks
  tracks: {
    getAll: getTracks,
    getById: getTrack,
    create: createTrack,
  },
};
