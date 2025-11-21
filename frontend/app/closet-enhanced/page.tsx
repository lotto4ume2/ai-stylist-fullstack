"use client";

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth-context';
import { api } from '@/lib/api';
import Navbar from '@/components/Navbar';

interface ClothingItem {
  id: string;
  image_url: string;
  category?: string;
  color?: string;
  brand?: string;
  notes?: string;
  is_favorite?: boolean;
  created_at: string;
}

export default function EnhancedClosetPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [items, setItems] = useState<ClothingItem[]>([]);
  const [filteredItems, setFilteredItems] = useState<ClothingItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedItem, setSelectedItem] = useState<ClothingItem | null>(null);
  
  // Filter states
  const [searchQuery, setSearchQuery] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [colorFilter, setColorFilter] = useState('');
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
  const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  useEffect(() => {
    if (user) {
      fetchItems();
    }
  }, [user]);

  useEffect(() => {
    applyFilters();
  }, [items, searchQuery, categoryFilter, colorFilter, showFavoritesOnly]);

  const fetchItems = async () => {
    try {
      setIsLoading(true);
      const response = await api.getItems();
      setItems(response.items);
      setFilteredItems(response.items);
    } catch (err: any) {
      setError(err.message || 'Failed to load items');
    } finally {
      setIsLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...items];

    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter(item =>
        item.category?.toLowerCase().includes(query) ||
        item.color?.toLowerCase().includes(query) ||
        item.brand?.toLowerCase().includes(query) ||
        item.notes?.toLowerCase().includes(query)
      );
    }

    if (categoryFilter) {
      filtered = filtered.filter(item => item.category === categoryFilter);
    }

    if (colorFilter) {
      filtered = filtered.filter(item => item.color === colorFilter);
    }

    if (showFavoritesOnly) {
      filtered = filtered.filter(item => item.is_favorite);
    }

    setFilteredItems(filtered);
  };

  const toggleFavorite = async (itemId: string) => {
    try {
      await api.toggleFavorite(itemId);
      // Update local state
      setItems(items.map(item =>
        item.id === itemId ? { ...item, is_favorite: !item.is_favorite } : item
      ));
    } catch (err: any) {
      setError(err.message || 'Failed to update favorite');
    }
  };

  const handleDelete = async (itemId: string) => {
    if (!confirm('Are you sure you want to delete this item?')) return;

    try {
      await api.deleteItem(itemId);
      setItems(items.filter(item => item.id !== itemId));
    } catch (err: any) {
      setError(err.message || 'Failed to delete item');
    }
  };

  const getUniqueCategories = () => {
    const categories = items.map(item => item.category).filter(Boolean);
    return Array.from(new Set(categories));
  };

  const getUniqueColors = () => {
    const colors = items.map(item => item.color).filter(Boolean);
    return Array.from(new Set(colors));
  };

  if (loading || isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800">
        <Navbar />
        <div className="flex items-center justify-center h-[calc(100vh-64px)]">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50 dark:from-gray-900 dark:to-gray-800 transition-colors duration-300">
      <Navbar />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            My Closet
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            {filteredItems.length} {filteredItems.length === 1 ? 'item' : 'items'}
          </p>
        </div>

        {/* Filters */}
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 transition-all duration-300">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-4">
            {/* Search */}
            <input
              type="text"
              placeholder="Search items..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white transition-all duration-200"
            />

            {/* Category Filter */}
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white transition-all duration-200"
            >
              <option value="">All Categories</option>
              {getUniqueCategories().map(cat => (
                <option key={cat} value={cat}>{cat}</option>
              ))}
            </select>

            {/* Color Filter */}
            <select
              value={colorFilter}
              onChange={(e) => setColorFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent dark:bg-gray-700 dark:text-white transition-all duration-200"
            >
              <option value="">All Colors</option>
              {getUniqueColors().map(color => (
                <option key={color} value={color}>{color}</option>
              ))}
            </select>

            {/* View Mode Toggle */}
            <div className="flex gap-2">
              <button
                onClick={() => setViewMode('grid')}
                className={`flex-1 px-4 py-2 rounded-lg transition-all duration-200 ${
                  viewMode === 'grid'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                Grid
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`flex-1 px-4 py-2 rounded-lg transition-all duration-200 ${
                  viewMode === 'list'
                    ? 'bg-purple-600 text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                }`}
              >
                List
              </button>
            </div>
          </div>

          {/* Favorites Toggle */}
          <label className="flex items-center cursor-pointer">
            <input
              type="checkbox"
              checked={showFavoritesOnly}
              onChange={(e) => setShowFavoritesOnly(e.target.checked)}
              className="w-5 h-5 text-purple-600 rounded focus:ring-2 focus:ring-purple-500"
            />
            <span className="ml-2 text-gray-700 dark:text-gray-300">
              Show favorites only
            </span>
          </label>
        </div>

        {error && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 text-red-600 dark:text-red-400 px-4 py-3 rounded-lg mb-6 animate-fade-in">
            {error}
          </div>
        )}

        {/* Items Grid/List */}
        {filteredItems.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-gray-600 dark:text-gray-400 text-lg">
              No items found. Try adjusting your filters or add new items!
            </p>
          </div>
        ) : (
          <div className={
            viewMode === 'grid'
              ? 'grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
              : 'space-y-4'
          }>
            {filteredItems.map((item, index) => (
              <div
                key={item.id}
                className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 animate-fade-in"
                style={{ animationDelay: `${index * 50}ms` }}
              >
                <div className="relative">
                  <img
                    src={item.image_url}
                    alt={item.category || 'Clothing item'}
                    className="w-full h-64 object-cover"
                  />
                  <button
                    onClick={() => toggleFavorite(item.id)}
                    className="absolute top-2 right-2 p-2 bg-white dark:bg-gray-800 rounded-full shadow-lg hover:scale-110 transition-transform duration-200"
                  >
                    <span className="text-2xl">
                      {item.is_favorite ? '❤️' : '🤍'}
                    </span>
                  </button>
                </div>
                
                <div className="p-4">
                  {item.category && (
                    <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-1">
                      {item.category}
                    </h3>
                  )}
                  {item.color && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">
                      Color: {item.color}
                    </p>
                  )}
                  {item.brand && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                      Brand: {item.brand}
                    </p>
                  )}
                  {item.notes && (
                    <p className="text-sm text-gray-500 dark:text-gray-500 mb-3">
                      {item.notes}
                    </p>
                  )}
                  
                  <button
                    onClick={() => handleDelete(item.id)}
                    className="w-full px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors duration-200"
                  >
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
