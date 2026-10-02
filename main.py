"""
Neuroutin — точка входа .exe.
Поднимает локальный HTTP-сервер для frontend и открывает окно pywebview.
Локальный сервер нужен, чтобы localStorage в WebView2 работал корректно.
"""
import sys
import threading
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial
from pathlib import Path

import webview


def get_frontend_dir() -> Path:
    # В .exe frontend лежит во временной папке _MEIPASS
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS) / "frontend"
    return Path(__file__).parent / "frontend"


def find_free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def run_server(directory: Path, port: int) -> None:
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    httpd = HTTPServer(("127.0.0.1", port), handler)
    httpd.serve_forever()


def main() -> None:
    frontend = get_frontend_dir()
    port = find_free_port()

    # Сервер в фоновом потоке
    t = threading.Thread(target=run_server, args=(frontend, port), daemon=True)
    t.start()

    webview.create_window(
        "Neuroutin",
        f"http://127.0.0.1:{port}/index.html",
        width=1280,
        height=800,
        min_size=(900, 600),
    )
    webview.start()


if __name__ == "__main__":
    main()