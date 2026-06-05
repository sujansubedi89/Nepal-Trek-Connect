'use client';
// ============================================================
// FILE: frontend/src/components/layout/Header.tsx
// PURPOSE: Top navigation bar shown on every page.
//          Shows Login/Register links when NOT logged in.
//          Shows user name + Logout button when logged in.
// ============================================================

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { usePathname, useRouter } from 'next/navigation';
import { FaBars, FaTimes, FaUser } from 'react-icons/fa';
import { SITE_NAME } from '@/lib/constants';
import { isAuthenticated, getCurrentUser, logoutUser } from '@/lib/auth';

export default function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const pathname = usePathname();
  const router = useRouter();

  // Auth state — track whether user is logged in
  // We use state here so the header re-renders when auth changes
  const [loggedIn, setLoggedIn] = useState(false);
  const [userName, setUserName] = useState('');

  // Check auth state when component mounts (page loads)
  // and whenever the pathname changes (user navigates to new page)
  useEffect(() => {
    const authenticated = isAuthenticated();
    setLoggedIn(authenticated);

    if (authenticated) {
      const user = getCurrentUser();
      if (user) {
        // Show first name if available, otherwise email
        setUserName(user.first_name || user.email);
      }
    }
  }, [pathname]);  // Re-check whenever URL changes

  // Scroll detection — adds shadow to header when scrolled
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Handle logout button click
  const handleLogout = () => {
    logoutUser();       // Clears localStorage
    setLoggedIn(false);
    setUserName('');
    router.push('/');   // Go to home page
  };

  const navigation = [
    { name: 'Home', href: '/' },
    { name: 'Treks', href: '/treks' },
    { name: 'About', href: '/about' },
    { name: 'Contact', href: '/contact' },
  ];

  return (
    <header
      className={`sticky top-0 z-50 transition-all duration-300 ${
        isScrolled ? 'bg-white shadow-md' : 'bg-white'
      }`}
    >
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16 md:h-20">

          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="text-2xl md:text-3xl font-heading font-bold text-primary-600">
              {SITE_NAME}
            </div>
          </Link>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                className={`text-sm font-medium transition-colors duration-200 ${
                  pathname === item.href
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-700 hover:text-primary-600'
                }`}
              >
                {item.name}
              </Link>
            ))}

            {/* ── AUTH BUTTONS ── */}
            {/* Show different buttons depending on login state */}
            {loggedIn ? (
              // LOGGED IN: show username + logout button
              <div className="flex items-center gap-3">
                {/* User name display */}
                <span className="flex items-center gap-1 text-sm text-gray-700">
                  <FaUser className="text-primary-600" size={14} />
                  {userName}
                </span>
                {/* Logout button */}
                <button
                  onClick={handleLogout}
                  className="text-sm font-medium text-gray-700 hover:text-red-600 transition-colors"
                >
                  Logout
                </button>
              </div>
            ) : (
              // NOT LOGGED IN: show login + register links
              <div className="flex items-center gap-3">
                <Link
                  href="/login"
                  className="text-sm font-medium text-gray-700 hover:text-primary-600 transition-colors"
                >
                  Log In
                </Link>
                <Link
                  href="/register"
                  className="text-sm font-medium bg-primary-600 text-white px-4 py-2 rounded-lg hover:bg-primary-700 transition-colors"
                >
                  Register
                </Link>
              </div>
            )}

            <Link href="/treks" className="btn-primary">
              Book Now
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="md:hidden text-gray-700 hover:text-primary-600"
          >
            {isMenuOpen ? <FaTimes size={24} /> : <FaBars size={24} />}
          </button>
        </div>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden py-4 space-y-2 border-t">
            {navigation.map((item) => (
              <Link
                key={item.name}
                href={item.href}
                onClick={() => setIsMenuOpen(false)}
                className={`block py-2 px-4 rounded-lg transition-colors ${
                  pathname === item.href
                    ? 'bg-primary-50 text-primary-600 font-semibold'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                {item.name}
              </Link>
            ))}

            {/* Mobile Auth Links */}
            {loggedIn ? (
              <>
                <span className="block py-2 px-4 text-gray-600 text-sm">
                  👤 {userName}
                </span>
                <button
                  onClick={() => { handleLogout(); setIsMenuOpen(false); }}
                  className="block w-full text-left py-2 px-4 text-red-600 hover:bg-red-50 rounded-lg"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  onClick={() => setIsMenuOpen(false)}
                  className="block py-2 px-4 text-gray-700 hover:bg-gray-100 rounded-lg"
                >
                  Log In
                </Link>
                <Link
                  href="/register"
                  onClick={() => setIsMenuOpen(false)}
                  className="block py-2 px-4 bg-gray-100 text-gray-800 rounded-lg"
                >
                  Register
                </Link>
              </>
            )}

            <Link
              href="/treks"
              onClick={() => setIsMenuOpen(false)}
              className="block py-2 px-4 bg-primary-600 text-white text-center rounded-lg font-semibold"
            >
              Book Now
            </Link>
          </div>
        )}
      </nav>
    </header>
  );
}