import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

// ============================================================
//  Test – verificación rápida de que todo responde
// Ejecutar: k6 run k6/smoke-test.js
// ============================================================

const errorRate = new Rate("errors");

const BASE_URL = __ENV.BASE_URL || "https://api.ciudadrobot.io";
const AI_URL = __ENV.AI_URL || "https://ai.ciudadrobot.io";

export const options = {
  vus: 3,
  duration: "1m",
  thresholds: {
    http_req_duration: ["p(99)<1500"],
    errors: ["rate<0.01"],
  },
};

export default function () {
  // Backend health
  let res = http.get(`${BASE_URL}/health`);
  check(res, { "backend healthy": (r) => r.status === 200 }) || errorRate.add(1);

  // AI Engine status
  res = http.get(`${AI_URL}/status`);
  check(res, { "ai-engine healthy": (r) => r.status === 200 }) || errorRate.add(1);

  // Robots
  res = http.get(`${BASE_URL}/api/robots`);
  check(res, { "robots ok": (r) => r.status === 200 }) || errorRate.add(1);

  // City
  res = http.get(`${BASE_URL}/api/city`);
  check(res, { "city ok": (r) => r.status === 200 }) || errorRate.add(1);

  sleep(1);
}
