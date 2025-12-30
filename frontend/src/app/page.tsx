// src/app/page.tsx
import React from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { FaMountain, FaUsers, FaAward, FaMapMarkedAlt, FaStar, FaArrowRight } from 'react-icons/fa';
import { getImageUrl } from '@/lib/utils';

// Type definition for Trek from Django API
interface Trek {
  id: number;
  slug: string;
  title: string;
  short_description: string;
  duration_days: number;
  price_usd: number;
  hero_image: string;
  difficulty?: string;
  rating?: number;
  reviews?: number;
}

// Fetch treks from Django backend
async function getTreks(): Promise<{ treks: Trek[]; error: string | null }> {
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  let treks: Trek[] = [];
  let error: string | null = null;

  try {
    const res = await fetch(`${API_URL}/api/treks/`, {
      cache: 'no-store' // Always fresh data
    });

    if (res.ok) {
      const data = await res.json();
      treks = data.results as Trek[] || [];
    } else {
      error = `Backend returned status ${res.status}`;
    }
  } catch (e) {
    if (e instanceof Error) {
      error = `Cannot connect to backend: ${e.message}. Is Django running on port 8000?`;
    } else {
      error = 'An unknown connection error occurred.';
    }
  }

  return { treks, error };
}

export default async function HomePage() {
  // Fetch treks from Django API
  const { treks, error } = await getTreks();

  return (
    <div>
      {/* Hero Section */}
      <section className="relative h-[600px] md:h-[700px] flex items-center justify-center bg-gradient-to-br from-gray-900 to-gray-800">
        <div className="absolute inset-0 bg-black opacity-40"></div>
        <div className="relative z-10 text-center text-white px-4 max-w-4xl">
          <h1 className="text-4xl md:text-6xl font-heading font-bold mb-6 leading-tight">
            Trekking in Nepal – Complete Guide<br />
            <span className="text-primary-400">Pokhara, Kathmandu, Himalayas</span>
          </h1>
          <p className="text-lg md:text-xl mb-8 text-gray-200 max-w-2xl mx-auto">
            Experience authentic Himalayan adventures with expert local guides. 
            From beginner-friendly trails to challenging expeditions.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link href="/treks" className="btn-primary text-lg px-8 py-3">
              Explore All Treks
            </Link>
            <Link href="/contact" className="btn-secondary text-lg px-8 py-3">
              Contact Us
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section-container">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {[
            { icon: FaMountain, title: '50+ Treks', desc: 'Wide range of trekking routes' },
            { icon: FaUsers, title: 'Expert Guides', desc: 'Licensed local professionals' },
            { icon: FaAward, title: '1000+ Happy Clients', desc: 'Trusted by trekkers worldwide' },
            { icon: FaMapMarkedAlt, title: 'Custom Itineraries', desc: 'Tailored to your needs' },
          ].map((feature, idx) => (
            <div key={idx} className="text-center p-6 rounded-xl bg-white shadow-md hover:shadow-xl transition-shadow">
              <feature.icon className="text-5xl text-primary-600 mx-auto mb-4" />
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Treks - DYNAMIC FROM DATABASE */}
      <section className="section-container bg-gray-100">
        <h2 className="text-3xl md:text-4xl font-heading font-bold text-center mb-12">
          Popular Treks in Nepal
        </h2>

        {/* Display Error */}
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8 max-w-4xl mx-auto">
            <strong>Error:</strong> {error}
            <div className="mt-2 text-sm">
              <p>✓ Check Django is running: <code>http://127.0.0.1:8000/api/treks/</code></p>
              <p>✓ Check <code>.env.local</code> has: <code>NEXT_PUBLIC_API_URL=http://localhost:8000</code></p>
            </div>
          </div>
        )}

        {/* Display Treks */}
        {treks.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {treks.map((trek) => (
              <Link 
                key={trek.id} 
                href={`/treks/${trek.slug}`} 
                className="card overflow-hidden group"
              >
                <div className="relative h-64">
                  <Image
                    src={getImageUrl(trek.hero_image)}
                    alt={trek.title}
                    fill
                    priority
                    style={{ objectFit: 'cover' }}
                    className="shadow-xl"
                  />
                  <div className="absolute top-4 right-4 bg-yellow-400 text-gray-900 px-3 py-1 rounded-full text-sm font-semibold">
                    ${trek.price_usd}
                  </div>
                </div>
                <div className="p-6">
                  <h3 className="text-xl font-semibold mb-2 group-hover:text-primary-600 transition-colors line-clamp-2">
                    {trek.title}
                  </h3>
                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {trek.short_description}
                  </p>
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 text-sm text-gray-600">
                      <span>📅 {trek.duration_days} days</span>
                      {trek.difficulty && <span>💪 {trek.difficulty}</span>}
                    </div>
                    {trek.rating && trek.reviews && (
                      <div className="flex items-center space-x-1">
                        <FaStar className="text-yellow-400" />
                        <span className="font-semibold">{trek.rating}</span>
                        <span className="text-gray-500 text-sm">({trek.reviews})</span>
                      </div>
                    )}
                    <FaArrowRight className="text-primary-600 group-hover:translate-x-2 transition-transform" />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* No Treks Message */}
        {treks.length === 0 && !error && (
          <div className="bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-3 rounded max-w-2xl mx-auto text-center">
            No treks found. Add treks via Django admin.
          </div>
        )}
      </section>

      {/* CTA Section */}
      <section className="section-container bg-primary-600 text-white text-center">
        <h2 className="text-3xl md:text-4xl font-heading font-bold mb-4">
          Ready to Start Your Adventure?
        </h2>
        <p className="text-lg md:text-xl mb-8 max-w-2xl mx-auto">
          Book your dream trek today and experience the majestic Himalayas with our expert team.
        </p>
        <Link href="/treks" className="bg-white text-primary-600 hover:bg-gray-100 font-semibold py-3 px-8 rounded-lg text-lg inline-flex items-center space-x-2 transition-colors">
          <span>Book Now</span>
          <FaArrowRight />
        </Link>
      </section>
    </div>
  );
}