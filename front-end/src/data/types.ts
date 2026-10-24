export type Health = 'healthy' | 'degraded' | 'failed' | 'unknown';
export interface MetricSnapshot {
    utilizationPct: number;
    latencyMs: number;
    packetLossPct: number;
    throughputMbps: number;
    status: Health;
    observedAt: string;
}