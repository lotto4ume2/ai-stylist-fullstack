'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import ProtectedRoute from '@/components/ProtectedRoute';
import Navbar from '@/components/Navbar';
import { itemsApi, handleApiError } from '@/lib/api';
import { ClothingItem } from '@/types';
import toast from 'react-hot-toast';

export default function ClosetPage() {
  const [items, setItems] = useState<ClothingItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState<string | null>(null);

  useEffect(() => {
    loadItems();
  }, []);

  const loadItems = async () => {
    try {
      const response = await itemsApi.getAll();
      setItems(response.items);
    } catch (error) {
      const errorMessage = handleApiError(error);
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (itemId: string) => {
    if (!confirm('Are you sure you want to delete this item?')) {
      return;
    }

    setDeleting(itemId);
    try {
      await itemsApi.delete(itemId);
      setItems(items.filter((item) => item.id !== itemId));
      toast.success('Item deleted successfully');
    } catch (error) {
      const errorMessage = handleApiError(error);
      toast.error(errorMessage);
    } finally {
      setDeleting(null);
    }
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50">
        <Navbar />

        <main className="container mx-auto px-6 py-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">My Closet</h1>
              <p className="text-gray-600 mt-1">
                {items.length} {items.length === 1 ? 'item' : 'items'} in your
                wardrobe
              </p>
            </div>
            <Link
              href="/upload"
              className="px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition flex items-center gap-2"
            >
              <svg
                className="w-5 h-5"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 4v16m8-8H4"
                />
              </svg>
              Add Item
            </Link>
          </div>

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              <p className="mt-4 text-gray-600">Loading your closet...</p>
            </div>
          )}

          {/* Empty State */}
          {!loading && items.length === 0 && (
            <div className="text-center py-20">
              <div className="w-24 h-24 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg
                  className="w-12 h-12 text-purple-600"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"
                  />
                </svg>
              </div>
              <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                Your closet is empty
              </h2>
              <p className="text-gray-600 mb-6">
                Start building your digital wardrobe by uploading your first
                item!
              </p>
              <Link
                href="/upload"
                className="inline-block px-6 py-3 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition"
              >
                Upload Your First Item
              </Link>
            </div>
          )}

          {/* Items Grid */}
          {!loading && items.length > 0 && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {items.map((item) => (
                <div
                  key={item.id}
                  className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition"
                >
                  {/* Image */}
                  <div className="aspect-square relative bg-gray-100">
                    <img
                      src={item.image_url}
                      alt={item.category || 'Clothing item'}
                      className="w-full h-full object-cover"
                    />
                  </div>

                  {/* Details */}
                  <div className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <div className="flex-1">
                        {item.category && (
                          <span className="inline-block px-2 py-1 bg-purple-100 text-purple-700 text-xs font-medium rounded mb-2">
                            {item.category}
                          </span>
                        )}
                        {item.brand && (
                          <h3 className="font-semibold text-gray-900">
                            {item.brand}
                          </h3>
                        )}
                        {item.color && (
                          <p className="text-sm text-gray-600">{item.color}</p>
                        )}
                      </div>
                    </div>

                    {item.notes && (
                      <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                        {item.notes}
                      </p>
                    )}

                    <div className="flex justify-between items-center pt-3 border-t">
                      <span className="text-xs text-gray-500">
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                      <button
                        onClick={() => handleDelete(item.id)}
                        disabled={deleting === item.id}
                        className="text-red-600 hover:text-red-700 text-sm font-medium disabled:opacity-50"
                      >
                        {deleting === item.id ? 'Deleting...' : 'Delete'}
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </ProtectedRoute>
  );
}
