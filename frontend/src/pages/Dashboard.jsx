// function Dashboard() {
//   const metrics = {
//     applicationsSent: 3,
//     dsaDone: 12,
//     followUpsDue: 2,
//   };

//   return (
//     <div>
//       <h1>Dashboard</h1>
//       <p>Track your job search and preparation progress.</p>

//       <div className="metrics-grid">
//         <div className="metric-card">
//           <h2>{metrics.applicationsSent}</h2>
//           <p>Applications Sent</p>
//         </div>

//         <div className="metric-card">
//           <h2>{metrics.dsaDone}</h2>
//           <p>DSA Problems Done</p>
//         </div>

//         <div className="metric-card">
//           <h2>{metrics.followUpsDue}</h2>
//           <p>Follow-ups Due</p>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default Dashboard;

// import { useEffect, useState } from "react";

// function Dashboard() {
//   const [metrics, setMetrics] = useState({
//     applicationsSent: 0,
//     dsaDone: 0,
//     followUpsDue: 0,
//   });

//   const [loading, setLoading] = useState(true);
//   const [errorMessage, setErrorMessage] = useState("");
//   const [dataSource, setDataSource] = useState("");

//   const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;
//   const ACCESS_TOKEN = import.meta.env.VITE_ACCESS_TOKEN;

//   useEffect(() => {
//     async function loadMetrics() {
//       setLoading(true);
//       setErrorMessage("");

//       try {
//         const response = await fetch(
//           `${API_BASE_URL}/dashboard/metrics?userId=user_123`,
//           {
//             headers: {
//               Authorization: `Bearer ${ACCESS_TOKEN}`,
//             },
//           }
//         );

//         const data = await response.json();

//         if (!response.ok) {
//           throw new Error(
//             data.error || data.message || "Unable to load dashboard metrics"
//           );
//         }

//         setMetrics(data.metrics);
//         setDataSource(data.source);
//       } catch (error) {
//         setErrorMessage(error.message);
//       } finally {
//         setLoading(false);
//       }
//     }

//     loadMetrics();
//   }, [API_BASE_URL, ACCESS_TOKEN]);

//   if (loading) {
//     return <p>Loading dashboard metrics...</p>;
//   }

//   return (
//     <div>
//       <h1>Dashboard</h1>
//       <p>Track your job search and preparation progress.</p>

//       {errorMessage && (
//         <p className="error-message">{errorMessage}</p>
//       )}

//       {!errorMessage && (
//         <>
//           <div className="metrics-grid">
//             <div className="metric-card">
//               <h2>{metrics.applicationsSent}</h2>
//               <p>Applications Sent</p>
//             </div>

//             <div className="metric-card">
//               <h2>{metrics.dsaDone}</h2>
//               <p>DSA Problems Done</p>
//             </div>

//             <div className="metric-card">
//               <h2>{metrics.followUpsDue}</h2>
//               <p>Follow-ups Due</p>
//             </div>
//           </div>

//           <p className="cache-source">
//             Data source: {dataSource}
//           </p>
//         </>
//       )}
//     </div>
//   );
// }

// export default Dashboard;

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