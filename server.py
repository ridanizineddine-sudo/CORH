from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json
import mimetypes
import sqlite3
import webbrowser
import os


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "corh_web.sqlite3"
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 8000))


def seed_data():
    return {
        "users": [
            {"username": "admin", "password": "admin123", "role": "responsable", "name": "Admin RH"},
            {"username": "sara", "password": "1234", "role": "employe", "employeId": 1, "name": "Sara Alami"},
        ],
        "employees": [
            {
                "id": 1,
                "nom": "Alami",
                "prenom": "Sara",
                "cin": "AB123456",
                "telephone": "0600000001",
                "email": "sara.alami@example.com",
                "poste": "Assistante RH",
                "categorie": "RH",
                "contrat": "CDI",
                "cnss": "",
            }
        ],
        "presences": [],
        "conges": [],
        "docRequests": [],
        "documents": [],
        "nextEmployeeId": 2,
        "nextLeaveId": 1,
        "nextDocRequestId": 1,
        "nextDocumentId": 1,
    }


def connect():
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "CREATE TABLE IF NOT EXISTS app_state (key TEXT PRIMARY KEY, value TEXT NOT NULL)"
    )
    return con


def load_state():
    with connect() as con:
        row = con.execute("SELECT value FROM app_state WHERE key = 'state'").fetchone()
        if row:
            return json.loads(row[0])
        state = seed_data()
        save_state(state)
        return state


def save_state(state):
    payload = json.dumps(state, ensure_ascii=False)
    with connect() as con:
        con.execute(
            "INSERT OR REPLACE INTO app_state (key, value) VALUES ('state', ?)",
            (payload,),
        )


class CoRHHandler(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path):
        if not path.exists() or not path.is_file():
            self.send_error(404, "Fichier introuvable")
            return
        body = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/state":
            self.send_json(200, load_state())
            return
        if self.path in ("/", "/index.html"):
            self.send_file(BASE_DIR / "index.html")
            return
        safe = self.path.split("?", 1)[0].lstrip("/").replace("\\", "/")
        requested = (BASE_DIR / safe).resolve()
        if BASE_DIR in requested.parents:
            self.send_file(requested)
            return
        self.send_error(403, "Chemin interdit")

    def do_POST(self):
        if self.path != "/api/state":
            self.send_error(404, "API inconnue")
            return
        length = int(self.headers.get("Content-Length", "0"))
        try:
            state = json.loads(self.rfile.read(length).decode("utf-8"))
            save_state(state)
            self.send_json(200, {"ok": True})
        except Exception as exc:
            self.send_json(400, {"ok": False, "error": str(exc)})

    def log_message(self, fmt, *args):
        print("%s - %s" % (self.address_string(), fmt % args))


def main():
    load_state()
    url = f"http://{HOST}:{PORT}"
    print("CoRH web avec backend Python")
    print(f"Ouvrir : {url}")
    # Sur Render, on ne peut pas ouvrir le navigateur automatiquement.
    if os.environ.get("RENDER") != "true":
        webbrowser.open(url)
    ThreadingHTTPServer((HOST, PORT), CoRHHandler).serve_forever()


if __name__ == "__main__":
    main()
