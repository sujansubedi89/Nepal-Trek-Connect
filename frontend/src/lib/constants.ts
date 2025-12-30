export const SITE_NAME='Nepal Trek Connect';
export const SITE_DESCRIPTION='Discover the best trekking routes in Nepal.Expert guides,affordable packages and  unforgettable experiences await you.';
export const CONTACT_PHONE='+9779846958184';
export const CONTACT_EMAIL='sujansubedinpnp@gmail.com';
export const WHATSAPP_NUMBER=process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '9779846958184';
export const DIFFICULTY_LABELS:Record<string,string>={
    easy:'Easy',
    easy_moderate:'Easy to Moderate',
    moderate:'Moderate',
    challenging:`Challenging`,
    very_challenging:'Very Challenging',
};


export const DIFFICULTY_COLORS:Record<string,string>={
    easy:'bg-green-100 text-green-800',
    easy_moderate:'bg-green-100 text-green-800',  
             moderate: 'bg-yellow-100 text-yellow-800',
  moderate_challenging: 'bg-orange-100 text-orange-800',
  challenging: 'bg-red-100 text-red-800',
  very_challenging: 'bg-red-100 text-red-800',
};

export const POPULAR_KEYWORDS = [
  'Everest Base Camp',
  'Annapurna Base Camp',
  'Mardi Himal',
  'Poon Hill',
  'Manaslu Circuit',
  'Langtang Valley',
  'Upper Mustang',
  'Gokyo Lakes',
  'Trekking in Nepal',
  'Nepal Trekking Packages',
  'Himalayan Trekking',
  'Best Treks in Nepal',
];