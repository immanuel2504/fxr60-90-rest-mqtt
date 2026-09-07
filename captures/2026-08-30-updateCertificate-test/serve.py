import http.server
import ssl
import datetime

PORT = 443


class LoggingHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        ts = datetime.datetime.now().isoformat()
        print(f"\n=== Request at {ts} from {self.client_address[0]} ===")
        print(f"Path: {self.path}")
        for name, value in self.headers.items():
            print(f"  {name}: {value}")
        auth = self.headers.get("Authorization")
        if auth:
            print(f"--> Authorization header received: {auth}")
        else:
            print("--> No Authorization header received")
        print("=" * 50)
        super().do_GET()


httpd = http.server.HTTPServer(("0.0.0.0", PORT), LoggingHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on 0.0.0.0:{PORT}  (Ctrl+C to stop)")
print("File will be reachable at: https://192.168.1.41/certificates/sample.pfx")
print("Every request's headers (including Authorization) will be printed below.")
httpd.serve_forever()
