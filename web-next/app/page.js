'use client';

import { useEffect } from 'react';

export default function Home() {
  const streamlitUrl = process.env.NEXT_PUBLIC_STREAMLIT_APP_URL;

  useEffect(() => {
    if (streamlitUrl) {
      window.location.href = streamlitUrl;
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
      fontFamily: 'system-ui, -apple-system, sans-serif',
      color: '#fafafa',
      textAlign: 'center'
    }}>
      <h1>Redirecting...</h1>
    </div>
  );
}




