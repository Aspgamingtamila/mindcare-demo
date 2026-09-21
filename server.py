"""Local SQLite server for the MindCare demo.

Run `python server.py`, then visit http://localhost:8000 in a browser.
This is a development demo only: it has no authentication, encryption, or
production-grade health-data controls.
"""

from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import os
import sqlite3

ROOT = Path(__file__).resolve().parent
DATABASE = Path(os.environ.get("DATABASE_PATH", ROOT / "mindcare-demo.db"))


def connect():
    database = sqlite3.connect(DATABASE)
    database.execute("PRAGMA journal_mode = WAL")
    return database


def initialize_database():
    with connect() as database:
        database.executescript((ROOT / "schema.sql").read_text(encoding="utf-8"))


class MindCareHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/state":
            with connect() as database:
                row = database.execute("SELECT state_json FROM demo_state WHERE id = 1").fetchone()
            self.send_json(json.loads(row[0]) if row else {})
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/state":
            self.send_error(HTTPStatus.NOT_FOUND, "Unknown API route")
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length < 1 or content_length > 250_000:
                raise ValueError("Invalid request size")
            state = json.loads(self.rfile.read(content_length).decode("utf-8"))
            if not isinstance(state, dict) or not isinstance(state.get("people"), list):
                raise ValueError("State must include a people list")
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as error:
            self.send_json({"error": str(error)}, HTTPStatus.BAD_REQUEST)
            return
        encoded_state = json.dumps(state, ensure_ascii=False)
        with connect() as database:
            database.execute(
                "INSERT INTO demo_state (id, state_json, updated_at) VALUES (1, ?, CURRENT_TIMESTAMP) "
                "ON CONFLICT(id) DO UPDATE SET state_json = excluded.state_json, updated_at = CURRENT_TIMESTAMP",
                (encoded_state,),
            )
        self.send_json({"ok": True})


if __name__ == "__main__":
    initialize_database()
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), MindCareHandler)
    print(f"MindCare demo running on port {port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMindCare demo stopped.")
    finally:
        server.server_close()
