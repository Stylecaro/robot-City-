FROM node:20-alpine AS builder
WORKDIR /app
COPY backend/package.json backend/package-lock.json* ./
RUN npm ci --omit=dev

FROM node:20-alpine
RUN apk add --no-cache curl tini
WORKDIR /app
COPY --from=builder /app/node_modules ./node_modules
COPY backend/ ./
ENV NODE_ENV=production
EXPOSE 8000
USER node
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["node", "server.js"]
