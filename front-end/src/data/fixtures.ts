import type {MetricSnapshot} from './types';

export const demoSnapshot: MetricSnapshot = {
    utilizationPct: 75,
    latencyMs: 12,
    packetLossPct: 2,
    throughputMbps: 100,
    status: 'degraded',
    observedAt: '2023-10-01T12:00:00Z'
};
export default demoSnapshot;