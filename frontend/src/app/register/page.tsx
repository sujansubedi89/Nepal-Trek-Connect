'use client';
// ============================================================
// FILE: frontend/src/app/login/page.tsx
// PURPOSE: The login page. Users enter email + password.
//          On success → redirect to wherever they came from
//          (e.g. if they tried to book and were redirected here,
//           they go back to the booking page after login).
// ============================================================

import { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import { loginUser } from '@/lib/auth';

export default function LoginPage() {
  const router = useRouter();
  // useSearchParams lets us read URL query params like ?redirect=/booking/123
  const searchParams = useSearchParams();

  // Form state — tracks what the user typed
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  // UI state — shows loading spinner, error messages
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // ──────────────────────────────────────────────────────────────
  // HANDLE FORM SUBMIT
  // Called when user clicks "Login" button
  // ──────────────────────────────────────────────────────────────
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();   // Stop browser from refreshing the page
    setLoading(true);
    setError('');         // Clear any old error messages

    try {
      // Call our loginUser function from auth.ts
      // This talks to Django's /api/auth/login/ endpoint
      await loginUser({
        email: formData.email,
        password: formData.password,
      });

      // Login worked! Now figure out where to redirect.
      // If user came from /booking/123, the URL looks like:
      //   /login?redirect=/booking/123
      // We read that 'redirect' value and send them back there.
      const redirectTo = searchParams.get('redirect') || '/';
      router.push(redirectTo);

    } catch (err: unknown) {
      // Login failed — show error message
      if (err && typeof err === 'object' && 'response' in err) {
        const axiosErr = err as { response?: { data?: { detail?: string } } };
        // Django sends {"detail": "No active account found with the given credentials"}
        setError(axiosErr.response?.data?.detail || 'Login failed. Check your email and password.');
      } else {
        setError('Something went wrong. Please try again.');
      }
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-4 py-12">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-lg p-8">

        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Welcome Back</h1>
          <p className="text-gray-500 mt-2">Log in to your Nepal Trek Connect account</p>
        </div>

        {/* Error Message Box */}
        {/* Only shows if there's an error */}
        {error && (
          <div className="bg-red-50 border border-red-300 text-red-700 rounded-lg px-4 py-3 mb-6 text-sm">
            ⚠️ {error}
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-5">

          {/* Email Field */}
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
              Email Address
            </label>
            <input
              id="email"
              type="email"
              required                    // Browser validation — must be filled
              autoComplete="email"        // Helps browser autofill
              value={formData.email}
              // onChange: every keystroke updates state
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
              // ...formData copies existing values, then email: e.target.value updates just email
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="you@example.com"
            />
          </div>

          {/* Password Field */}
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              Password
            </label>
            <input
              id="password"
              type="password"
              required
              autoComplete="current-password"
              value={formData.password}
              onChange={(e) => setFormData({ ...formData, password: e.target.value })}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Enter your password"
            />
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}   // Disable while request is in progress
            className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-semibold py-3 px-4 rounded-lg transition-colors duration-200"
          >
            {/* Show different text while loading */}
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin h-4 w-4 border-2 border-white border-t-transparent rounded-full" />
                Logging in...
              </span>
            ) : (
              'Log In'
            )}
          </button>
        </form>

        {/* Link to Register Page */}
        <p className="text-center text-sm text-gray-600 mt-6">
          Don&apos;t have an account?{' '}
          <Link href="/register" className="text-blue-600 hover:underline font-medium">
            Create one here
          </Link>
        </p>

      </div>
    </div>
  );
}