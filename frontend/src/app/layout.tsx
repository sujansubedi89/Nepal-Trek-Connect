import type { Metadata } from 'next';
import { Inter, Montserrat } from 'next/font/google';
import './globals.css';
import Header from '@/components/layout/Header';
import Footer from '@/components/layout/Footer';
import WhatsAppButton from '@/components/common/WhatsAppButton';
import ChatBot from '@/components/common/ChatBot';

const inter = Inter({ subsets: ['latin'], variable: '--font-inter' });
const montserrat = Montserrat({ subsets: ['latin'], variable: '--font-montserrat' });

export const metadata: Metadata = {
  title: 'Nepal Trek Connect - Best Trekking in Nepal | Pokhara, Annapurna, Everest',
  description: 'Discover authentic trekking experiences in Nepal. From Everest Base Camp to Annapurna Circuit. Expert guides, affordable packages, and unforgettable adventures.',
  keywords: 'trekking in Nepal, Nepal trekking, Everest Base Camp trek, Annapurna Base Camp, Mardi Himal trek, Poon Hill trek, Pokhara trekking, Himalayan trekking, best treks in Nepal, Nepal mountain trekking',
  authors: [{ name: 'Nepal Trek Connect' }],
  openGraph: {
    title: 'Nepal Trek Connect - Best Trekking Packages in Nepal',
    description: 'Experience the magic of Himalayan trekking with expert local guides. Book your dream trek today!',
    url: 'https://nepaltrekconnect.com',
    siteName: 'Nepal Trek Connect',
    images: [
      {
        url: '/images/og-image.jpg',
        width: 1200,
        height: 630,
        alt: 'Nepal Trek Connect - Himalayan Trekking',
      },
    ],
    locale: 'en_US',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Nepal Trek Connect - Best Trekking in Nepal',
    description: 'Discover authentic trekking experiences in Nepal',
    images: ['/images/twitter-image.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  verification: {
    google: 'your-google-verification-code',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable} ${montserrat.variable}`}>
      <body className="min-h-screen flex flex-col bg-gray-50">
        <Header />
        <main className="flex-grow">
          {children}
        </main>
        <Footer />
        <WhatsAppButton />
        <ChatBot />
      </body>
    </html>
  );
}