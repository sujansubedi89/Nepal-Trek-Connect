// File: src/types/index.ts (Cleaned Version)

export interface Trek {
  id: number;
  title: string;
  slug: string;
  short_description: string;
  long_description?: string;
  location: string;
  duration_days: number;
  duration_nights: number;
  difficulty: string;
  max_altitude: number;
  max_altitude_feet: number;
  best_season: string;
  price_usd: string;
  discount_percentage: number;
  discounted_price: string;
  hero_image: string;
  is_featured: boolean;
  is_popular: boolean;
  average_rating: string;
  total_reviews: number;
  views_count: number;
  
}

export interface TrekDetail extends Trek {
  latitude: string;
  longitude: string;
  image_keywords: string;
  meta_title: string;
  meta_description: string;
  // This field is correctly named 'gallery_images'
  gallery: TrekImage[];
  itinerary: Itinerary[];
  included_items: IncludedItem[];
  excluded_items: ExcludedItem[];
  map_coordinates: MapCoordinate[];
}

export interface TrekImage {
  id: number;
  image: string;
  caption: string;
  order: number;
}

export interface Itinerary {
  id: number;
  day_number: number;
  title: string;
  description: string;
  altitude: string;
  trekking_hours: string;
  accommodation: string;
  meals_included: string;
}

export interface IncludedItem {
  id: number;
  item: string;
}

export interface ExcludedItem {
  id: number;
  item: string;
}

export interface MapCoordinate {
  id: number;
  name: string;
  latitude: string;
  longitude: string;
}

export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone: string;
  country_code: string;
  whatsapp_number: string;
  country: string;
}

export interface Booking {
  id: number;
  booking_id: string;
  trek: number;
  trek_details: Trek;
  full_name: string;
  email: string;
  phone: string;
  country_code: string;
  whatsapp_number: string;
  country: string;
  number_of_people: number;
  start_date: string;
  special_requests: string;
  price_per_person: string;
  total_price: string;
  status: string;
  created_at: string;
}

export interface Review {
  id: number;
  user_name: string;
  rating: number;
  title: string;
  comment: string;
  image1?: string;
  image2?: string;
  image3?: string;
  is_verified: boolean;
  created_at: string;
}

export interface ApiResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}