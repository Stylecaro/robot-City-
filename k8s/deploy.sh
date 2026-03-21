#!/bin/bash
# ============================================================
# Ciudad Robot – Deploy to Kubernetes
# ============================================================
set -euo pipefail

NAMESPACE="ciudad-robot"
REGISTRY="${REGISTRY:-ciudad-robot}"

echo "=== 1. Construyendo imágenes Docker ==="
docker build -t "${REGISTRY}/backend:latest" -f backend/Dockerfile .
docker build -t "${REGISTRY}/ai-engine:latest" -f ai-engine/Dockerfile .
docker build -t "${REGISTRY}/frontend:latest" -f frontend/Dockerfile .

echo "=== 2. Aplicando manifiestos K8s ==="
kubectl apply -f k8s/base/namespace.yml
kubectl apply -f k8s/base/secrets.yml
kubectl apply -f k8s/base/configmap.yml
kubectl apply -f k8s/base/network-policies.yml
kubectl apply -f k8s/base/mongodb.yml
kubectl apply -f k8s/base/redis.yml

echo "Esperando a que MongoDB y Redis estén listos..."
kubectl -n "${NAMESPACE}" rollout status statefulset/mongodb --timeout=120s
kubectl -n "${NAMESPACE}" rollout status deployment/redis --timeout=60s

kubectl apply -f k8s/base/backend.yml
kubectl apply -f k8s/base/ai-engine.yml
kubectl apply -f k8s/base/frontend.yml
kubectl apply -f k8s/base/monitoring.yml
kubectl apply -f k8s/base/cert-manager.yml
kubectl apply -f k8s/base/ingress.yml

echo "=== 3. Esperando despliegues ==="
kubectl -n "${NAMESPACE}" rollout status deployment/backend --timeout=120s
kubectl -n "${NAMESPACE}" rollout status deployment/ai-engine --timeout=180s
kubectl -n "${NAMESPACE}" rollout status deployment/frontend --timeout=60s

echo ""
echo "=== Despliegue completado ==="
kubectl -n "${NAMESPACE}" get pods
kubectl -n "${NAMESPACE}" get svc
kubectl -n "${NAMESPACE}" get ingress
