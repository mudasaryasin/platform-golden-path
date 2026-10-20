"""Small stateless reference service; no third-party runtime dependencies."""
import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        routes = {"/": {"service": "golden-path", "version": "0.1.0"},
                  "/healthz": {"status": "ok"}, "/readyz": {"status": "ready"}}
        status = 200 if self.path in routes else 404
        payload = json.dumps(routes.get(self.path, {"error": "not found"})).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format, *args):
        # Avoid logging request URLs which may contain sensitive query parameters.
        print(json.dumps({"event": "http_request", "method": self.command}), flush=True)

def main():
    ThreadingHTTPServer(("0.0.0.0", int(os.environ.get("PORT", "8080"))), Handler).serve_forever()

if __name__ == "__main__":
    main()
