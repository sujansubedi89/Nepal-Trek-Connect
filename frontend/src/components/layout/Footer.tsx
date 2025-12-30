import React from 'react';
import Link from 'next/link';
import { FaFacebook, FaInstagram, FaTwitter, FaWhatsapp, FaEnvelope, FaPhone, FaMapMarkerAlt } from 'react-icons/fa';
import { SITE_NAME, CONTACT_EMAIL, CONTACT_PHONE } from '@/lib/constants';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    quickLinks: [
      { name: 'About Us', href: '/about' },
      { name: 'All Treks', href: '/treks' },
      { name: 'Contact Us', href: '/contact' },
      { name: 'Privacy Policy', href: '/privacy' },
      { name: 'Terms & Conditions', href: '/terms' },
    ],
    popularTreks: [
      { name: 'Everest Base Camp', href: '/treks/everest-base-camp-trek-14-days' },
      { name: 'Annapurna Base Camp', href: '/treks/annapurna-base-camp-trek-10-days' },
      { name: 'Mardi Himal Trek', href: '/treks/mardi-himal-trek-8-days' },
      { name: 'Poon Hill Trek', href: '/treks/ghorepani-poon-hill-trek-5-days' },
      { name: 'Manaslu Circuit', href: '/treks/manaslu-circuit-trek-15-days' },
    ],
  };

  return (
    <footer className="bg-gray-900 text-gray-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <h3 className="text-2xl font-heading font-bold text-white mb-4">
              {SITE_NAME}
            </h3>
            <p className="text-sm mb-4">
              Your trusted partner for authentic trekking experiences in Nepal. 
              Explore the Himalayas with expert local guides.
            </p>
            <div className="flex space-x-4">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="hover:text-primary-400 transition-colors">
                <FaFacebook size={20} />
              </a>
              <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="hover:text-primary-400 transition-colors">
                <FaInstagram size={20} />
              </a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:text-primary-400 transition-colors">
                <FaTwitter size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Quick Links</h4>
            <ul className="space-y-2">
              {footerLinks.quickLinks.map((link) => (
                <li key={link.name}>
                  <Link
                    href={link.href}
                    className="text-sm hover:text-primary-400 transition-colors"
                  >
                    {link.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Popular Treks */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Popular Treks</h4>
            <ul className="space-y-2">
              {footerLinks.popularTreks.map((trek) => (
                <li key={trek.name}>
                  <Link
                    href={trek.href}
                    className="text-sm hover:text-primary-400 transition-colors"
                  >
                    {trek.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h4 className="text-lg font-semibold text-white mb-4">Contact Us</h4>
            <div className="space-y-3">
              <div className="flex items-start space-x-3">
                <FaMapMarkerAlt className="text-primary-400 mt-1 flex-shrink-0" />
                <span className="text-sm">Lakeside, Pokhara, Nepal</span>
              </div>
              <div className="flex items-center space-x-3">
                <FaPhone className="text-primary-400 flex-shrink-0" />
                <a href={`tel:${CONTACT_PHONE}`} className="text-sm hover:text-primary-400">
                  {CONTACT_PHONE}
                </a>
              </div>
              <div className="flex items-center space-x-3">
                <FaWhatsapp className="text-primary-400 flex-shrink-0" />
                <a href={`https://wa.me/9779846958184`} className="text-sm hover:text-primary-400">
                  WhatsApp: +977 9846958184
                </a>
              </div>
              <div className="flex items-center space-x-3">
                <FaEnvelope className="text-primary-400 flex-shrink-0" />
                <a href={`mailto:${CONTACT_EMAIL}`} className="text-sm hover:text-primary-400">
                  {CONTACT_EMAIL}
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="mt-12 pt-8 border-t border-gray-800 text-center text-sm">
          <p>&copy; {currentYear} {SITE_NAME}. All rights reserved.</p>
          <p className="mt-2">
            Built with ❤️ for adventurers worldwide Sujan Subedi | 
            <Link href="https:www.sujansubedi12.com.np" className="text-primary-400 hover:underline ml-1">
              Link
            </Link>
          </p>
        </div>
      </div>
    </footer>
  );
}