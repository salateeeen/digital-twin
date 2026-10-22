import './App.css';
/*Array Of Object For DataCards */
const metrics=[{label:'Devices',value:3,unit:'Connected'},
               {label:'Access Points',value:4,unit:'Active'},     
               {label:'Utilization',value:18,unit:'%'},
               {label:'Latency',value:34,unit:'ms'},
               {label:'Packet Loss',value:12,unit:'%'},
               {label:'Throughput',value:123,unit:'Mbps'},
               
]
function App() {
  return (
    <main>
      {/* اسم المشروع وحالةالشبكة */}
      <header>
        <div>
          <p className="dashboard-top-title">DIGITAL TWIN · NETWORK MONITORING</p>
          <h1 className="dashboard-title">Network Dashboard</h1>
          <p className="dashboard-description">Real-time network health and performance</p>
        </div>
        <div className="network-status">
          <span className="status-dot">●</span> 
          Healthy
        </div>
      </header>


       {/* قسم الكارد */}
      <section>
        <h2 className="metrics-section-title">Network Overview</h2>
        <div className="metrics-container">
          {metrics.map((metric) => (
            <div key={metric.label} className="metric-card">
              <h3>{metric.label}</h3>
              <p>{metric.value}<span>{metric.unit}</span></p>
            </div>
          ))}
        </div>
      </section>
    </main>
  );
}

export default App;