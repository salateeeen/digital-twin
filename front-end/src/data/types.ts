export type Health = 'healthy' | 'degraded' | 'failed' | 'unknown';
export type ConnectionMode='demo'|'live'|'polling'|'offline';
export interface MetricSnapshot {
   schemaVersion: '1.0';     /*إصدار صيغة البيانات. */
    runId: string;       /*معرّف تشغيل التجربة. */
    entityId: string;        /*معرّف العنصر الذي تصفه البيانات */
    entityType: string;      /*نوع العنصر */
    observedAt: string;    
    status: Health;
    utilizationPct: number | null;
    latencyMs: number | null;
    packetLossPct: number | null;
    throughputMbps: number | null;
    source: string; /*مصدر البيانات وهو fixture بهاي الحاله */
    sequence: number; /*رقم تسلسلي للبيانات */
}

export interface Device {
    id: string;
    label: string;
    floorId: string;
    kind: 'client' | 'switch' | 'controller';
    health: Health;
}

export interface AccessPoint{
  id: string;
  label: string;
  floorId: string;
  health: Health;
  clients: number; /* #Devices who connected to the APs */
  utilizationPct: number | null; /*Usage %e*/
}
export interface DevicesResponse {
    schemaVersion: '1.0';
    observedAt: string;
    devices: Device[];
}

export interface Floor{
id:string;  /* اي دي للطابق  */
label:string;   /*الاسم الي رح يظهر بالداش بورد  */
} 