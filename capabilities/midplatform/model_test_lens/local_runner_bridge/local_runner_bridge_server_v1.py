# -*- coding: utf-8 -*-
"""Local Runner Bridge HTTP server v1 — localhost only."""

from __future__ import annotations

import argparse
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Optional

from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_api_handlers_v1 import (
    handle_request,
    try_serve_local_file,
)
from capabilities.midplatform.model_test_lens.local_runner_bridge.local_runner_bridge_skeleton_execution_types_v1 import (
    BIND_HOST,
    BIND_PORT,
    SERVICE_NAME,
)


def validate_bind_host(host: str) -> str:
    normalized = host.strip().lower()
    if normalized not in ("127.0.0.1", "localhost"):
        raise SystemExit(
            f"REFUSED: Local Runner Bridge must bind 127.0.0.1 or localhost only, got {host!r}"
        )
    return "127.0.0.1"


class LocalRunnerBridgeHandler(BaseHTTPRequestHandler):
    server_version = f"{SERVICE_NAME}/1.0"

    def log_message(self, fmt: str, *args) -> None:
        sys.stderr.write("%s - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), fmt % args))

    def _send(self, code: int, data: dict, extra_headers: dict) -> None:
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        for k, v in extra_headers.items():
            self.send_header(k, v)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if code != 204:
            self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        code, data, headers = handle_request("OPTIONS", self.path, body, self.headers.get("Origin"))
        self._send(code, data, headers)

    def do_GET(self) -> None:
        file_resp = try_serve_local_file(self.path, self.headers.get("Origin"))
        if file_resp is not None:
            code, body, _ctype, headers = file_resp
            self.send_response(code)
            for k, v in headers.items():
                self.send_header(k, v)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        code, data, headers = handle_request("GET", self.path, b"", self.headers.get("Origin"))
        self._send(code, data, headers)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        code, data, headers = handle_request("POST", self.path, body, self.headers.get("Origin"))
        self._send(code, data, headers)


def serve(host: str = BIND_HOST, port: int = BIND_PORT) -> None:
    bind = validate_bind_host(host)
    server = ThreadingHTTPServer((bind, port), LocalRunnerBridgeHandler)
    print(f"Local Runner Bridge listening on http://{bind}:{port} (localhost-only, not runtime)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down Local Runner Bridge.")
        server.server_close()


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description="Model Test Lens Local Runner Bridge (localhost only)")
    parser.add_argument("--host", default=BIND_HOST)
    parser.add_argument("--port", type=int, default=BIND_PORT)
    args = parser.parse_args(argv)
    serve(args.host, args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
