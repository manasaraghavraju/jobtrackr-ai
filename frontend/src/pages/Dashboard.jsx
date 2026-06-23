function Dashboard() {
  const metrics = {
    applicationsSent: 3,
    dsaDone: 12,
    followUpsDue: 2,
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Track your job search and preparation progress.</p>

      <div className="metrics-grid">
        <div className="metric-card">
          <h2>{metrics.applicationsSent}</h2>
          <p>Applications Sent</p>
        </div>

        <div className="metric-card">
          <h2>{metrics.dsaDone}</h2>
          <p>DSA Problems Done</p>
        </div>

        <div className="metric-card">
          <h2>{metrics.followUpsDue}</h2>
          <p>Follow-ups Due</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;