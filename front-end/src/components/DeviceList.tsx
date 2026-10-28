import type{ Device } from "../data/types";


type DeviceListProps={
    devices:Device[];
};

function formatDeviceHealth(health: Device['health']){
  return health.charAt(0).toUpperCase()+health.slice(1);
}

function DeviceList({ devices }: DeviceListProps) {
    return (
        <section className="device-list">
            <h2>Devices</h2>
            <ul>
                {devices.map((device) => (
                    <li key={device.id}>
                        <strong>{device.label}</strong>
                        <span> — Type: {device.kind}</span>
                        <span className={`status-${device.health}`}>{' — Health: '}{formatDeviceHealth(device.health)}</span>
                    </li>
                ))}
            </ul>
        </section>
    );
}

export default DeviceList
