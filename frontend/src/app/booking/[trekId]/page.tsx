'use client';

import { useState, useEffect,use } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { initiateESewaPayment, submitToESewa } from '@/lib/payment';

export default function BookingPage({
  params,
}: {
  params: Promise<{ trekId: string }>;
}) {
  // FIX 1: Unwrap params using React.use() for Next.js 15
  const { trekId } = use(params);
  const [trek, setTrek] = useState(null);

// When page loads, fetch the trek
useEffect(() => {
  const fetchTrek = async () => {
    const response = await api.get(`/treks/${trekId}/`);
    setTrek(response.data);
  };
  fetchTrek();
}, [trekId]);

  const router = useRouter();
  const [loading, setLoading] = useState(false);
  const [authError, setAuthError] = useState(false);
  
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    country_code: '',
    whatsapp_number: '',
    country: '',
    number_of_people: 1,
    start_date: '',
    special_requests: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAuthError(false);

    try {
      console.log('Creating booking for trek:', trekId);
      
      // See exactly what you're sending
      const bookingData = {
        trek: trekId,
        ...formData,
      };
      console.log('📤 Sending booking data:', bookingData);
      console.log('📤 FormData contents:', formData);

      // Step 1: Create booking
      const bookingResponse = await api.post('/bookings/', bookingData);

      console.log('✅ Booking created:', bookingResponse.data);
      const bookingId = bookingResponse.data.booking_id;

      // Step 2: Initiate eSewa payment
      const paymentData = await initiateESewaPayment(bookingId);
      console.log('Payment initiated:', paymentData);

      // Step 3: Redirect to eSewa
      submitToESewa(paymentData.esewa_params, paymentData.esewa_url);
      
    } catch (error: unknown) {
      console.error('❌ Booking error:', error);
      
      // Handle 401 Unauthorized
      if (error && typeof error === 'object' && 'response' in error) {
        const axiosError = error as { response?: { status?: number; data?: { error?: string } } };
        
        console.error('❌ Error response data:', axiosError.response?.data);
        console.error('❌ Error status:', axiosError.response?.status);
        
        if (axiosError.response?.status === 401) {
          alert('Your session has expired. Please login again.');
          setAuthError(true);
          router.push('/login');
        } else {
          alert(axiosError.response?.data?.error || 'Booking failed. Please try again.');
        }
      } else {
        alert('Booking failed. Please try again.');
      }
      
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-2xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-8">
          <h1 className="text-3xl font-bold mb-6">Book Your Trek</h1>

          {/* Show auth error */}
          {authError && (
            <div className="bg-red-100 border-2 border-red-400 rounded-lg p-4 mb-6">
              <p className="text-red-800 font-semibold">
                ⚠️ You must be logged in to make a booking!
              </p>
              <button
                onClick={() => router.push('/login')}
                className="mt-2 bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700"
              >
                Go to Login
              </button>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium mb-2">Full Name *</label>
              <input
                type="text"
                required
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Email *</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Phone *</label>
                <input
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium mb-2">WhatsApp</label>
                <input
                  type="tel"
                  value={formData.whatsapp_number}
                  onChange={(e) => setFormData({ ...formData, whatsapp_number: e.target.value })}
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Number of People *</label>
              <input
                type="number"
                min="1"
                required
                value={formData.number_of_people}
                onChange={(e) => setFormData({ ...formData, number_of_people: parseInt(e.target.value) })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Start Date *</label>
              <input
                type="date"
                required
                value={formData.start_date}
                onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Special Requests</label>
              <textarea
                rows={3}
                value={formData.special_requests}
                onChange={(e) => setFormData({ ...formData, special_requests: e.target.value })}
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <>Processing...</>
              ) : (
                <>
                  <span>Pay with eSewa</span>
                  <img src="https://esewa.com.np/common/images/esewa-logo.png" alt="eSewa" className="h-6" />
                </>
                
              )}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}