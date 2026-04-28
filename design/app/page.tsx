"use client";

import React, { useState } from "react";

export default function Home() {
  const [rating, setRating] = useState(4.0);

  return (
    <div className="min-h-screen bg-surface font-body-md text-on-background selection:bg-secondary-container selection:text-on-secondary-container">
      {/* TopNavBar Shell */}
      <nav className="bg-white/90 dark:bg-slate-950/90 backdrop-blur-lg border-b border-slate-100 dark:border-slate-800 shadow-sm antialiased top-0 sticky z-50">
        <div className="flex justify-between items-center px-4 md:px-12 py-4 w-full">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-black tracking-tighter text-primary">Zomato AI</span>
          </div>
          <div className="hidden md:flex items-center gap-8">
            <a className="text-primary font-bold border-b-2 border-primary pb-1" href="#">Home</a>
            <a className="text-slate-600 dark:text-slate-400 font-medium hover:text-primary transition-colors duration-200" href="#">AI Discovery</a>
            <a className="text-slate-600 dark:text-slate-400 font-medium hover:text-primary transition-colors duration-200" href="#">Trending</a>
            <a className="text-slate-600 dark:text-slate-400 font-medium hover:text-primary transition-colors duration-200" href="#">History</a>
          </div>
          <div className="flex items-center gap-4">
            <button className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer">notifications</button>
            <button className="material-symbols-outlined text-on-surface-variant hover:text-primary transition-colors cursor-pointer">account_circle</button>
          </div>
        </div>
      </nav>

      {/* Hero Section with Search Form */}
      <header 
        className="min-h-[750px] flex flex-col items-center justify-center px-6 relative"
        style={{
          backgroundImage: `linear-gradient(rgba(0, 0, 0, 0.5), rgba(183, 18, 42, 0.4), rgba(0, 0, 0, 0.7)), url('https://lh3.googleusercontent.com/aida-public/AB6AXuDmdzh6f1ZSRxdK78en13bXrBOOQaVOsvjSAOkMX-caKUodVLKl_Q8yJ5be8JblppXasifFJRwF5ua7xtwhX1hstwfz7_btLEgXC3QxgKEVAmT290XSXnvNLYlE71HnZYiwby-R5FJqzvUTD6ePcNNHx_EMWLqX1iGyjjVJgPTkTlbBrqrrokzyHWz5jwh7nLHe8r71nSonc4zIWjaV8OXDGi6AvnUJH12PS2eN5-ZbKKk9rCCam6suu31hyl2rW1Y700qOH_G-cPHw')`,
          backgroundSize: 'cover',
          backgroundPosition: 'center',
          backgroundAttachment: 'fixed'
        }}
      >
        <div className="absolute inset-0 backdrop-blur-[2px] pointer-events-none"></div>
        <div className="max-w-4xl w-full text-center mb-10 relative z-10">
          <h1 className="font-display text-white text-5xl md:text-6xl font-extrabold drop-shadow-2xl mb-4">Craving something specific?</h1>
          <p className="font-body-lg text-white/95 text-lg md:text-xl max-w-xl mx-auto drop-shadow-md">Let Zomato AI find the perfect table for your taste, mood, and budget.</p>
        </div>

        {/* Glassmorphism Search Form */}
        <div className="max-w-5xl w-full bg-black/40 backdrop-blur-xl border border-white/20 p-8 rounded-2xl shadow-2xl relative z-10">
          <form className="grid grid-cols-1 md:grid-cols-12 gap-6">
            {/* Location Field */}
            <div className="md:col-span-4 relative">
              <label className="block text-white text-label-sm font-semibold mb-2 px-1">Location</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary">location_on</span>
                <input className="w-full bg-white border-none rounded-lg py-3.5 pl-10 pr-4 text-on-surface focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="Search locality or area..." type="text"/>
              </div>
            </div>

            {/* Cuisine Field */}
            <div className="md:col-span-4 relative">
              <label className="block text-white text-label-sm font-semibold mb-2 px-1">Cuisine (Optional)</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary">restaurant</span>
                <input className="w-full bg-white border-none rounded-lg py-3.5 pl-10 pr-4 text-on-surface focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="Italian, Mughlai, Chinese..." type="text"/>
              </div>
            </div>

            {/* Budget Field */}
            <div className="md:col-span-4 relative">
              <label className="block text-white text-label-sm font-semibold mb-2 px-1">Budget</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary">payments</span>
                <input className="w-full bg-white border-none rounded-lg py-3.5 pl-10 pr-4 text-on-surface focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="Enter budget in ₹" type="number"/>
              </div>
            </div>

            {/* Rating Field: Slider + Number Sync */}
            <div className="md:col-span-4 bg-white/10 p-4 rounded-lg flex flex-col justify-center">
              <div className="flex justify-between items-center mb-3">
                <label className="text-white text-label-sm font-semibold">Min Rating</label>
                <div className="flex items-center gap-2">
                  <input 
                    className="w-12 bg-white/20 border-none rounded py-1 px-1 text-center text-white text-sm font-bold focus:ring-1 focus:ring-primary outline-none" 
                    max="5" min="1" step="0.1" type="number" 
                    value={rating}
                    onChange={(e) => setRating(parseFloat(e.target.value))}
                  />
                  <span className="text-red-400 text-xs font-bold uppercase tracking-tight">Stars</span>
                </div>
              </div>
              <input 
                className="w-full accent-primary h-1.5 rounded-full cursor-pointer" 
                max="5" min="1" step="0.1" type="range" 
                value={rating}
                onChange={(e) => setRating(parseFloat(e.target.value))}
              />
            </div>

            {/* Extra Preferences */}
            <div className="md:col-span-5 relative">
              <label className="block text-white text-label-sm font-semibold mb-2 px-1">Extra Preferences (Optional)</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-primary">psychology</span>
                <input className="w-full bg-white border-none rounded-lg py-3.5 pl-10 pr-4 text-on-surface focus:ring-2 focus:ring-primary outline-none transition-all" placeholder="e.g. 'Quiet romantic date', 'Pet friendly'..." type="text"/>
              </div>
            </div>

            {/* Find Places Button */}
            <div className="md:col-span-3 flex items-end">
              <button className="w-full bg-primary hover:bg-secondary text-white font-bold py-3.5 rounded-lg transition-all transform active:scale-95 shadow-lg flex items-center justify-center gap-2" type="button">
                <span className="material-symbols-outlined">search</span>
                Find Places
              </button>
            </div>
          </form>
        </div>
      </header>

      {/* Results Section */}
      <main className="max-w-7xl mx-auto px-6 py-16">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end mb-10 gap-4">
          <div>
            <h2 className="font-headline-lg text-3xl font-bold text-on-surface">Top AI Recommendations</h2>
            <p className="text-on-surface-variant">Handpicked matches based on your unique preferences</p>
          </div>
          <div className="flex gap-2">
            <button className="bg-white border border-outline-variant px-5 py-2.5 rounded-full text-label-lg font-semibold flex items-center gap-2 hover:bg-surface-container transition-colors shadow-sm text-on-surface">
              <span className="material-symbols-outlined text-base">tune</span>
              Refine Results
            </button>
          </div>
        </div>

        {/* Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-md">
          {/* Restaurant Card 1 */}
          <div className="group bg-surface-container-lowest rounded-xl overflow-hidden border border-surface-container shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="h-60 relative overflow-hidden">
              <img 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                alt="modern upscale italian restaurant interior" 
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuCibHG-4SVLaoGi95viIlIFaG_Z2RGwk3YRqusfLnCl8rjqnW3FIir_2rgW71nTK3mWITSFpZ1zgAxvA4Dw_bayrajKnYd59H-TK3YCMrJSn1H9CjrsPV3BUxIzoLq7L4-M5TVBA0-p_uOmlb8pB5K6iMMrmhaTIL_iMJVEz9WjN9b_jxlSzbrrlKcyQRB_9rXWLZLlkebauGCroXIZSo5qSe0z83Dm2wd-YSRMINfjtE_7nfy91fpFcywj4QlVGzcaOdF0stnVfR4A"
              />
              <div className="absolute top-3 right-3 bg-tertiary-container text-white px-2.5 py-1 rounded-lg text-label-sm font-bold flex items-center gap-1 shadow-md">
                4.8 <span className="material-symbols-outlined text-[14px]">star</span>
              </div>
            </div>
            <div className="p-5">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-headline-md text-xl font-bold text-on-surface">The Glass House</h3>
                <span className="text-on-surface-variant font-medium">₹₹₹₹</span>
              </div>
              <div className="flex items-center gap-1 text-on-surface-variant text-label-sm mb-4">
                <span className="material-symbols-outlined text-[16px]">location_on</span>
                Indiranagar, Bangalore
              </div>
              {/* AI Snippet */}
              <div className="bg-primary/5 border border-primary-container/10 rounded-lg p-3 flex gap-2">
                <span className="material-symbols-outlined text-primary text-[20px]">auto_awesome</span>
                <p className="text-label-sm text-on-surface italic leading-snug">"Matches your request for 'Quiet Romantic Dinners' with 98% compatibility. Excellent mood lighting."</p>
              </div>
            </div>
          </div>

          {/* Restaurant Card 2 */}
          <div className="group bg-surface-container-lowest rounded-xl overflow-hidden border border-surface-container shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="h-60 relative overflow-hidden">
              <img 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                alt="close-up of colorful north indian thali" 
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuAesF9cCy0shfw2FlHfC3WpRyw7h4KmA14c1uTyaKPS63xmv5D5YnjKZMuFJTYjWEAlRL2KVT7DWWwqA1cJIIkSj-q2JIToEfJ1tzQpI-0KyW6E00E1KCG9qBHBlnAHn6u4LVj_MWK_vbRd9Ym7oJKu72EEuAMHA9u9VNN1Ma7uBke_KG_-91T53nfeNaYaaXzeYP3mXSfMXFi8_MxCfOmDNvhsl6S1cyAjwgHAMjYXVsuV8484tYH_9ucpaJsPHCZxkBiUjnaY2sMP"
              />
              <div className="absolute top-3 right-3 bg-tertiary-container text-white px-2.5 py-1 rounded-lg text-label-sm font-bold flex items-center gap-1 shadow-md">
                4.5 <span className="material-symbols-outlined text-[14px]">star</span>
              </div>
            </div>
            <div className="p-5">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-headline-md text-xl font-bold text-on-surface">Spice Artisan</h3>
                <span className="text-on-surface-variant font-medium">₹₹</span>
              </div>
              <div className="flex items-center gap-1 text-on-surface-variant text-label-sm mb-4">
                <span className="material-symbols-outlined text-[16px]">location_on</span>
                Connaught Place, Delhi
              </div>
              {/* AI Snippet */}
              <div className="bg-primary/5 border border-primary-container/10 rounded-lg p-3 flex gap-2">
                <span className="material-symbols-outlined text-primary text-[20px]">auto_awesome</span>
                <p className="text-label-sm text-on-surface italic leading-snug">"Top choice for authentic Mughlai. Your budget preference fits perfectly here for a group of four."</p>
              </div>
            </div>
          </div>

          {/* Restaurant Card 3 */}
          <div className="group bg-surface-container-lowest rounded-xl overflow-hidden border border-surface-container shadow-sm hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
            <div className="h-60 relative overflow-hidden">
              <img 
                className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" 
                alt="stylish outdoor rooftop cafe" 
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuDB6vRbrnzKWkR6MhBC2j-r7MbZb8ctt3QPVJl-AYY9vKJalMAflI4n4ZyIOLwkMsBFV36qsM6-Z4UtVsRJAiwdS5ldSjfbmSw_Zq8qalLEf6iVNGPUOyBiDcugOSNdHINUr7isJcVCHiKi3L8WJPyr_wGnOgzFsFhfc3xyJ6LWk2t37Z25g4JRhDHiZaRvFp0BaQ1QwxTeL24NlsSFQOp2hQCcHY05a_fKHJ-U0YKmKg8BPnCiLRONPvg8Vnp2sxf4yKqRaORaogCp"
              />
              <div className="absolute top-3 right-3 bg-tertiary-container text-white px-2.5 py-1 rounded-lg text-label-sm font-bold flex items-center gap-1 shadow-md">
                4.2 <span className="material-symbols-outlined text-[14px]">star</span>
              </div>
            </div>
            <div className="p-5">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-headline-md text-xl font-bold text-on-surface">Cloud Nine Cafe</h3>
                <span className="text-on-surface-variant font-medium">₹₹₹</span>
              </div>
              <div className="flex items-center gap-1 text-on-surface-variant text-label-sm mb-4">
                <span className="material-symbols-outlined text-[16px]">location_on</span>
                Bandra West, Mumbai
              </div>
              {/* AI Snippet */}
              <div className="bg-primary/5 border border-primary-container/10 rounded-lg p-3 flex gap-2">
                <span className="material-symbols-outlined text-primary text-[20px]">auto_awesome</span>
                <p className="text-label-sm text-on-surface italic leading-snug">"Matches your pet-friendly filter. Known for high ratings on Sunday brunches and open-air seating."</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer Shell */}
      <footer className="bg-slate-50 dark:bg-slate-900 border-t border-slate-200 dark:bg-slate-800 text-sm py-12 mt-auto">
        <div className="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="flex flex-col gap-4">
            <span className="text-xl font-black text-slate-900 dark:text-white">Zomato AI</span>
            <p className="text-slate-500 dark:text-slate-400 max-w-sm">Discovering the soul of cities through the language of food. Powered by next-gen culinary intelligence.</p>
            <p className="text-slate-500 dark:text-slate-400 mt-4">© 2024 Zomato AI Ltd. All rights reserved.</p>
          </div>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="flex flex-col gap-2">
              <span className="font-bold text-slate-900 dark:text-white mb-2">Company</span>
              <a className="text-slate-500 dark:text-slate-400 hover:underline hover:text-primary transition-all" href="#">About</a>
              <a className="text-slate-500 dark:text-slate-400 hover:underline hover:text-primary transition-all" href="#">Contact</a>
            </div>
            <div className="flex flex-col gap-2">
              <span className="font-bold text-slate-900 dark:text-white mb-2">Legal</span>
              <a className="text-slate-500 dark:text-slate-400 hover:underline hover:text-primary transition-all" href="#">Privacy</a>
              <a className="text-slate-500 dark:text-slate-400 hover:underline hover:text-primary transition-all" href="#">Terms</a>
            </div>
            <div className="flex flex-col gap-2">
              <span className="font-bold text-slate-900 dark:text-white mb-2">Sitemap</span>
              <a className="text-slate-500 dark:text-slate-400 hover:underline hover:text-primary transition-all" href="#">Sitemap</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
