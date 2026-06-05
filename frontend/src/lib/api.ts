// ============================================================
// FILE: frontend/src/lib/api.ts
// PURPOSE: Central API client used by ALL pages to talk to the
//          Django backend. Every API call goes through this file.
// ============================================================

import axios, { AxiosError, AxiosRequestConfig } from 'axios';

// Read the backend URL from .env.local file
// NEXT_PUBLIC_ prefix means it's safe to use in the browser
// If not set, use localhost for development
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Create an axios "instance" — like a pre-configured fetch client
// All requests automatically get the base URL + JSON headers
const api = axios.create({
  baseURL: `${API_URL}/api`,   // All URLs start with /api (e.g. /api/treks/)
  headers: {
    'Content-Type': 'application/json',  // Tell server we're sending JSON
  },
});

// ──────────────────────────────────────────────────────────────
// REQUEST INTERCEPTOR
// This runs BEFORE every single API call you make.
// Purpose: automatically add the JWT token to every request.
// Without this, you'd have to manually add the token every time.
// ──────────────────────────────────────────────────────────────
api.interceptors.request.use((config) => {
  // typeof window !== 'undefined' → check we're in the browser
  // (Next.js also runs on the server where localStorage doesn't exist)
  if (typeof window !== 'undefined') {
    // Get the saved JWT token from browser storage
    // 🔑 KEY FIX: was 'token', now 'access_token' — must match what login saves!
    const token = localStorage.getItem('access_token');

    if (token) {
      // Add the token to the Authorization header
      // ✅ KEY FIX: Use backticks `` not single quotes ''
      // Single quotes: 'Bearer ${token}' → sends literal "${token}" (broken!)
      // Backticks:    `Bearer ${token}` → sends "Bearer eyJhbG..." (correct!)
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;  // Return the modified config so the request proceeds
});

// ──────────────────────────────────────────────────────────────
// RESPONSE INTERCEPTOR
// This runs AFTER every API call, before your code sees the result.
// Purpose: if we get a 401 (Unauthorized), try refreshing the token
//          automatically. If refresh fails, send user to login page.
// ──────────────────────────────────────────────────────────────
api.interceptors.response.use(
  // First function: runs on SUCCESS (status 200-299)
  // Just pass the response through unchanged
  (response) => response,

  // Second function: runs on ERROR (status 400+)
  async (error: AxiosError) => {
    // Get the original request that failed
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

    // 401 = "Unauthorized" — our access token has expired
    // _retry flag prevents infinite loops (don't retry the refresh itself)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;  // Mark that we've already tried once

      if (typeof window !== 'undefined') {
        // Try to get a new access token using the refresh token
        const refreshToken = localStorage.getItem('refresh_token');

        if (refreshToken) {
          try {
            // Call the Django refresh endpoint
            const { data } = await axios.post(`${API_URL}/api/auth/refresh/`, {
              refresh: refreshToken,
            });

            // Save the new access token
            // ✅ KEY FIX: Save as 'access_token' to match what we read above
            localStorage.setItem('access_token', data.access);

            // Update the failed request's header with the new token
            if (!originalRequest.headers) {
              originalRequest.headers = {};
            }
            originalRequest.headers.Authorization = `Bearer ${data.access}`;

            // Retry the original request with the new token
            return api(originalRequest);
          } catch {
            // Refresh failed — token is totally expired, must login again
            localStorage.removeItem('access_token');
            localStorage.removeItem('refresh_token');
            localStorage.removeItem('user');
            // Redirect to login page
            window.location.href = '/login';
          }
        } else {
          // No refresh token exists at all → user was never logged in
          window.location.href = '/login';
        }
      }
    }

    // For all other errors (400, 403, 404, 500...), just reject normally
    // The calling code will catch this in its try/catch
    return Promise.reject(error);
  }
);

export default api;