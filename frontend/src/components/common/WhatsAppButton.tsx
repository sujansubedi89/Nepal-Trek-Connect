'use client';

import React, { useState } from 'react';
import { FaWhatsapp, FaTimes } from 'react-icons/fa';
import { getWhatsAppLink } from '@/lib/utils';

export default function WhatsAppButton() {
  const [isVisible, setIsVisible] = useState(true);

  if (!isVisible) return null;

  return (
    <div className="fixed bottom-24 right-6 z-40 flex flex-col items-end space-y-2">
      {/* Close Button */}
      <button
        onClick={() => setIsVisible(false)}
        className="bg-gray-100 hover:bg-gray-200 text-gray-600 rounded-full p-1 shadow-lg transition-all duration-200"
        aria-label="Close WhatsApp button"
      >
        <FaTimes size={12} />
      </button>

      {/* WhatsApp Button */}
      <a
        href={getWhatsAppLink('Hi! I want to inquire about trekking packages in Nepal.')}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-green-500 hover:bg-green-600 text-white rounded-full p-4 shadow-2xl hover:scale-110 transition-all duration-300 flex items-center justify-center group"
        aria-label="Contact us on WhatsApp"
      >
        <FaWhatsapp size={32} className="animate-pulse group-hover:animate-none" />
      </a>

      {/* Tooltip */}
      <div className="bg-white text-gray-800 px-4 py-2 rounded-lg shadow-lg text-sm font-medium whitespace-nowrap">
        Chat with us on WhatsApp!
      </div>
    </div>
  );
}