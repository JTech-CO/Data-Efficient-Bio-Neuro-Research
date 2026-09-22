"""Local-only development server. No uploads, arbitrary code, shell, or real assays.

CSRF token, same-origin/Host checks and a single-run lock protect the bounded
synthetic execution endpoint. This is not an authenticated production server.
"""
from __future__ import annotations
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import secrets
import threading
from .runner import RunConfig, run_experiment, save_run, audit_run

ROOT = Path(__file__).resolve().parents[2]

class LabServer(ThreadingHTTPServer):
    daemon_threads = True
    def __init__(self, port: int):
        self.token = secrets.token_urlsafe(32)
        self.execution_lock = threading.Lock()
        super().__init__(("127.0.0.1", port), LabHandler)

class LabHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def end_headers(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        super().end_headers()

    def valid_host(self) -> bool:
        port = self.server.server_address[1]
        return self.headers.get("Host") in (f"127.0.0.1:{port}", f"localhost:{port}")

    def json_response(self, status: int, value: dict):
        data = json.dumps(value, ensure_ascii=False, allow_nan=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def allowed_static(self) -> bool:
        path = unquote(urlsplit(self.path).path).lstrip("/")
        if not path:
            return True
        if ".." in Path(path).parts or "\\" in path or any(part.startswith(".") for part in Path(path).parts):
            return False
        return path == "index.html" or path in ("README.md", "README.en.md") or path.startswith(("lab/", "docs/", "references/", "research/docs/", "research/results/", "research/quality/"))

    def do_GET(self):
        if not self.valid_host():
            return self.json_response(403, {"error": "Invalid Host"})
        if urlsplit(self.path).path == "/api/health":
            return self.json_response(200, {"mode": "synthetic-local-runner", "version": "1.1.0", "csrf_token": self.server.token})
        if not self.allowed_static():
            return self.json_response(404, {"error": "Not available"})
        super().do_GET()

    def do_HEAD(self):
        if not self.valid_host() or not self.allowed_static():
            self.send_error(404)
            return
        super().do_HEAD()

    def list_directory(self, path):
        self.send_error(403, "Directory listing disabled")
        return None

    def do_POST(self):
        if urlsplit(self.path).path != "/api/run":
            return self.json_response(404, {"error": "Unknown endpoint"})
        origin = self.headers.get("Origin")
        if not self.valid_host() or origin != f"http://{self.headers.get('Host')}" or not secrets.compare_digest(self.headers.get("X-Lab-Token", ""), self.server.token):
            return self.json_response(403, {"error": "Same-origin request and session token required"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 1 <= length <= 4096 or self.headers.get("Content-Type", "").split(";")[0] != "application/json":
                return self.json_response(400, {"error": "Expected bounded application/json request"})
            payload = json.loads(self.rfile.read(length))
            config = RunConfig(**payload)
        except (ValueError, TypeError, KeyError, json.JSONDecodeError):
            return self.json_response(400, {"error": "Invalid experiment configuration"})
        if not self.server.execution_lock.acquire(blocking=False):
            return self.json_response(409, {"error": "One experiment is already running in this local server"})
        try:
            result = run_experiment(config)
            save_run(result, ROOT / "research/results/local" / (result["run_id"] + ".json"))
            self.json_response(200, {"run": result, "audit": audit_run(result)})
        except Exception as exc:
            self.log_error("Synthetic execution error: %s", exc)
            self.json_response(500, {"error": "Synthetic run failed; inspect local terminal"})
        finally:
            self.server.execution_lock.release()


def serve(port: int = 8765):
    if not 1024 <= port <= 65535:
        raise ValueError("port must be between 1024 and 65535")
    server = LabServer(port)
    print(f"Closed-loop research lab: http://127.0.0.1:{port}\nLocal synthetic execution only. Press Ctrl+C to stop.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
