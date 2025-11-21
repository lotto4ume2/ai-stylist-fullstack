'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authApi, handleApiError } from './api';
import { User, SignupData, LoginData } from '@/types';
import toast from 'react-hot-toast';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (data: LoginData) => Promise<void>;
  signup: (data: SignupData) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  // Check for existing session on mount
  useEffect(() => {
    const initializeAuth = () => {
      if (typeof window !== 'undefined') {
        const token = localStorage.getItem('access_token');
        const userEmail = localStorage.getItem('user_email');
        const userId = localStorage.getItem('user_id');

        if (token && userEmail && userId) {
          setUser({
            id: userId,
            email: userEmail,
          });
        }
      }
      setLoading(false);
    };

    initializeAuth();
  }, []);

  const login = async (data: LoginData) => {
    try {
      const response = await authApi.login(data);
      
      // Store auth data
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user_email', response.email);
      localStorage.setItem('user_id', response.user_id);

      setUser({
        id: response.user_id,
        email: response.email,
      });

      toast.success('Login successful!');
      router.push('/closet');
    } catch (error) {
      const errorMessage = handleApiError(error);
      toast.error(errorMessage);
      throw error;
    }
  };

  const signup = async (data: SignupData) => {
    try {
      const response = await authApi.signup(data);
      
      // Store auth data
      localStorage.setItem('access_token', response.access_token);
      localStorage.setItem('user_email', response.email);
      localStorage.setItem('user_id', response.user_id);

      setUser({
        id: response.user_id,
        email: response.email,
        full_name: data.full_name,
      });

      toast.success('Account created successfully!');
      router.push('/closet');
    } catch (error) {
      const errorMessage = handleApiError(error);
      toast.error(errorMessage);
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    localStorage.removeItem('user_id');
    setUser(null);
    toast.success('Logged out successfully');
    router.push('/');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        login,
        signup,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
