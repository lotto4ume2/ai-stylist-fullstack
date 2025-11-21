// User and Authentication Types
export interface User {
  id: string;
  email: string;
  full_name?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user_id: string;
  email: string;
}

export interface SignupData {
  email: string;
  password: string;
  full_name?: string;
}

export interface LoginData {
  email: string;
  password: string;
}

// Clothing Item Types
export interface ClothingItem {
  id: string;
  user_id: string;
  image_url: string;
  category?: string;
  color?: string;
  brand?: string;
  notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface ClothingItemCreate {
  category?: string;
  color?: string;
  brand?: string;
  notes?: string;
}

export interface UploadResponse {
  message: string;
  item: ClothingItem;
}

export interface ItemsResponse {
  items: ClothingItem[];
  count: number;
}

// API Error Types
export interface ApiError {
  detail: string;
}
