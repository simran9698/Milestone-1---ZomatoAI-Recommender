export default function Home() {
  const streamlitUrl = process.env.NEXT_PUBLIC_STREAMLIT_APP_URL;

  if (!streamlitUrl) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100vh', fontFamily: 'sans-serif', backgroundColor: '#0e1117', color: '#fafafa' }}>
        <h1 style={{ color: '#ff4b4b' }}>Configuration Missing</h1>
        <p>Please set the <code>NEXT_PUBLIC_STREAMLIT_APP_URL</code> environment variable.</p>
      </div>
    );
  }

  return (
    <div style={{ margin: 0, padding: 0, height: '100vh', overflow: 'hidden', backgroundColor: '#0e1117' }}>
      <iframe
        src={streamlitUrl}
        style={{ width: '100%', height: '100%', border: 'none' }}
        title="Zomato AI Recommender"
        allow="geolocation; microphone; camera"
      />
    </div>
  );
}

