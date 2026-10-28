import type {MetricSnapshot,ConnectionMode,Device,AccessPoint,Floor} from './types';
export const fixtureSnapshot: MetricSnapshot = {
  schemaVersion: '1.0',
  runId: 'fixture-run-001',
  entityId: 'network',
  entityType: 'network',
  observedAt: '2026-01-12T10:00:00Z',
  status: 'healthy',
  utilizationPct: 18,
  latencyMs: 4,
  packetLossPct: 0,
  throughputMbps: 120,
  source: 'fixture',
  sequence: 1,
};
export const demoConnectionMode: ConnectionMode = 'offline';

export const fixtureDevices:Device[]=[

   {    id: 'client-1',
        label: 'Client 1',
        floorId: 'floor-1',
        kind: 'client',
        health: 'healthy'} ,

   {    id: 'ap-2',
        label: 'AP-2',
        floorId: 'floor-2',
        kind: 'switch',
        health: 'degraded'},

   {    id: 'ryu-1',
        label: 'Ryu controller',
        floorId: 'floor-1',
        kind: 'controller',
        health: 'failed'},
     
        
]
export const fixtureAccessPoints: AccessPoint[]=[
      {
    id: 'ap-1',
    label: 'AP-1',
    floorId: 'floor-1',
    health: 'healthy',
    clients: 5,
    utilizationPct: 30
               },
      {
    id: 'ap-2',
    label: 'AP-2',
    floorId: 'floor-2',
    health: 'healthy',
    clients: 8,
    utilizationPct: 65
                },
     {
    id: 'ap-3',
    label: 'AP-3',
    floorId: 'floor-3',
    health: 'unknown',
    clients: 0,
    utilizationPct: null
                }
]
    
export const fixtureFloors: Floor[]=[

    { id: 'floor-1', label: 'Floor 1' },
    { id: 'floor-2', label: 'Floor 2' },
    { id: 'floor-3', label: 'Floor 3' }

]

export default fixtureSnapshot;