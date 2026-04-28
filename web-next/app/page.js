'use client';

import { useEffect, useState } from 'react';

export default function Home() {
  const streamlitUrl = process.env.NEXT_PUBLIC_STREAMLIT_APP_URL;
  const [countdown, setCountdown] = useState(5);

  useEffect(() => {
    if (streamlitUrl) {
      // Countdown timer
      const countInterval = setInterval(() => {
        setCountdown((prev) => (prev > 1 ? prev - 1 : 1));
      }, 1000);

      // Redirect after 5 seconds
      const redirectTimer = setTimeout(() => {
        window.location.href = streamlitUrl;
      }, 5000);

      return () => {
        clearInterval(countInterval);
        clearTimeout(redirectTimer);
      };
    }
  }, [streamlitUrl]);

  if (!streamlitUrl) {
    return (
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh', 
        backgroundColor: '#0b0f19', 
        color: '#fafafa',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        padding: '2rem',
        textAlign: 'center'
      }}>
        <h1 style={{ color: '#E23744', fontSize: '2.5rem', fontWeight: '800', marginBottom: '1rem' }}>
          Configuration Missing
        </h1>
        <p style={{ color: '#94a3b8', fontSize: '1.2rem' }}>
          Please assign <code>NEXT_PUBLIC_STREAMLIT_APP_URL</code> in Vercel.
        </p>
      </div>
    );
  }

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column', 
      alignItems: 'center', 
      justifyContent: 'center', 
      height: '100vh', 
      backgroundColor: '#0b0f19',
      backgroundImage: 'radial-gradient(circle at 50% 30%, rgba(183, 18, 42, 0.25), transparent 60%)',
      fontFamily: 'system-ui, -apple-system, sans-serif',
      color: '#fafafa',
      textAlign: 'center',
      padding: '2rem'
    }}>
      <div style={{
        background: 'rgba(255, 255, 255, 0.04)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        padding: '3.5rem',
        borderRadius: '1.5rem',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.5)',
        maxWidth: '500px',
        width: '90%'
      }}>
        <h1 style={{ 
          fontSize: '2.5rem', 
          fontWeight: '800', 
          letterSpacing: '-0.04em', 
          marginBottom: '1rem',
          color: 'white'
        }}>
          Zomato<span style={{ color: '#E23744' }}>AI</span>
        </h1>
        
        <div style={{
          width: '50px',
          height: '50px',
          border: '3px solid rgba(226, 55, 68, 0.2)',
          borderTop: '3px solid #E23744',
          borderRadius: '50%',
          margin: '2rem auto',
          animation: 'spin 1s linear infinite'
        }} />
        
        <h2 style={{ fontSize: '1.3rem', fontWeight: '600', marginBottom: '0.5rem' }}>
          Connecting to Recommender
        </h2>
        <p style={{ color: '#94a3b8', fontSize: '1rem' }}>
          Redirecting you automatically in {countdown} seconds...
        </p>
      </div>
      
      <style jsx global>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}



