import { WHATSAPP_NUMBER } from '@/lib/constants';
export const formatPrice = (price: string | number): string => {
  const numPrice = typeof price === 'string' ? parseFloat(price) : price;
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(numPrice);
};

export const formatDate = (date: string): string => {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
};

export const getImageUrl = (imagePath: string | null | undefined): string => {
  // If no image, return placeholder
  if (!imagePath) {
    return '/images/trek-placeholder.jpg';
  }
  
  // If already full URL, return as-is
  if (imagePath.startsWith('http')) {
    return imagePath;
  }
  
  // Build full URL to Django backend
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  // Remove leading slash if present
  const cleanPath = imagePath.startsWith('/') ? imagePath : `/${imagePath}`;
  
  return `${API_URL}${cleanPath}`;
};
export const truncateText = (text: string, maxLength: number): string => {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength).trim() + '...';
};

export const getWhatsAppLink = (message: string = ''): string => {
  const phone = WHATSAPP_NUMBER.replace(/\+/g, '');
  const encodedMessage = encodeURIComponent(message || 'Hi, I would like to know more about your trekking packages.');
  return `https://wa.me/${phone}?text=${encodedMessage}`;
};

export const scrollToTop = (): void => {
  window.scrollTo({ top: 0, behavior: 'smooth' });
};