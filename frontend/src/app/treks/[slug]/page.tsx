// File: src/app/treks/[slug]/page.tsx 

import Link from 'next/link'; 
import Image from 'next/image'; 

// CORRECT IMPORT PATH (Assuming '@/types' maps to src/types/index.ts)
import { 
    TrekDetail, 
    Itinerary, 
    IncludedItem, 
    ExcludedItem, 
    TrekImage,
    MapCoordinate
} from '@/types'; 
// Import your utilities and constants (assuming these paths are correct)
import { getImageUrl, formatPrice, getWhatsAppLink } from '@/lib/utils';
import { DIFFICULTY_LABELS, DIFFICULTY_COLORS } from '@/lib/constants';


// This is an Async Server Component
export default async function TrekDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>; // ← Change the type to Promise
}) {
  
  // *** CORRECT FIX ***
  // Await the entire params object, then destructure slug
  const { slug } = await params;
  
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  // Explicitly type the variables
  let trek: TrekDetail | null = null;
  let error: string | null = null;
  
  // *** Initial check for missing slug (fixes the empty slug in the API call) ***
  if (!slug) {
     error = 'The trek identifier is missing from the URL.';
  }

  if (slug) {
      // Console logs for debugging the URL
      console.log(`[TrekDetailPage] Attempting to fetch slug: ${slug}`);
      console.log(`[TrekDetailPage] Full API URL: ${API_URL}/api/treks/${slug}/`);
      
      try {
          // This calls the correct detail endpoint: /api/treks/{slug}/
          const res = await fetch(`${API_URL}/api/treks/${slug}/`, { 
              cache: 'no-store' 
          });
          
          if (res.ok) {
              const data = await res.json();
              trek = data as TrekDetail;
          } else {
              // Log the status if fetch fails, which is where your 404 came from
              console.error(`[TrekDetailPage] API returned status: ${res.status} for slug: ${slug}`);
              error = `Trek not found (${res.status})`;
          }
      } catch (e: unknown) {
          console.error("Fetch Error:", e);
          error = 'Cannot connect to backend or network error.';
      }
  }

  if (error || !trek) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
        <div className="max-w-md w-full bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-2xl font-bold text-red-600 mb-4">Trek Not Found</h1>
          <p className="text-gray-600 mb-4">{error}</p>
          <p className="text-sm text-gray-500 mb-4">Looking for: **{slug || "N/A"}**</p>
          <Link
            href="/treks" 
            className="inline-block bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            ← Back to All Treks
          </Link>
        </div>
      </div>
    );
  }

  const getDifficultyClass = (difficultySlug: string): string => {
    return DIFFICULTY_COLORS[difficultySlug] || 'bg-gray-100 text-gray-800'; 
  };
    
  const price = formatPrice(trek.price_usd);
  const discountedPrice = trek.discounted_price ? formatPrice(trek.discounted_price) : null;
  const finalPriceDisplay = discountedPrice || price;
  const whatsAppMessage = `Hi, I'm interested in the "${trek.title}" trek and would like to know more.`;


  return (
    <div className="min-h-screen bg-gray-100">
      
      {/* Hero Image Section */}
      <div className="relative h-96 w-full">
        <Image
          src={getImageUrl(trek.hero_image)}
          alt={trek.title}
          fill
          priority
          style={{ objectFit: 'cover' }}
          className="shadow-xl"
        />
        <div className="absolute inset-0 bg-black bg-opacity-40 flex items-end">
          <div className="max-w-4xl mx-auto px-4 pb-8 w-full">
            <h1 className="text-4xl md:text-5xl font-extrabold text-white mb-2 leading-tight drop-shadow-lg">{trek.title}</h1>
            <p className="text-xl text-gray-200 drop-shadow-md">{trek.location}</p>
          </div>
        </div>
      </div>


      {/* Content Layout */}
      <div className="max-w-4xl mx-auto px-4 py-12">
        
        {/* Details Box */}
        <div className="bg-white rounded-xl shadow-2xl p-6 mb-8 transform -translate-y-16">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-3xl mb-2">📅</div>
              <div className="text-sm text-gray-600">Duration</div>
              <div className="font-bold text-lg">{trek.duration_days} days / {trek.duration_nights} nights</div>
            </div>
            <div>
              <div className="text-3xl mb-2">💪</div>
              <div className="text-sm text-gray-600">Difficulty</div>
              <div className={`font-semibold text-sm py-1 px-3 rounded-full inline-block mt-1 ${getDifficultyClass(trek.difficulty)}`}>
                  {DIFFICULTY_LABELS[trek.difficulty] || trek.difficulty}
              </div>
            </div>
            <div>
              <div className="text-3xl mb-2">⛰️</div>
              <div className="text-sm text-gray-600">Max Altitude</div>
              <div className="font-bold text-lg">{trek.max_altitude}m ({trek.max_altitude_feet}ft)</div>
            </div>
            <div>
              <div className="text-3xl mb-2">💰</div>
              <div className="text-sm text-gray-600">Price From</div>
              <div className={`font-extrabold text-2xl ${discountedPrice ? 'text-red-600' : 'text-blue-600'}`}>
                {finalPriceDisplay}
              </div>
              {trek.discounted_price && (
                  <div className="text-sm text-gray-500 line-through">
                      {price}
                  </div>
              )}
            </div>
          </div>
        </div>

        {/* Description */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <h2 className="text-2xl font-bold mb-4 border-b pb-2">Trek Overview</h2>
          <p className="text-gray-700 mb-4 leading-relaxed">
            {trek.short_description}
          </p>
          <p className="text-gray-700 leading-relaxed">
            {trek.long_description}
          </p>
          
          {/* MAP COORDINATES Section */}
          {trek.map_coordinates && trek.map_coordinates.length > 0 && (
            <div className='mt-6'>
                <h3 className="text-lg font-bold mb-2">Key Map Coordinates:</h3>
                <ul className="list-disc list-inside text-gray-600">
                    {trek.map_coordinates.map((coord: MapCoordinate) => (
                        <li key={coord.id} className="text-sm">
                            {coord.name}: Lat {coord.latitude}, Lon {coord.longitude}
                        </li>
                    ))}
                </ul>
            </div>
          )}
          
        </div>

        {/* DETAILED ITINERARY SECTION */}
        <section className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-2xl font-bold mb-4 border-b pb-2">Detailed Itinerary</h2>
            <div className="space-y-4">
                {trek.itinerary.map((day: Itinerary) => (
                    <details key={day.id} className="border-b border-gray-200 rounded-lg overflow-hidden">
                        <summary className="flex justify-between items-center cursor-pointer p-4 bg-gray-50 hover:bg-gray-100 font-semibold text-gray-800">
                            <span>Day {day.day_number}: {day.title}</span>
                            <span className="text-sm text-blue-600 bg-blue-50 px-3 py-1 rounded-full">{day.altitude}</span>
                        </summary>
                        
                        <div className="p-4 text-gray-700 border-t">
                            <p className="mb-3">{day.description}</p>
                            <ul className="list-disc list-inside space-y-1 text-sm text-gray-600">
                                <li>**Trekking Hours:** {day.trekking_hours}</li>
                                <li>**Accommodation:** {day.accommodation}</li>
                                <li>**Meals:** {day.meals_included}</li>
                            </ul>
                        </div>
                    </details>
                ))}
            </div>
        </section>

        {/* INCLUSIONS & EXCLUSIONS SECTION */}
        <div className="grid md:grid-cols-2 gap-8 mb-8">
            {/* INCLUDED ITEMS */}
            <section className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-bold mb-4 border-b pb-2 text-green-700">✅ Whats Included</h2>
                <ul className="space-y-3">
                    {trek.included_items.map((itemObj: IncludedItem) => (
                        <li key={itemObj.id} className="flex items-start text-gray-700">
                            <span className="text-green-500 mr-3 mt-1">✔</span>
                            {itemObj.item}
                        </li>
                    ))}
                </ul>
            </section>

            {/* EXCLUDED ITEMS */}
            <section className="bg-white rounded-lg shadow-md p-6">
                <h2 className="text-2xl font-bold mb-4 border-b pb-2 text-red-700">❌ Whats Excluded</h2>
                <ul className="space-y-3">
                    {trek.excluded_items.map((itemObj: ExcludedItem) => (
                        <li key={itemObj.id} className="flex items-start text-gray-700">
                            <span className="text-red-500 mr-3 mt-1">✘</span>
                            {itemObj.item}
                        </li>
                    ))}
                </ul>
            </section>
        </div>

        {/* GALLERY SECTION */}
        <section className="bg-white rounded-lg shadow-md p-6 mb-8">
            <h2 className="text-2xl font-bold mb-4 border-b pb-2">Photo Gallery</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {/* Accessing gallery_images correctly as per your index.ts */}
                {trek.gallery.map((imageObj: TrekImage) => (
                    <figure key={imageObj.id} className="overflow-hidden rounded-lg shadow-lg">
                        <div className="relative h-40">
                            <Image 
                                src={getImageUrl(imageObj.image)} 
                                alt={imageObj.caption || trek.title} 
                                fill
                                sizes="(max-width: 768px) 50vw, 33vw"
                                style={{ objectFit: 'cover' }}
                            /> 
                        </div>
                        <figcaption className="p-3 text-xs text-center text-gray-600 bg-gray-50">{imageObj.caption || trek.title}</figcaption>
                    </figure>
                ))}
            </div>
        </section>


        {/* Book Now */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-2xl font-bold mb-4">Ready to Book?</h2>
          <div className="flex flex-col sm:flex-row gap-4">
            <a
              href={getWhatsAppLink(whatsAppMessage)}
              target="_blank"
              rel="noopener noreferrer"
              className="flex-1 bg-green-600 hover:bg-green-700 text-white text-center font-semibold py-3 px-6 rounded-lg transition duration-200"
            >
              💬 WhatsApp Us
            </a>
            <Link
              href={`/booking/${trek.slug}`}
              className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg text-center transition duration-200"
            >
              📝 Book Now
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}