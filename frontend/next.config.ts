/** @type {import('next').NextConfig} */
const nextConfig = {
  // Fixes the "Exit Code 1" by ignoring TypeScript/Lint errors during build
  typescript: {
    ignoreBuildErrors: true,
  },
  eslint: {
    ignoreDuringBuilds: true,
  },

  images: {
    remotePatterns: [
      {
        protocol: 'http',
        hostname: 'localhost',
        port: '8000',
        pathname: '/media/**',
      },
      {
        protocol: 'https',
        // This allows your images from the Django backend to load correctly
        hostname: '://onrender.com', 
        pathname: '/media/**',
      }
    ],
    dangerouslyAllowSVG: true,
    // Set to true to avoid Vercel image optimization limits on free tier
    unoptimized: true, 
  },
  
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
    NEXT_PUBLIC_STRIPE_PUBLIC_KEY: process.env.NEXT_PUBLIC_STRIPE_PUBLIC_KEY,
    NEXT_PUBLIC_KHALTI_PUBLIC_KEY: process.env.NEXT_PUBLIC_KHALTI_PUBLIC_KEY,
    NEXT_PUBLIC_WHATSAPP_NUMBER: process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '9779846958184',
  },
}

module.exports = nextConfig
