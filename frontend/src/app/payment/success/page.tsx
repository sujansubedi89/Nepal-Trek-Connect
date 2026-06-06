'use client';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';

export default function PaymentSuccessPage() {
  const searchParams = useSearchParams();
  const bookingId = searchParams.get('booking_id');

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-lg p-8 max-w-md w-full text-center">
        <div className="text-6xl mb-4">✅</div>
        <h1 className="text-2xl font-bold text-green-600 mb-2">Payment Successful!</h1>
        {bookingId && (
          <p className="text-gray-600 mb-4">Booking ID: <strong>{bookingId}</strong></p>
        )}
        <p className="text-gray-500 mb-6">
          Your trek has been booked! Check your email for confirmation.
        </p>
        <Link href="/treks" className="inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700">
          Browse More Treks
        </Link>
      </div>
    </div>
  );
}