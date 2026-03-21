const { Registry, Counter, Histogram, Gauge, collectDefaultMetrics } = require('prom-client');

const register = new Registry();

collectDefaultMetrics({ register });

// --- Contadores ---
const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total de peticiones HTTP recibidas',
  labelNames: ['method', 'route', 'status_code'],
  registers: [register],
});

const wsConnectionsTotal = new Counter({
  name: 'ws_connections_total',
  help: 'Total de conexiones WebSocket establecidas',
  registers: [register],
});

const wsMessagesTotal = new Counter({
  name: 'ws_messages_total',
  help: 'Total de mensajes WebSocket procesados',
  labelNames: ['event'],
  registers: [register],
});

// --- Histogramas ---
const httpRequestDuration = new Histogram({
  name: 'http_request_duration_seconds',
  help: 'Duración de peticiones HTTP en segundos',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [register],
});

// --- Gauges ---
const wsActiveConnections = new Gauge({
  name: 'ws_active_connections',
  help: 'Conexiones WebSocket activas actualmente',
  registers: [register],
});

const robotsActive = new Gauge({
  name: 'robots_active',
  help: 'Robots activos en la ciudad',
  registers: [register],
});

const cityEfficiency = new Gauge({
  name: 'city_efficiency',
  help: 'Eficiencia actual de la ciudad (0-1)',
  registers: [register],
});

// Middleware para medir peticiones HTTP
function metricsMiddleware(req, res, next) {
  const start = process.hrtime.bigint();

  res.on('finish', () => {
    const durationNs = Number(process.hrtime.bigint() - start);
    const durationSec = durationNs / 1e9;
    const route = req.route?.path || req.path;
    const labels = {
      method: req.method,
      route,
      status_code: res.statusCode,
    };
    httpRequestsTotal.inc(labels);
    httpRequestDuration.observe(labels, durationSec);
  });

  next();
}

module.exports = {
  register,
  metricsMiddleware,
  httpRequestsTotal,
  httpRequestDuration,
  wsConnectionsTotal,
  wsMessagesTotal,
  wsActiveConnections,
  robotsActive,
  cityEfficiency,
};
