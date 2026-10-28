import './App.css';
import StatusCard from './components/StatusCards';
import type { ConnectionMode } from './data/types';
import type { Health } from './data/types';
import DeviceList from './components/DeviceList';
import {
  fixtureSnapshot,
  fixtureDevices,
  fixtureAccessPoints,
  demoConnectionMode,
} from './data/fixtures';

function formatConnectionMode(mode: ConnectionMode){
  const result=mode.split('-').map(word=> word.charAt(0).toUpperCase()+word.slice(1)).join(' ');
  return result;
}
function formatHealth(status: Health){
  return status.charAt(0).toUpperCase()+status.slice(1);
}


function App() {
  const totalDevices=fixtureDevices.length;
  const healthyDevices=fixtureDevices.filter((device)=>device.health==='healthy').length;
  const healthyAPs=fixtureAccessPoints.filter((ap)=>ap.health==='healthy').length;
  const activeAlerts: number=2;
  const recoveryState="No Recovery";
  return (
    <main>
      {/* اسم المشروع وحالةالشبكة */}
      <header>
        <div>
          <p className="dashboard-top-title">DIGITAL TWIN · NETWORK MONITORING</p>
          <h1 className="dashboard-title">Network Dashboard</h1>
          <p className="dashboard-description">Real-time network health and performance</p>
          <p className="last-updated">Last updated: {new Date(fixtureSnapshot.observedAt).toLocaleString("en-US",{month:"short",
                                                                                      day:"numeric", 
                                                                                      year:"numeric",
                                                                                      hour:"numeric",
                                                                                      minute:"numeric",
                                                                                      hour12:true
                            })}
          </p>
        </div>
        <div className="header-status">
        {/*------------------------ Connection Mode--------------------------- */}
         <div className="connection-mode">
          {formatConnectionMode(demoConnectionMode)}
            <span>Simulated data</span>
        </div>
                            {/*------------------------ Network Status--------------------------- */}
        <div className="network-status" role="status">
          <span className={`status-${fixtureSnapshot.status }`} aria-hidden='true'>●</span> 
          <span className={`status-${fixtureSnapshot.status}`}>{formatHealth(fixtureSnapshot.status)}</span>
        </div>
       </div>
      </header>


       {/* قسم الكارد */}
      <section>
        <h2 className="metrics-section-title">Network Overview</h2>
        <div className="metrics-container">
         <StatusCard
          label="Latency" 
          value={fixtureSnapshot.latencyMs}
           unit="ms"
           />
           <StatusCard
            label="Utilization"
            value={fixtureSnapshot.utilizationPct}
            unit="%"
           />
            <StatusCard
             label="Packet Loss"
             value={fixtureSnapshot.packetLossPct}
             unit="%"
            />
            <StatusCard
             label="Throughput"
             value={fixtureSnapshot.throughputMbps}
             unit="Mbps"
            />
            <StatusCard
            label='Total Devices' 
            value={totalDevices}
            unit={totalDevices===1?"Device":"Devices"}/>
            <StatusCard 
            label="Healthy Devices"
            value={healthyDevices}
            unit={healthyDevices===1?"Device":"Devices"}/>
            <StatusCard
            label="Healthy APs"
            value={`${healthyAPs}/${fixtureAccessPoints.length}`}
            unit={healthyAPs==1?"AP":"APs"}/>
            <StatusCard
            label="Active Alerts"
            value={activeAlerts}
            unit={activeAlerts===1?"Alert":"Alerts"}/>
            <StatusCard
            label="Recovery State"
            value={recoveryState}
            unit=""/>
        </div>
      </section>
      <DeviceList devices={fixtureDevices}/>
    </main>
  );
}

export default App;