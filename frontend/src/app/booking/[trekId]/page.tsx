// 'use client';
// // ============================================================
// // FILE: frontend/src/app/booking/[trekId]/page.tsx
// // PURPOSE: Booking form page. User fills in details and pays.
// //          KEY CHANGE: Check if user is logged in FIRST.
// //          If not → redirect to /login?redirect=/booking/ID
// //          so after login they come back here automatically.
// // ============================================================

// import { useState, useEffect, use } from 'react';
// import { useRouter } from 'next/navigation';
// import api from '@/lib/api';
// import { isAuthenticated } from '@/lib/auth';
// import { initiateESewaPayment, submitToESewa } from '@/lib/payment';
// import ChatBot from '@/components/common/ChatBot';

// // Trek type — what the API returns for a trek
// interface Trek {
//   id: number;
//   title: string;
//   slug:string;
//   price_usd:string;
//   discounted_price:string;
//   price_per_person: number;
//   duration_days: number;
//   difficulty: string;
// }

// export default function BookingPage({
//   params,
// }: {
//   params: Promise<{ trekId: string }>;
// }) {
//   // Unwrap the dynamic route parameter (Next.js 15 requires React.use())
//   const { trekId } = use(params);
//   const router = useRouter();

//   const [trek, setTrek] = useState<Trek | null>(null);
//   const [loading, setLoading] = useState(false);
//   const [pageLoading, setPageLoading] = useState(true);
//   const [error, setError] = useState('');

//   const [formData, setFormData] = useState({
//     full_name: '',
//     email: '',
//     phone: '',
//     country_code: '+977',
//     whatsapp_number: '',
//     country: '',
//     number_of_people: 1,
//     start_date: '',
//     special_requests: '',
//   });

//   // ──────────────────────────────────────────────────────────────
//   // AUTH CHECK — runs when page first loads
//   // If not logged in, redirect to /login with a "redirect" param
//   // so they come back here after logging in
//   // ──────────────────────────────────────────────────────────────
//   useEffect(() => {
//     if (!isAuthenticated()) {
//       // Build the redirect URL: /login?redirect=/booking/123
//       // encodeURIComponent encodes special chars like / in the URL
//       router.push(`/login?redirect=${encodeURIComponent(`/booking/${trekId}`)}`);
//       return;
//     }

//     // User IS logged in — fetch the trek details
//     const fetchTrek = async () => {
//       try {
//         const response = await api.get(`/treks/${trekId}/`);
//         setTrek(response.data);
//       } catch (err) {
//         console.error('Failed to load trek:', err);
//         setError('Failed to load trek details. Please try again.');
//       } finally {
//         setPageLoading(false);  // Stop showing loading spinner
//       }
//     };

//     fetchTrek();
//   }, [trekId, router]);
// const pricePerPerson=trek?parseFloat(trek.discounted_price || trek.price_usd):0;
//   // Calculate total price: trek price × number of people
//   const totalPrice =pricePerPerson * formData.number_of_people;

//   // ──────────────────────────────────────────────────────────────
//   // FORM SUBMIT — creates booking then initiates eSewa payment
//   // ──────────────────────────────────────────────────────────────
//   const handleSubmit = async (e: React.FormEvent) => {
//     e.preventDefault();
//     setLoading(true);
//     setError('');

//     try {
//       // STEP 1: Create the booking in Django
//       // POST /api/bookings/ with form data
//       const bookingData = {
//         trek: trek!.id,   // Which trek they're booking
//         ...formData,    // All the form fields
//       };

//       console.log('Creating booking:', bookingData);
//       const bookingResponse = await api.post('/bookings/', bookingData);
//       const bookingId = bookingResponse.data.booking_id;
//       console.log('Booking created, ID:', bookingId);

//       // STEP 2: Ask Django to generate eSewa payment parameters
//       // POST /api/payments/esewa/initiate/ with bookingId
//       const paymentData = await initiateESewaPayment(bookingId);
// // payload is now under esewa_payload key
// submitToESewa(paymentData.esewa_payload, paymentData.esewa_payload.esewa_url);

//     } catch (err: unknown) {
//       console.error('Booking failed:', err);

//       if (err && typeof err === 'object' && 'response' in err) {
//         const axiosErr = err as { response?: { status?: number; data?: Record<string, string[]> } };
//         const status = axiosErr.response?.status;
//         const data = axiosErr.response?.data;

//         if (status === 401) {
//           // Token expired — send back to login
//           router.push(`/login?redirect=${encodeURIComponent(`/booking/${trekId}`)}`);
//           return;
//         }

//         // Show field-specific errors from Django
//         if (data) {
//           const messages = Object.entries(data)
//             .map(([field, msgs]) => `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`)
//             .join(' | ');
//           setError(messages);
//         } else {
//           setError('Booking failed. Please check your details and try again.');
//         }
//       } else {
//         setError('Network error. Please check your connection.');
//       }
//       setLoading(false);
//     }
//   };

//   // ── LOADING STATE ──
//   if (pageLoading) {
//     return (
//       <div className="min-h-screen flex items-center justify-center">
//         <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full" />
//       </div>
//     );
//   }

//   return (
//     <div className="min-h-screen bg-gray-100 py-12">
//       <div className="max-w-2xl mx-auto px-4">
//         <div className="bg-white rounded-lg shadow-md p-8">

//           {/* Trek Summary at top of form */}
//           {trek && (
//             <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
//               <h2 className="font-bold text-blue-900 text-lg">{trek.title}</h2>
//               <div className="flex gap-4 text-sm text-blue-700 mt-1">
//                 <span>⏱ {trek.duration_days} days</span>
//                 <span>⚡ {trek.difficulty}</span>
//                 <span>💰 NPR {trek.price_per_person?.toLocaleString()} / person</span>
//               </div>
//             </div>
//           )}

//           <h1 className="text-3xl font-bold mb-6">Book Your Trek</h1>

//           {/* Error Message */}
//           {error && (
//             <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 mb-6">
//               ⚠️ {error}
//             </div>
//           )}

//           <form onSubmit={handleSubmit} className="space-y-4">

//             {/* Full Name */}
//             <div>
//               <label className="block text-sm font-medium mb-2">Full Name *</label>
//               <input
//                 type="text"
//                 required
//                 value={formData.full_name}
//                 onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
//                 className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//                 placeholder="Ram Shrestha"
//               />
//             </div>

//             {/* Email */}
//             <div>
//               <label className="block text-sm font-medium mb-2">Email *</label>
//               <input
//                 type="email"
//                 required
//                 value={formData.email}
//                 onChange={(e) => setFormData({ ...formData, email: e.target.value })}
//                 className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//               />
//             </div>

//             {/* Phone + WhatsApp */}
//             <div className="grid grid-cols-2 gap-4">
//               <div>
//                 <label className="block text-sm font-medium mb-2">Phone *</label>
//                 <input
//                   type="tel"
//                   required
//                   value={formData.phone}
//                   onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
//                   className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//                 />
//               </div>
//               <div>
//                 <label className="block text-sm font-medium mb-2">WhatsApp</label>
//                 <input
//                   type="tel"
//                   value={formData.whatsapp_number}
//                   onChange={(e) => setFormData({ ...formData, whatsapp_number: e.target.value })}
//                   className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//                 />
//               </div>
//             </div>

//             {/* Country */}
//             <div>
//               <label className="block text-sm font-medium mb-2">Country</label>
//               <input
//                 type="text"
//                 value={formData.country}
//                 onChange={(e) => setFormData({ ...formData, country: e.target.value })}
//                 className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//                 placeholder="Nepal"
//               />
//             </div>

//             {/* Number of People */}
//             <div>
//               <label className="block text-sm font-medium mb-2">Number of People *</label>
//               <input
//                 type="number"
//                 min="1"
//                 max="20"
//                 required
//                 value={formData.number_of_people}
//                 onChange={(e) =>
//                   setFormData({ ...formData, number_of_people: parseInt(e.target.value) || 1 })
//                 }
//                 className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//               />
//             </div>

//             {/* Start Date */}
//             <div>
//               <label className="block text-sm font-medium mb-2">Start Date *</label>
//               <input
//                 type="date"
//                 required
//                 // min: can't book in the past — today is the earliest
//                 min={new Date().toISOString().split('T')[0]}
//                 value={formData.start_date}
//                 onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
//                 className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//               />
//             </div>

//             {/* Special Requests */}
//             <div>
//               <label className="block text-sm font-medium mb-2">Special Requests</label>
//               <textarea
//                 rows={3}
//                 value={formData.special_requests}
//                 onChange={(e) => setFormData({ ...formData, special_requests: e.target.value })}
//                 className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
//                 placeholder="Vegetarian meals, altitude sickness medication, porter required..."
//               />
//             </div>

//             {/* Price Summary */}
//             {trek && (
//               <div className="bg-gray-50 rounded-lg p-4 border">
//                 <div className="flex justify-between text-sm text-gray-600">
//                   <span>NPR {trek.price_per_person?.toLocaleString()} × {formData.number_of_people} people</span>
//                   <span>NPR {totalPrice.toLocaleString()}</span>
//                 </div>
//                 <div className="flex justify-between font-bold text-gray-900 mt-2 text-lg">
//                   <span>Total</span>
//                   <span>NPR {totalPrice.toLocaleString()}</span>
//                 </div>
//               </div>
//             )}

//             {/* Pay with eSewa Button */}
//             <button
//               type="submit"
//               disabled={loading}
//               className="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
//             >
//               {loading ? (
//                 <span className="flex items-center gap-2">
//                   <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
//                   Processing...
//                 </span>
//               ) : (
//                 <>
//                   <span>💚</span>
//                   <span>Pay with eSewa — NPR {totalPrice.toLocaleString()}</span>
//                 </>
//               )}
//             </button>

//             {/* WhatsApp alternative */}
//             <button
//               type="button"
//               onClick={() => {
//                 const number = process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '9779846958184';
//                 const msg = encodeURIComponent(
//                   `Hi, I'd like to book ${trek?.title}.\nName: ${formData.full_name}\nEmail: ${formData.email}\nPhone: ${formData.phone}\nPeople: ${formData.number_of_people}\nDate: ${formData.start_date}`
//                 );
//                 window.open(`https://wa.me/${number}?text=${msg}`, '_blank');
//               }}
//               className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
//             >
//               <span>💬</span>
//               <span>Or contact via WhatsApp</span>
//             </button>

//           </form>
//         </div>
//       </div>

//       <ChatBot />
//     </div>
//   );
// }

'use client';
// ============================================================
// FILE: frontend/src/app/booking/[trekId]/page.tsx
// PURPOSE: Booking form page. User fills in details and pays.
//          KEY CHANGE: Check if user is logged in FIRST.
//          If not → redirect to /login?redirect=/booking/ID
//          so after login they come back here automatically.
// ============================================================

import { useState, useEffect, use } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { isAuthenticated } from '@/lib/auth';
import { submitToESewa } from '@/lib/payment';
import ChatBot from '@/components/common/ChatBot';

// Trek type — what the API returns for a trek
interface Trek {
  id: number;
  title: string;
  slug: string;
  price_usd: string;
  discounted_price: string;
  price_per_person: number;
  duration_days: number;
  difficulty: string;
}

export default function BookingPage({
  params,
}: {
  params: Promise<{ trekId: string }>;
}) {
  // Unwrap the dynamic route parameter (Next.js 15 requires React.use())
  const { trekId } = use(params);
  const router = useRouter();

  const [trek, setTrek] = useState<Trek | null>(null);
  const [loading, setLoading] = useState(false);
  const [pageLoading, setPageLoading] = useState(true);
  const [error, setError] = useState('');

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    phone: '',
    country_code: '+977',
    whatsapp_number: '',
    country: '',
    number_of_people: 1,
    start_date: '',
    special_requests: '',
  });

  // ──────────────────────────────────────────────────────────────
  // AUTH CHECK — runs when page first loads
  // If not logged in, redirect to /login with a "redirect" param
  // so they come back here after logging in
  // ──────────────────────────────────────────────────────────────
  useEffect(() => {
    if (!isAuthenticated()) {
      router.push(`/login?redirect=${encodeURIComponent(`/booking/${trekId}`)}`);
      return;
    }

    // User IS logged in — fetch the trek details
    const fetchTrek = async () => {
      try {
        const response = await api.get(`/treks/${trekId}/`);
        setTrek(response.data);
      } catch (err) {
        console.error('Failed to load trek:', err);
        setError('Failed to load trek details. Please try again.');
      } finally {
        setPageLoading(false);
      }
    };

    fetchTrek();
  }, [trekId, router]);

  // ── PRICE CALCULATION ───────────────────────────────────────
  // Use discounted_price if available, otherwise fall back to price_usd.
  // price_per_person is the NPR display value shown in the summary header.
  const pricePerPerson = trek
    ? parseFloat(trek.discounted_price || trek.price_usd)
    : 0;
  const totalPrice = pricePerPerson * formData.number_of_people;

  // ──────────────────────────────────────────────────────────────
  // FORM SUBMIT — creates booking then initiates eSewa payment
  //
  // Flow (matches tutorial exactly):
  //   1. POST /api/bookings/          → creates booking, returns booking_id
  //   2. POST /payments/esewa/initiate/ → Django builds signed payload
  //   3. submitToESewa()              → browser navigates to eSewa
  //   4. eSewa redirects to success_url with ?data=<base64>
  //   5. Django verifies & marks booking paid
  // ──────────────────────────────────────────────────────────────
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // STEP 1: Create the booking in Django
      const bookingData = {
        trek: trek!.id,
        ...formData,
      };

      console.log('Creating booking:', bookingData);
      const bookingResponse = await api.post('/bookings/', { trek: trek!.id, ...formData });
const { esewa_payload } = bookingResponse.data;
submitToESewa(esewa_payload, esewa_payload.esewa_url);

      // NOTE: code after this line won't run — browser navigates away

    } catch (err: unknown) {
      console.error('Booking failed:', err);

      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as {
          response?: { status?: number; data?: Record<string, string[]> };
        };
        const status = axiosErr.response?.status;
        const data = axiosErr.response?.data;

        if (status === 401) {
          // Token expired — send back to login
          router.push(
            `/login?redirect=${encodeURIComponent(`/booking/${trekId}`)}`
          );
          return;
        }

        // Show field-specific errors from Django
        if (data) {
          const messages = Object.entries(data)
            .map(
              ([field, msgs]) =>
                `${field}: ${Array.isArray(msgs) ? msgs.join(', ') : msgs}`
            )
            .join(' | ');
          setError(messages);
        } else {
          setError('Booking failed. Please check your details and try again.');
        }
      } else {
        setError('Network error. Please check your connection.');
      }
      setLoading(false);
    }
  };

  // ── LOADING STATE ──
  if (pageLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin h-12 w-12 border-4 border-blue-600 border-t-transparent rounded-full" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 py-12">
      <div className="max-w-2xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-md p-8">

          {/* Trek Summary at top of form */}
          {trek && (
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h2 className="font-bold text-blue-900 text-lg">{trek.title}</h2>
              <div className="flex gap-4 text-sm text-blue-700 mt-1">
                <span>⏱ {trek.duration_days} days</span>
                <span>⚡ {trek.difficulty}</span>
                {/* price_per_person is the NPR value your backend returns for display */}
                <span>💰 NPR {trek.price_per_person?.toLocaleString()} / person</span>
              </div>
            </div>
          )}

          <h1 className="text-3xl font-bold mb-6">Book Your Trek</h1>

          {/* Error Message */}
          {error && (
            <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 mb-6">
              ⚠️ {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">

            {/* Full Name */}
            <div>
              <label className="block text-sm font-medium mb-2">Full Name *</label>
              <input
                type="text"
                required
                value={formData.full_name}
                onChange={(e) =>
                  setFormData({ ...formData, full_name: e.target.value })
                }
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Ram Shrestha"
              />
            </div>

            {/* Email */}
            <div>
              <label className="block text-sm font-medium mb-2">Email *</label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) =>
                  setFormData({ ...formData, email: e.target.value })
                }
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Phone + WhatsApp */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-2">Phone *</label>
                <input
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={(e) =>
                    setFormData({ ...formData, phone: e.target.value })
                  }
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-2">WhatsApp</label>
                <input
                  type="tel"
                  value={formData.whatsapp_number}
                  onChange={(e) =>
                    setFormData({ ...formData, whatsapp_number: e.target.value })
                  }
                  className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Country */}
            <div>
              <label className="block text-sm font-medium mb-2">Country</label>
              <input
                type="text"
                value={formData.country}
                onChange={(e) =>
                  setFormData({ ...formData, country: e.target.value })
                }
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Nepal"
              />
            </div>

            {/* Number of People */}
            <div>
              <label className="block text-sm font-medium mb-2">
                Number of People *
              </label>
              <input
                type="number"
                min="1"
                max="20"
                required
                value={formData.number_of_people}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    number_of_people: parseInt(e.target.value) || 1,
                  })
                }
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Start Date */}
            <div>
              <label className="block text-sm font-medium mb-2">Start Date *</label>
              <input
                type="date"
                required
                min={new Date().toISOString().split('T')[0]}
                value={formData.start_date}
                onChange={(e) =>
                  setFormData({ ...formData, start_date: e.target.value })
                }
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Special Requests */}
            <div>
              <label className="block text-sm font-medium mb-2">
                Special Requests
              </label>
              <textarea
                rows={3}
                value={formData.special_requests}
                onChange={(e) =>
                  setFormData({ ...formData, special_requests: e.target.value })
                }
                className="w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500"
                placeholder="Vegetarian meals, altitude sickness medication, porter required..."
              />
            </div>

            {/* Price Summary */}
            {trek && (
              <div className="bg-gray-50 rounded-lg p-4 border">
                <div className="flex justify-between text-sm text-gray-600">
                  {/*
                    Display uses price_per_person (your backend's NPR field).
                    Calculation uses pricePerPerson (discounted_price || price_usd)
                    which is what Django uses to charge eSewa.
                    If both are the same field on your backend, that's fine too.
                  */}
                  <span>
                    NPR {trek.price_per_person?.toLocaleString()} ×{' '}
                    {formData.number_of_people} people
                  </span>
                  <span>NPR {totalPrice.toLocaleString()}</span>
                </div>
                <div className="flex justify-between font-bold text-gray-900 mt-2 text-lg">
                  <span>Total</span>
                  <span>NPR {totalPrice.toLocaleString()}</span>
                </div>
              </div>
            )}

            {/* Pay with eSewa Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-green-600 hover:bg-green-700 disabled:bg-green-400 text-white font-bold py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                  Processing...
                </span>
              ) : (
                <>
                  <span>💚</span>
                  <span>Pay with eSewa — NPR {totalPrice.toLocaleString()}</span>
                </>
              )}
            </button>

            {/* WhatsApp alternative */}
            <button
              type="button"
              onClick={() => {
                const number =
                  process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '9779846958184';
                const msg = encodeURIComponent(
                  `Hi, I'd like to book ${trek?.title}.\nName: ${formData.full_name}\nEmail: ${formData.email}\nPhone: ${formData.phone}\nPeople: ${formData.number_of_people}\nDate: ${formData.start_date}`
                );
                window.open(`https://wa.me/${number}?text=${msg}`, '_blank');
              }}
              className="w-full bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium py-3 px-6 rounded-lg flex items-center justify-center gap-2 transition-colors"
            >
              <span>💬</span>
              <span>Or contact via WhatsApp</span>
            </button>

          </form>
        </div>
      </div>

      <ChatBot />
    </div>
  );
}