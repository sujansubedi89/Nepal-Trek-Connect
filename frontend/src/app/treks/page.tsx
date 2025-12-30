import Image from 'next/image';
import { getImageUrl } from '@/lib/utils';
import { TrekImage } from '@/types';
import React from 'react';

// 1. Define the Interface based on your Django API output
export interface Trek {
  id: number;
  slug: string;
  title: string;
  short_description: string;
  duration_days: number;
  price_usd: number;
  hero_image:string;
  // Add other fields here (e.g., image_url, rating)
}

// 2. Type-Safe Data Fetching Utility
async function getTreks(): Promise<{ treks: Trek[]; error: string | null }> {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  let treks: Trek[] = [];
  let error: string | null = null;

  try {
    const res = await fetch(`${API_URL}/api/treks/`, { 
      // Ensure data is always fresh during development
      cache: 'no-store' 
    });
    
    if (res.ok) {
      const data = await res.json();
      // Use type assertion based on expected DRF structure { results: Trek[] }
      treks = data.results as Trek[] || []; 
    } else {
      error = `Backend returned status ${res.status}. Check your Django viewset.`;
    }
  } catch (e) { 
    // Type-safe error handling for network issues
    if (e instanceof Error) {
      error = `Cannot connect to backend: ${e.message}. Is Django running on port 8000?`;
    } else {
      error = 'An unknown connection error occurred.';
    }
  }

  return { treks, error };
}

// 3. Main Server Component
export default async function TreksPage() {
  const { treks, error } = await getTreks();

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-7xl mx-auto px-4">
        <h1 className="text-4xl font-bold mb-8">All Trekking Packages</h1>

        {/* Display Connection/Fetch Error */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            <strong>Error:</strong> {error}
            <div className="mt-2 text-sm">
              <p>✓ Check Django is running: <code>http://127.0.0.1:8000/api/treks/</code></p>
              <p>✓ Check <code>.env.local</code> has: <code>NEXT_PUBLIC_API_URL=http://localhost:8000</code></p>
              <p>✓ Check Django CORS settings.</p>
            </div>
          </div>
        )}

        {/* Display No Data Message */}
        {treks.length === 0 && !error && (
          <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded">
            No treks found. Add treks via Django admin.
          </div>
        )}

        {/* Display Treks */}
        {treks.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* The 'trek' variable is now implicitly typed as 'Trek' */}
            {treks.map((trek) => (
              <a 
                key={trek.id}
                href={`/treks/${trek.slug}`}
                className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition"
              >
               <div className="relative h-96 w-full">
<Image
src={getImageUrl(trek.hero_image)}
alt={trek.title}
fill
priority
style={{ objectFit: 'cover' }}
className="shadow-xl"
/>
     </div>           
                <div className="p-6">
                  <h2 className="text-xl font-semibold mb-2 line-clamp-2">
                    {trek.title}
                  </h2>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {trek.short_description}
                  </p>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-gray-500">
                      📅 {trek.duration_days} days
                    </span>
                    <span className="text-xl font-bold text-blue-600">
                      ${trek.price_usd}
                    </span>
                  </div>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}