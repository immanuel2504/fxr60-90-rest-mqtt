import http.server
import ssl

PORT = 8443

httpd = http.server.HTTPServer(("0.0.0.0", PORT), http.server.SimpleHTTPRequestHandler)
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.load_cert_chain(certfile="server-cert.pem", keyfile="server-key.pem")
httpd.socket = ctx.wrap_socket(httpd.socket, server_side=True)

print(f"Serving HTTPS on 0.0.0.0:{PORT}  (Ctrl+C to stop)")
print("File will be reachable at: https://192.168.1.41:8443/certificates/sample.pfx")
httpd.serve_forever()
