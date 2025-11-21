import axios, { AxiosError } from 'axios';
import {
  AuthResponse,
  SignupData,
  LoginData,
  UploadResponse,
  ItemsResponse,
  ApiError,
} from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Handle API errors
export const handleApiError = (error: unknown): string => {
  if (axios.isAxiosError(error)) {
    const axiosError = error as AxiosError<ApiError>;
    return axiosError.response?.data?.detail || 'An error occurred';
  }
  return 'An unexpected error occurred';
};

// Authentication API
export const authApi = {
  signup: async (data: SignupData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/signup', data);
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/api/auth/login', data);
    return response.data;
  },
};

// Clothing Items API
export const itemsApi = {
  upload: async (
    file: File,
    metadata: {
      category?: string;
      color?: string;
      brand?: string;
      notes?: string;
    }
  ): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    
    if (metadata.category) formData.append('category', metadata.category);
    if (metadata.color) formData.append('color', metadata.color);
    if (metadata.brand) formData.append('brand', metadata.brand);
    if (metadata.notes) formData.append('notes', metadata.notes);

    const token = localStorage.getItem('access_token');
    const response = await axios.post<UploadResponse>(
      `${API_URL}/api/items/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  },

  getAll: async (): Promise<ItemsResponse> => {
    const response = await api.get<ItemsResponse>('/api/items');
    return response.data;
  },

  delete: async (itemId: string): Promise<{ message: string }> => {
    const response = await api.delete<{ message: string }>(
      `/api/items/${itemId}`
    );
    return response.data;
  },

  toggleFavorite: async (itemId: string): Promise<{ message: string; is_favorite: boolean }> => {
    const response = await api.post<{ message: string; is_favorite: boolean }>(
      `/api/items/${itemId}/favorite`
    );
    return response.data;
  },

  search: async (params: {
    query?: string;
    category?: string;
    color?: string;
    brand?: string;
    is_favorite?: boolean;
  }): Promise<ItemsResponse> => {
    const response = await api.get<ItemsResponse>('/api/items/search', { params });
    return response.data;
  },
};

// AI Recommendations API
export const recommendationsApi = {
  getOutfits: async (params?: {
    occasion?: string;
    weather?: string;
    style_preference?: string;
  }): Promise<any> => {
    const response = await api.post('/api/recommendations/outfits', null, { params });
    return response.data;
  },

  analyzeCloset: async (): Promise<any> => {
    const response = await api.get('/api/recommendations/closet-analysis');
    return response.data;
  },
};

// Weather API
export const weatherApi = {
  getRecommendations: async (location?: string): Promise<any> => {
    const response = await api.get('/api/weather/recommendations', {
      params: location ? { location } : undefined,
    });
    return response.data;
  },
};

export default api;
