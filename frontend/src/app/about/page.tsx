import React from 'react';
import Link from 'next/link';
import Header   from '@/components/layout/Header';  
import Footer from '@/components/layout/Footer';
export const metadata={
    title:'About Us - Nepal Trek Connect',
    description:'Learn more about Nepal Trek Connect, your trusted partner for authentic trekking experiences in Nepal. Meet our team and discover our mission to provide unforgettable adventures in the Himalayas.',
    keywords:'about Nepal Trek Connect, trekking company Nepal, Himalayan adventures, trekking guides Nepal, Nepal trekking experiences'
};
const AboutPage:React.FC=()=>{
    return(
        <div className='flex flex-col min-h-screen'>
            {/* <Header/> */}
            <main className='flex-grow p-8 max-w-4xl mx-auto'>
                {/* H1: Primary keyword placement and clear brand identity */}
        {/* H1 Tag should contain the main keyword: Trekking in Nepal */}
        <h1 className="text-5xl font-extrabold mb-8 text-indigo-700 border-b-4 border-indigo-200 pb-2">
          Nepal Trek Connect: Your Authentic Trekking Partner in Nepal
        </h1>

        {/* --- SECTION 1: THE VISION (TRUST & LOCAL EXPERTISE) --- */}
        <section className="mb-12">
          {/* H2: Secondary Keywords & Core Value - e.g., "Local Experts" */}
          <h2 className="text-3xl font-bold mb-4 text-gray-800">
            Connecting You to the Heart of the Himalayas
          </h2>
          <p className="text-lg text-gray-700 leading-relaxed mb-4">
            At **Nepal Trek Connect**, we are more than just a trekking agency; we are lifelong mountaineers and local experts dedicated to sharing the majestic beauty of our home. Based right here in Kathmandu, we specialize in organizing safe, sustainable, and unforgettable **treks across Nepal mountains**. From the challenging heights of **Everest Base Camp** to the cultural trails of the **Annapurna Circuit**, our roots run deep in the very trails you will walk.
          </p>
          <p className="text-lg font-semibold text-gray-700">
            Our mission is simple: to connect every adventurer with the real, authentic Nepal.
          </p>
        </section>

        {/* --- SECTION 2: WHY CHOOSE US (TRUST SIGNALS & KEY BENEFITS) --- */}
        <section className="mb-12 bg-indigo-50 p-6 rounded-lg shadow-inner">
          {/* H2: Transactional keywords & Call to Value */}
          <h2 className="text-3xl font-bold mb-6 text-indigo-600">
            Why We Are the Best Choice for Your Mountain Adventure
          </h2>
          
          <div className="grid md:grid-cols-3 gap-6">
            <div className="p-4 border-l-4 border-indigo-400">
              <h3 className="text-xl font-semibold mb-2">🏔️ All-Mountain Expertise</h3>
              <p className="text-gray-700">
                We cover **all mountain regions** in Nepal. Our guides are highly certified for high-altitude environments, ensuring your trek to destinations like **Manaslu** or **Gokyo Lakes** is managed with precision safety protocols.
              </p>
            </div>
            <div className="p-4 border-l-4 border-indigo-400">
              <h3 className="text-xl font-semibold mb-2">⭐ Safety & Licensed Guides</h3>
              <p className="text-gray-700">
                Safety is our top priority. We use only **Government-Licensed Trekking Guides** who are first-aid certified. We manage all logistics, permits, and emergency evacuation access, giving you complete peace of mind.
              </p>
            </div>
            <div className="p-4 border-l-4 border-indigo-400">
              <h3 className="text-xl font-semibold mb-2">🌿 Sustainable & Local Impact</h3>
              <p className="text-gray-700">
                We are committed to eco-friendly practices (Leave No Trace). By hiring exclusively local porters and guides, your journey directly supports the economic well-being of the Himalayan communities we visit.
              </p>
            </div>
          </div>
        </section>
        
        {/* --- SECTION 3: CALL TO ACTION (CTA) & NEXT STEP --- */}
        <section className="text-center pt-6">
          <h2 className="text-3xl font-bold mb-4 text-gray-800">
            Ready to Experience the Himalayas?
          </h2>
          <p className="text-xl text-gray-600 mb-6">
            Let us customize your perfect **Nepal trek package** today.
          </p>
          <Link
            href="/treks" // Link to your main trekking packages page (high-value SEO link)
            className="inline-block bg-indigo-600 hover:bg-indigo-700 text-white text-xl font-bold py-3 px-8 rounded-full transition duration-300 shadow-lg"
          >
           View All Trekking Adventures
          </Link>
           
        </section>

      </main>

      {/* Renders the global footer */}
      {/* <Footer /> */}
      
    </div>
  );
};

export default AboutPage;