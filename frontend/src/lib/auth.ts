// ============================================================
// FILE: frontend/src/lib/auth.ts
// PURPOSE: All authentication functions in one place.
//          Login, Register, Logout, and checking if logged in.
//          Import and use these functions from any page.
// ============================================================

import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// ──────────────────────────────────────────────────────────────
// TYPE DEFINITIONS
// TypeScript needs to know the "shape" of our data.
// These define what a User object looks like, what login returns, etc.
// ──────────────────────────────────────────────────────────────

// What a User looks like (matches the Django User model fields)
export interface User {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  phone: string;
  country: string;
}

// What the login API returns
export interface AuthTokens {
  access: string;    // Short-lived token (1 day)
  refresh: string;   // Long-lived token (30 days)
  user: User;
}

// What you send to login
export interface LoginCredentials {
  email: string;
  password: string;
}

// What you send to register
export interface RegisterData {
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  password: string;
  password_confirm: string;
  phone?: string;       // ? means optional
  country?: string;
  country_code?: string;
}

// ──────────────────────────────────────────────────────────────
// LOGIN FUNCTION
// Sends email+password to Django, gets back JWT tokens + user info.
// Saves everything to localStorage so we can use it across pages.
// ──────────────────────────────────────────────────────────────
export const loginUser = async (credentials: LoginCredentials): Promise<AuthTokens> => {
  // POST /api/auth/login/ with email and password
  const response = await axios.post(`${API_URL}/api/auth/login/`, credentials);
  const data: AuthTokens = response.data;

  // Save tokens to localStorage (browser's key-value storage)
  // These persist even after closing/reopening the browser tab
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  // Save user info so we can show their name in the header without an API call
  localStorage.setItem('user', JSON.stringify(data.user));

  return data;
};

// ──────────────────────────────────────────────────────────────
// REGISTER FUNCTION
// Creates a new account. Does NOT log in automatically.
// After registering, user must go to login page.
// ──────────────────────────────────────────────────────────────
export const registerUser = async (data: RegisterData) => {
  // POST /api/auth/register/ with all the user's info
  const response = await axios.post(`${API_URL}/api/auth/register/`, data);
  return response.data;
  // Returns: { user: {...}, message: "Registration successful! Please login." }
};

// ──────────────────────────────────────────────────────────────
// LOGOUT FUNCTION
// Removes all saved tokens and user info.
// The server doesn't need to be told (tokens just expire naturally).
// ──────────────────────────────────────────────────────────────
export const logoutUser = () => {
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  localStorage.removeItem('user');
  // Redirect to home page
  window.location.href = '/';
};

// ──────────────────────────────────────────────────────────────
// CHECK IF USER IS LOGGED IN
// Returns true if we have an access token saved.
// Used to show Login vs Logout button in Header.
// ──────────────────────────────────────────────────────────────
export const isAuthenticated = (): boolean => {
  // typeof window check → needed for Next.js server-side rendering
  if (typeof window === 'undefined') return false;
  return !!localStorage.getItem('access_token');
  // !! converts any value to boolean: null → false, "token123" → true
};

// ──────────────────────────────────────────────────────────────
// GET CURRENT USER
// Returns the saved User object, or null if not logged in.
// ──────────────────────────────────────────────────────────────
export const getCurrentUser = (): User | null => {
  if (typeof window === 'undefined') return null;
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);  // Convert saved JSON string back to object
  } catch {
    return null;
  }
};