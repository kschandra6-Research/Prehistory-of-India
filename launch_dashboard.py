"""
Prehistoric Archaeological GIS Dashboard Launcher
Indian Subcontinent Prehistoric Archaeological Sites (Paleolithic, Mesolithic, Neolithic)
"""

import http.server
import socketserver
import webbrowser
import os
import sys
import threading
import time

PORT = 8000
MAX_PORT_ATTEMPTS = 20

def find_open_port(start_port):
    import socket
    for port in range(start_port, start_port + MAX_PORT_ATTEMPTS):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            res = sock.connect_ex(('127.0.0.1', port))
            if res != 0: # Port is available
                return port
    return start_port

def run_server():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)

    port = find_open_port(PORT)
    url = f"http://localhost:{port}/index.html"

    handler = http.server.SimpleHTTPRequestHandler

    print("=" * 70)
    print(" PREHISTORIC ARCHAEOLOGICAL GIS & DATABASE DASHBOARD")
    print(" Indian Subcontinent: Paleolithic, Mesolithic, Neolithic")
    print(" Idea & Design by K.S.Chandra 2026 | kavikondalaschandra@gmail.com")
    print("=" * 70)
    print(f" Serving directory: {base_dir}")
    print(f" Opening web dashboard in default browser at: {url}")
    print("=" * 70)
    print(" Press Ctrl+C in this terminal window to stop the server.\n")

    # Open browser slightly after starting listener
    def open_browser():
        time.sleep(0.8)
        webbrowser.open(url)

    threading.Thread(target=open_browser, daemon=True).start()

    with socketserver.TCPServer(("", port), handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Prehistoric GIS Dashboard server. Goodbye!")
            httpd.shutdown()

if __name__ == "__main__":
    run_server()
