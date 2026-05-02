'use client';

import { useState, useEffect } from 'react';

export default function Home() {
  const [locations, setLocations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  
  const [formData, setFormData] = useState({
    location: '',
    cuisine: '',
    min_rating: 0,
    max_budget: 1000,
    extra_preferences: ''
  });

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';

  useEffect(() => {
    async function fetchLocations() {
      try {
        const res = await fetch(`${apiUrl}/locations`);
        if (!res.ok) throw new Error('Failed to fetch locations');
        const data = await res.json();
        setLocations(data);
      } catch (err) {
        console.error('Error fetching locations:', err);
      }
    }
    fetchLocations();
  }, [apiUrl]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults([]);

    try {
      const res = await fetch(`${apiUrl}/recommend`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!res.ok) throw new Error('Failed to get recommendations');
      
      const data = await res.json();
      if (data.reason_code !== 'SUCCESS') {
        setError(`No matches found: ${data.reason_code.replace(/_/g, ' ')}`);
      } else {
        setResults(data.results);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: '800px', margin: '0 auto', padding: '2rem' }}>
      <header style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <h1 style={{ fontSize: '3rem', fontWeight: '800', marginBottom: '0.5rem' }}>
          Zomato<span style={{ color: 'var(--primary)' }}>AI</span>
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.2rem' }}>
          Personalized restaurant recommendations powered by AI
        </p>
      </header>

      <section className="glass" style={{ padding: '2rem', marginBottom: '3rem' }}>
        <form onSubmit={handleSubmit} style={{ display: 'grid', gap: '1.5rem' }}>
          <div style={{ display: 'grid', gap: '0.5rem' }}>
            <label style={{ fontWeight: '600', fontSize: '0.9rem' }}>📍 Select Location</label>
            <select 
              required
              style={{ padding: '0.8rem', borderRadius: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--card-border)', color: 'white' }}
              value={formData.location}
              onChange={(e) => setFormData({...formData, location: e.target.value})}
            >
              <option value="" disabled style={{ background: '#1a1a1a' }}>Where do you want to eat?</option>
              {locations.map(loc => (
                <option key={loc} value={loc} style={{ background: '#1a1a1a' }}>{loc}</option>
              ))}
            </select>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              <label style={{ fontWeight: '600', fontSize: '0.9rem' }}>🍳 Cuisine (Optional)</label>
              <input 
                type="text"
                placeholder="e.g. Italian, Chinese"
                style={{ padding: '0.8rem', borderRadius: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--card-border)', color: 'white' }}
                value={formData.cuisine}
                onChange={(e) => setFormData({...formData, cuisine: e.target.value})}
              />
            </div>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              <label style={{ fontWeight: '600', fontSize: '0.9rem' }}>⭐ Min Rating: {formData.min_rating}</label>
              <input 
                type="range" min="0" max="5" step="0.1"
                style={{ cursor: 'pointer', accentColor: 'var(--primary)' }}
                value={formData.min_rating}
                onChange={(e) => setFormData({...formData, min_rating: parseFloat(e.target.value)})}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              <label style={{ fontWeight: '600', fontSize: '0.9rem' }}>💰 Max Budget for Two (₹)</label>
              <input 
                type="number"
                style={{ padding: '0.8rem', borderRadius: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--card-border)', color: 'white' }}
                value={formData.max_budget}
                onChange={(e) => setFormData({...formData, max_budget: parseInt(e.target.value)})}
              />
            </div>
            <div style={{ display: 'grid', gap: '0.5rem' }}>
              <label style={{ fontWeight: '600', fontSize: '0.9rem' }}>✨ Extra Preferences</label>
              <input 
                type="text"
                placeholder="e.g. outdoor seating"
                style={{ padding: '0.8rem', borderRadius: '0.5rem', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--card-border)', color: 'white' }}
                value={formData.extra_preferences}
                onChange={(e) => setFormData({...formData, extra_preferences: e.target.value})}
              />
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading}
            style={{ 
              background: 'linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%)',
              color: 'white',
              padding: '1rem',
              borderRadius: '0.75rem',
              border: 'none',
              fontWeight: '700',
              cursor: loading ? 'not-allowed' : 'pointer',
              marginTop: '0.5rem',
              transition: 'transform 0.2s',
              opacity: loading ? 0.7 : 1
            }}
          >
            {loading ? 'Finding Places...' : 'Find Recommendations'}
          </button>
        </form>
      </section>

      {error && (
        <div className="glass animate-fade-in" style={{ padding: '1.5rem', textAlign: 'center', color: '#ff4d4d', border: '1px solid #ff4d4d33', marginBottom: '2rem' }}>
          <p>{error}</p>
        </div>
      )}

      <div style={{ display: 'grid', gap: '2rem' }}>
        {results.map((res, i) => (
          <div key={i} className="glass animate-fade-in" style={{ padding: '2rem', animationDelay: `${i * 0.1}s` }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
              <div>
                <h3 style={{ fontSize: '1.5rem', fontWeight: '700', marginBottom: '0.25rem' }}>{res.name}</h3>
                <p style={{ color: 'var(--text-muted)' }}>{Array.isArray(res.cuisines) ? res.cuisines.join(', ') : res.cuisines}</p>
              </div>
              <div style={{ background: 'rgba(226, 55, 68, 0.15)', color: 'var(--primary)', padding: '0.4rem 0.8rem', borderRadius: '0.75rem', fontWeight: '700' }}>
                ⭐ {res.rating.toFixed(1)}
              </div>
            </div>
            
            <div style={{ display: 'grid', gap: '0.75rem', padding: '1.25rem 0', borderTop: '1px solid var(--card-border)', borderBottom: '1px solid var(--card-border)', marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>📍 {res.location}</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>💰 ₹{res.cost_for_two} for two</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>👥 {res.votes} votes</div>
            </div>

            <div style={{ background: 'rgba(0, 0, 0, 0.2)', padding: '1.25rem', borderRadius: '0.75rem', borderLeft: '4px solid var(--primary)' }}>
              <strong style={{ color: 'var(--primary)', display: 'block', marginBottom: '0.5rem' }}>💡 AI Analysis</strong>
              <p style={{ color: '#cbd5e1', fontSize: '0.95rem', whiteSpace: 'pre-wrap' }}>{res.explanation}</p>
            </div>
          </div>
        ))}
      </div>
    </main>
  );
}




