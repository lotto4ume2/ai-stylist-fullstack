'use client';

import Link from 'next/link';
import { useAuth } from '@/lib/auth-context';

export default function Navbar() {
  const { user, logout } = useAuth();

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="container mx-auto px-6 py-4">
        <div className="flex justify-between items-center">
          <Link href="/closet">
            <h1 className="text-2xl font-bold text-purple-600">AI-Stylist</h1>
          </Link>

          <div className="flex items-center gap-6">
            <Link
              href="/closet"
              className="text-gray-700 hover:text-purple-600 transition"
            >
              My Closet
            </Link>
            <Link
              href="/upload"
              className="text-gray-700 hover:text-purple-600 transition"
            >
              Upload
            </Link>
            
            <div className="flex items-center gap-4 border-l pl-6">
              <span className="text-sm text-gray-600">{user?.email}</span>
              <button
                onClick={logout}
                className="px-4 py-2 text-sm bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}
