'use client';
import Link from 'next/link';

export default function PaymentFailedPage() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-md p-10 max-w-md text-center">
        <div className="text-6xl mb-4">❌</div>
        <h1 className="text-2xl font-bold text-red-700 mb-2">Payment Failed</h1>
        <p className="text-gray-600 mb-6">
          Something went wrong. Your booking has not been confirmed. Please try again.
        </p>
        <Link
          href="/treks"
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg"
        >
          Back to Treks
        </Link>
      </div>
    </div>
  );
}