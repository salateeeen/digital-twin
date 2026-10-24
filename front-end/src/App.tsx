import './App.css';
import StatusCard from './components/StatusCards';
import demoSnapshot from './data/fixtures';

/*Array Of Object For DataCards */
function App() {
  return (
    <main>
      {/* اسم المشروع وحالةالشبكة */}
      <header>
        <div>
          <p className="dashboard-top-title">DIGITAL TWIN · NETWORK MONITORING</p>
          <h1 className="dashboard-title">Network Dashboard</h1>
          <p className="dashboard-description">Real-time network health and performance</p>
          <p>Last updated: {new Date(demoSnapshot.observedAt).toLocaleString("en-US",{month:"short",
                                                                                      day:"numeric", 
                                                                                      year:"numeric",
                                                                                      hour:"numeric",
                                                                                      minute:"numeric",
                                                                                      hour12:true
                            })}
          </p>
        </div>
        <div className="network-status" role="status">
          <span className={`status-${demoSnapshot.status }`}>●</span> 
          <span className={`status-${demoSnapshot.status}`}>{demoSnapshot.status.charAt(0).toUpperCase() + demoSnapshot.status.slice(1)}</span>
        </div>
      </header>


       {/* قسم الكارد */}
      <section>
        <h2 className="metrics-section-title">Network Overview</h2>
        <div className="metrics-container">
         <StatusCard
          label="Latency" 
          value={demoSnapshot.latencyMs}
           unit="ms"
           />
           <StatusCard
            label="Utilization"
            value={demoSnapshot.utilizationPct}
            unit="%"
           />
            <StatusCard
             label="Packet Loss"
             value={demoSnapshot.packetLossPct}
             unit="%"
            />
            <StatusCard
             label="Throughput"
             value={demoSnapshot.throughputMbps}
             unit="Mbps"
            />

        </div>
      </section>
    </main>
  );
}

export default App;