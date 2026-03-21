import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

// ============================================================
// Test de estrés extremo – busca el punto de rotura
// Ejecutar: k6 run k6/stress-test.js
// ============================================================

const errorRate = new Rate("errors");

const BASE_URL = __ENV.BASE_URL || "https://api.ciudadrobot.io";
const AI_URL = __ENV.AI_URL || "https://ai.ciudadrobot.io";

export const options = {
  stages: [
    { duration: "2m", target: 100 },
    { duration: "5m", target: 100 },
    { duration: "2m", target: 300 },
    { duration: "5m", target: 300 },
    { duration: "2m", target: 500 },
    { duration: "5m", target: 500 },
    { duration: "2m", target: 800 },
    { duration: "5m", target: 800 },
    { duration: "5m", target: 0 },
  ],
  thresholds: {
    http_req_duration: ["p(95)<5000"],
    errors: ["rate<0.3"],
  },
};

export default function () {
  const endpoints = [
    { url: `${BASE_URL}/health`, name: "health" },
    { url: `${BASE_URL}/api/robots`, name: "robots" },
    { url: `${BASE_URL}/api/city`, name: "city" },
    { url: `${AI_URL}/status`, name: "ai-status" },
    { url: `${AI_URL}/robots`, name: "ai-robots" },
  ];

  const ep = endpoints[Math.floor(Math.random() * endpoints.length)];
  const res = http.get(ep.url, { tags: { name: ep.name } });

  const ok = check(res, {
    "status < 500": (r) => r.status < 500,
    "duration < 5s": (r) => r.timings.duration < 5000,
  });

  if (!ok) errorRate.add(1);

  sleep(0.3);
}
