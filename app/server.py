"""Servidor HTTP simples para o MVP de busca de vagas."""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from app.data_sources import fetch_jobs

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


class JobsHandler(BaseHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_file(self, file_path: Path, content_type: str = "text/html; charset=utf-8") -> None:
        if not file_path.exists():
            self.send_error(HTTPStatus.NOT_FOUND, "Arquivo não encontrado")
            return
        data = file_path.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)

        if parsed.path == "/":
            return self._serve_file(STATIC_DIR / "index.html")

        if parsed.path == "/static/styles.css":
            return self._serve_file(STATIC_DIR / "styles.css", "text/css; charset=utf-8")

        if parsed.path == "/static/app.js":
            return self._serve_file(STATIC_DIR / "app.js", "application/javascript; charset=utf-8")

        if parsed.path == "/api/vagas":
            params = parse_qs(parsed.query)
            localidade = params.get("localidade", [None])[0]
            area = params.get("area", [None])[0]

            jobs = fetch_jobs(localidade=localidade)
            if area:
                jobs = [job for job in jobs if job.area_especifica.lower() == area.lower()]

            return self._send_json({"total": len(jobs), "vagas": [job.to_dict() for job in jobs]})

        self.send_error(HTTPStatus.NOT_FOUND, "Rota não encontrada")


def run(host: str = "0.0.0.0", port: int = 8000) -> None:
    server = ThreadingHTTPServer((host, port), JobsHandler)
    print(f"Servidor disponível em http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
