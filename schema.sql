-- MindCare demo: SQLite persistence for the local prototype.
-- This is intentionally a local development database, not a production health-data design.
CREATE TABLE IF NOT EXISTS demo_state (
  id INTEGER PRIMARY KEY CHECK (id = 1),
  state_json TEXT NOT NULL,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
