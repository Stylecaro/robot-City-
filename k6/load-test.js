import http from "k6/http";
import ws from "k6/ws";
import { check, sleep, group } from "k6";
import { Rate, Trend, Counter } from "k6/metrics";

// ============================================================
// Ciudad Robot – Test de carga k6 contra cluster K8s
// Ejecutar: k6 run --out json=results.json k6/load-test.js
// ============================================================

// Métricas personalizadas
const errorRate = new Rate("errors");
const robotCreationTime = new Trend("robot_creation_time", true);
const aiStatusTime = new Trend("ai_status_time", true);
const wsMessages = new Counter("ws_messages_sent");

// Configuración – ajustar BASE_URL al ingress real o puerto
const BASE_URL = __ENV.BASE_URL || "https://api.ciudadrobot.io";
const AI_URL = __ENV.AI_URL || "https://ai.ciudadrobot.io";
const WS_URL = __ENV.WS_URL || "wss://api.ciudadrobot.io";

// ============================================================
// Escenarios de carga
// ============================================================
export const options = {
  scenarios: {
    // Carga continua normal
    constant_load: {
      executor: "constant-vus",
      vus: 50,
      duration: "5m",
      exec: "apiTests",
    },
    // Rampa progresiva
    ramp_up: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "2m", target: 100 },
        { duration: "5m", target: 100 },
        { duration: "2m", target: 200 },
        { duration: "5m", target: 200 },
        { duration: "2m", target: 0 },
      ],
      exec: "apiTests",
      startTime: "6m",
    },
    // Picos de estrés
    spike: {
      executor: "ramping-vus",
      startVUs: 0,
      stages: [
        { duration: "30s", target: 500 },
        { duration: "1m", target: 500 },
        { duration: "30s", target: 0 },
      ],
      exec: "apiTests",
      startTime: "22m",
    },
    // WebSocket
    websocket_load: {
      executor: "constant-vus",
      vus: 30,
      duration: "10m",
      exec: "wsTest",
      startTime: "2m",
    },
    // Carga AI Engine
    ai_engine_load: {
      executor: "ramping-arrival-rate",
      startRate: 10,
      timeUnit: "1s",
      preAllocatedVUs: 50,
      maxVUs: 200,
      stages: [
        { duration: "2m", target: 50 },
        { duration: "3m", target: 50 },
        { duration: "1m", target: 0 },
      ],
      exec: "aiEngineTests",
      startTime: "6m",
    },
  },
  thresholds: {
    http_req_duration: ["p(95)<2000", "p(99)<5000"],
    http_req_failed: ["rate<0.05"],
    errors: ["rate<0.1"],
    robot_creation_time: ["p(95)<3000"],
    ai_status_time: ["p(95)<1000"],
  },
};

// ============================================================
// Tests de API REST
// ============================================================
export function apiTests() {
  group("Health Check", () => {
    const res = http.get(`${BASE_URL}/health`);
    check(res, {
      "health status 200": (r) => r.status === 200,
      "health body OK": (r) => {
        try {
          return JSON.parse(r.body).status === "OK";
        } catch {
          return false;
        }
      },
    }) || errorRate.add(1);
  });

  group("API Info", () => {
    const res = http.get(`${BASE_URL}/api`);
    check(res, {
      "api info 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("List Robots", () => {
    const res = http.get(`${BASE_URL}/api/robots`);
    check(res, {
      "robots status 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("City Data", () => {
    const res = http.get(`${BASE_URL}/api/city`);
    check(res, {
      "city status 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("Security Status", () => {
    const res = http.get(`${BASE_URL}/api/security`);
    check(res, {
      "security status 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  sleep(1);
}

// ============================================================
// Tests del AI Engine
// ============================================================
export function aiEngineTests() {
  group("AI Status", () => {
    const start = Date.now();
    const res = http.get(`${AI_URL}/status`);
    aiStatusTime.add(Date.now() - start);
    check(res, {
      "ai status 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("List Robots (AI)", () => {
    const res = http.get(`${AI_URL}/robots`);
    check(res, {
      "ai robots 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("Create Robot", () => {
    const payload = JSON.stringify({
      name: `k6-bot-${__VU}-${__ITER}`,
      type: "worker",
      capabilities: ["patrol", "scan"],
    });
    const params = { headers: { "Content-Type": "application/json" } };
    const start = Date.now();
    const res = http.post(`${AI_URL}/robots/create`, payload, params);
    robotCreationTime.add(Date.now() - start);
    check(res, {
      "create robot 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("City Optimization", () => {
    const res = http.get(`${AI_URL}/city/optimization`);
    check(res, {
      "city opt 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  group("Quantum Nodes", () => {
    const res = http.get(`${AI_URL}/quantum/nodes`);
    check(res, {
      "quantum nodes 200": (r) => r.status === 200,
    }) || errorRate.add(1);
  });

  sleep(0.5);
}

// ============================================================
// Test WebSocket
// ============================================================
export function wsTest() {
  const url = `${WS_URL}/socket.io/?EIO=4&transport=websocket`;

  const res = ws.connect(url, {}, function (socket) {
    socket.on("open", () => {
      socket.send(JSON.stringify({ type: "get_robots", data: {} }));
      wsMessages.add(1);
    });

    socket.on("message", (data) => {
      // Recibir respuestas
    });

    // Enviar mensajes periódicos
    for (let i = 0; i < 10; i++) {
      socket.setTimeout(function () {
        socket.send(
          JSON.stringify({
            type: "get_robots",
            data: {},
          })
        );
        wsMessages.add(1);
      }, (i + 1) * 2000);
    }

    // Cerrar tras ~22 segundos
    socket.setTimeout(function () {
      socket.close();
    }, 22000);
  });

  check(res, {
    "ws status 101": (r) => r && r.status === 101,
  }) || errorRate.add(1);
}

// ============================================================
// Informe
// ============================================================
export function handleSummary(data) {
  const summary = {
    timestamp: new Date().toISOString(),
    scenarios: Object.keys(options.scenarios),
    metrics: {
      http_req_duration_p95:
        data.metrics?.http_req_duration?.values?.["p(95)"] || "N/A",
      http_req_duration_p99:
        data.metrics?.http_req_duration?.values?.["p(99)"] || "N/A",
      http_req_failed_rate:
        data.metrics?.http_req_failed?.values?.rate || "N/A",
      error_rate: data.metrics?.errors?.values?.rate || "N/A",
      total_requests:
        data.metrics?.http_reqs?.values?.count || "N/A",
      vus_max: data.metrics?.vus_max?.values?.value || "N/A",
    },
  };

  return {
    "k6/results-summary.json": JSON.stringify(summary, null, 2),
    stdout: `\n=== Ciudad Robot Load Test Summary ===
Total Requests: ${summary.metrics.total_requests}
P95 Latency:    ${summary.metrics.http_req_duration_p95}ms
P99 Latency:    ${summary.metrics.http_req_duration_p99}ms
Error Rate:     ${summary.metrics.error_rate}
Max VUs:        ${summary.metrics.vus_max}
======================================\n`,
  };
}
