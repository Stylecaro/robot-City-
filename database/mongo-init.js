// ============================================================
// Ciudad Robot – Políticas de MongoDB
// Ejecutar: mongosh < mongo-init.js
// ============================================================

// 1. Crear usuario de aplicación (privilegios mínimos)
db = db.getSiblingDB("admin");
db.createUser({
  user: "ciudad_app",
  pwd: "app_secure_password",
  roles: [
    { role: "readWrite", db: "ciudad_robot" },
  ],
});

db.createUser({
  user: "ciudad_readonly",
  pwd: "readonly_secure_password",
  roles: [
    { role: "read", db: "ciudad_robot" },
  ],
});

db.createUser({
  user: "ciudad_backup",
  pwd: "backup_secure_password",
  roles: [
    { role: "backup", db: "admin" },
    { role: "read", db: "ciudad_robot" },
  ],
});

// 2. Cambiar a la base de datos de la aplicación
db = db.getSiblingDB("ciudad_robot");

// ============================================================
// 3. Validación de esquemas (Schema Validation)
// ============================================================

db.createCollection("robots", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "name", "type", "status", "last_updated"],
      properties: {
        id: { bsonType: "string", description: "ID único del robot" },
        name: { bsonType: "string", minLength: 1, maxLength: 100 },
        type: {
          bsonType: "string",
          enum: ["worker", "security", "research", "maintenance", "combat", "medical"],
        },
        status: {
          bsonType: "string",
          enum: ["active", "idle", "maintenance", "offline", "destroyed"],
        },
        health: { bsonType: "double", minimum: 0, maximum: 100 },
        position: {
          bsonType: "object",
          properties: {
            x: { bsonType: "double" },
            y: { bsonType: "double" },
            z: { bsonType: "double" },
          },
        },
        last_updated: { bsonType: "date" },
      },
    },
  },
  validationLevel: "moderate",
  validationAction: "warn",
});

db.createCollection("decisions", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["decision_type", "timestamp", "result"],
      properties: {
        decision_type: { bsonType: "string" },
        timestamp: { bsonType: "date" },
        confidence: { bsonType: "double", minimum: 0, maximum: 1 },
        result: { bsonType: "object" },
        context: { bsonType: "object" },
      },
    },
  },
  validationLevel: "moderate",
  validationAction: "warn",
});

db.createCollection("city_metrics", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp"],
      properties: {
        timestamp: { bsonType: "date" },
        efficiency: { bsonType: "double", minimum: 0, maximum: 1 },
        population: { bsonType: "int" },
        energy_usage: { bsonType: "double" },
        security_level: { bsonType: "double", minimum: 0, maximum: 1 },
      },
    },
  },
  validationLevel: "moderate",
  validationAction: "warn",
});

db.createCollection("humanoids", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["id", "zone", "status"],
      properties: {
        id: { bsonType: "string" },
        zone: { bsonType: "string" },
        status: {
          bsonType: "string",
          enum: ["patrolling", "alert", "engaged", "standby", "offline"],
        },
      },
    },
  },
  validationLevel: "moderate",
  validationAction: "warn",
});

db.createCollection("incidents", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["type", "severity", "timestamp"],
      properties: {
        type: { bsonType: "string" },
        severity: {
          bsonType: "string",
          enum: ["low", "medium", "high", "critical"],
        },
        timestamp: { bsonType: "date" },
        resolved: { bsonType: "bool" },
      },
    },
  },
  validationLevel: "moderate",
  validationAction: "warn",
});

db.createCollection("optimizations", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["timestamp"],
      properties: {
        timestamp: { bsonType: "date" },
        score: { bsonType: "double", minimum: 0, maximum: 1 },
      },
    },
  },
  validationLevel: "moderate",
  validationAction: "warn",
});

// ============================================================
// 4. Índices para rendimiento
// ============================================================

// robots
db.robots.createIndex({ id: 1 }, { unique: true });
db.robots.createIndex({ type: 1, status: 1 });
db.robots.createIndex({ last_updated: -1 });
db.robots.createIndex({ "position.x": 1, "position.y": 1, "position.z": 1 });

// decisions
db.decisions.createIndex({ timestamp: -1 });
db.decisions.createIndex({ decision_type: 1, timestamp: -1 });

// city_metrics – TTL: borrar métricas > 90 días
db.city_metrics.createIndex(
  { timestamp: -1 },
  { expireAfterSeconds: 90 * 24 * 3600 }
);

// humanoids
db.humanoids.createIndex({ id: 1 }, { unique: true });
db.humanoids.createIndex({ zone: 1, status: 1 });

// incidents – TTL: borrar incidentes resueltos > 180 días
db.incidents.createIndex({ timestamp: -1 });
db.incidents.createIndex(
  { timestamp: 1, resolved: 1 },
  { expireAfterSeconds: 180 * 24 * 3600, partialFilterExpression: { resolved: true } }
);
db.incidents.createIndex({ severity: 1, timestamp: -1 });

// optimizations
db.optimizations.createIndex({ timestamp: -1 });

// ============================================================
// 5. Configuración de profiler (producción: solo queries lentas)
// ============================================================
db.setProfilingLevel(1, { slowms: 100 });

print("=== Políticas de MongoDB aplicadas correctamente ===");
