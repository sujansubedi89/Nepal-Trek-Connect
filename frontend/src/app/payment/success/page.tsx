'use client';
import { useSearchParams } from 'next/navigation';
import Link from 'next/link';

export default function PaymentSuccessPage() {
  const params = useSearchParams();
  // eSewa sends ?data=<base64> — Django already verified it
  // You can optionally decode and show booking_id here

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-md p-10 max-w-md text-center">
        <div className="text-6xl mb-4">✅</div>
        <h1 className="text-2xl font-bold text-green-700 mb-2">Payment Successful!</h1>
        <p className="text-gray-600 mb-6">
          Your trek has been booked. A confirmation email has been sent to you.
        </p>
        <Link
          href="/treks"
          className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg"
        >
          Browse More Treks
        </Link>
      </div>
    </div>
  );
}