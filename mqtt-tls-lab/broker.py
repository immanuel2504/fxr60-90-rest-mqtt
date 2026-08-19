#!/usr/bin/env python3
"""Minimal MQTT 3.1.1 broker over TLS with mutual authentication.

Dependency-free (stdlib only) so the lab runs without pip. It implements what a
reader-to-broker test needs and nothing more:

  CONNECT/CONNACK, SUBSCRIBE/SUBACK, UNSUBSCRIBE/UNSUBACK,
  PUBLISH (QoS 0 and 1, with PUBACK), retained messages,
  PINGREQ/PINGRESP, DISCONNECT, topic wildcards + and #

Not implemented: QoS 2, will messages, persistent sessions, username/password
auth (client identity comes from the TLS certificate instead).

  py -3 broker.py                     # 0.0.0.0:8883, client cert required
  py -3 broker.py --host 127.0.0.1    # local only
  py -3 broker.py --allow-anonymous   # no client cert — mimics verifyPeer:false

Every client must present a certificate signed by certs/ca.crt, and the CN of
that certificate is logged on connect. Stop with Ctrl+C.
"""

from __future__ import annotations

import argparse
import os
import socket
import ssl
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
CERTS = os.path.join(HERE, "certs")

CONNECT, CONNACK, PUBLISH, PUBACK = 1, 2, 3, 4
SUBSCRIBE, SUBACK, UNSUBSCRIBE, UNSUBACK = 8, 9, 10, 11
PINGREQ, PINGRESP, DISCONNECT = 12, 13, 14

NAMES = {1: "CONNECT", 2: "CONNACK", 3: "PUBLISH", 4: "PUBACK", 8: "SUBSCRIBE",
         9: "SUBACK", 10: "UNSUBSCRIBE", 11: "UNSUBACK", 12: "PINGREQ",
         13: "PINGRESP", 14: "DISCONNECT"}


def log(*parts: object) -> None:
    print(f"[{time.strftime('%H:%M:%S')}]", *parts, flush=True)


# --------------------------------------------------------------------------
# wire format helpers
# --------------------------------------------------------------------------
def recv_exact(sock: ssl.SSLSocket, count: int) -> bytes:
    buf = b""
    while len(buf) < count:
        chunk = sock.recv(count - len(buf))
        if not chunk:
            raise ConnectionError("peer closed")
        buf += chunk
    return buf


def recv_remaining_length(sock: ssl.SSLSocket) -> int:
    value, shift = 0, 0
    while True:
        byte = recv_exact(sock, 1)[0]
        value |= (byte & 0x7F) << shift
        if not byte & 0x80:
            return value
        shift += 7
        if shift > 21:
            raise ValueError("malformed remaining length")


def encode_remaining_length(value: int) -> bytes:
    out = bytearray()
    while True:
        byte = value % 128
        value //= 128
        if value:
            byte |= 0x80
        out.append(byte)
        if not value:
            return bytes(out)


def take_string(data: bytes, offset: int) -> tuple[str, int]:
    length = int.from_bytes(data[offset:offset + 2], "big")
    start = offset + 2
    return data[start:start + length].decode("utf-8", "replace"), start + length


def encode_string(text: str) -> bytes:
    raw = text.encode("utf-8")
    return len(raw).to_bytes(2, "big") + raw


def topic_matches(filt: str, topic: str) -> bool:
    """MQTT 3.1.1 wildcard rules: + one level, # remainder."""
    if filt == topic:
        return True
    fparts, tparts = filt.split("/"), topic.split("/")
    for i, fp in enumerate(fparts):
        if fp == "#":
            return i == len(fparts) - 1
        if i >= len(tparts):
            return False
        if fp != "+" and fp != tparts[i]:
            return False
    return len(fparts) == len(tparts)


# --------------------------------------------------------------------------
class Client:
    def __init__(self, sock: ssl.SSLSocket, addr, cn: str):
        self.sock = sock
        self.addr = addr
        self.cn = cn
        self.client_id = "?"
        self.subs: dict[str, int] = {}
        self.lock = threading.Lock()
        self._packet_id = 0

    def next_packet_id(self) -> int:
        self._packet_id = self._packet_id % 65535 + 1
        return self._packet_id

    def send(self, packet: bytes) -> None:
        with self.lock:
            self.sock.sendall(packet)

    def __str__(self) -> str:
        return f"{self.client_id} ({self.cn} @ {self.addr[0]}:{self.addr[1]})"


class Broker:
    def __init__(self, verbose: bool):
        self.clients: set[Client] = set()
        self.retained: dict[str, tuple[bytes, int]] = {}
        self.lock = threading.Lock()
        self.verbose = verbose
        self.published = 0
        self.delivered = 0

    # -- publish path ----------------------------------------------------
    def publish(self, topic: str, payload: bytes, qos: int, retain: bool) -> int:
        if retain:
            with self.lock:
                if payload:
                    self.retained[topic] = (payload, qos)
                else:
                    self.retained.pop(topic, None)  # empty payload clears
        with self.lock:
            targets = [(c, sub_qos) for c in self.clients
                       for filt, sub_qos in c.subs.items()
                       if topic_matches(filt, topic)]
        sent = 0
        for client, sub_qos in targets:
            try:
                client.send(build_publish(topic, payload, min(qos, sub_qos),
                                         client.next_packet_id()))
                sent += 1
            except OSError:
                pass
        self.published += 1
        self.delivered += sent
        return sent

    def add(self, client: Client) -> None:
        with self.lock:
            self.clients.add(client)

    def remove(self, client: Client) -> None:
        with self.lock:
            self.clients.discard(client)

    def send_retained(self, client: Client, filt: str, sub_qos: int) -> None:
        with self.lock:
            matches = [(t, p, q) for t, (p, q) in self.retained.items()
                       if topic_matches(filt, t)]
        for topic, payload, qos in matches:
            try:
                client.send(build_publish(topic, payload, min(qos, sub_qos),
                                          client.next_packet_id(), retain=True))
            except OSError:
                pass


def build_publish(topic: str, payload: bytes, qos: int, packet_id: int,
                  retain: bool = False) -> bytes:
    body = encode_string(topic)
    if qos > 0:
        body += packet_id.to_bytes(2, "big")
    body += payload
    flags = (qos << 1) | (1 if retain else 0)
    return bytes([(PUBLISH << 4) | flags]) + encode_remaining_length(len(body)) + body


# --------------------------------------------------------------------------
def handle_client(broker: Broker, sock: ssl.SSLSocket, addr) -> None:
    cn = "anonymous"
    cert = sock.getpeercert()
    if cert:
        for field in cert.get("subject", ()):
            for key, value in field:
                if key == "commonName":
                    cn = value

    client = Client(sock, addr, cn)
    connected = False
    try:
        while True:
            header = recv_exact(sock, 1)[0]
            ptype, flags = header >> 4, header & 0x0F
            length = recv_remaining_length(sock)
            body = recv_exact(sock, length) if length else b""

            if broker.verbose and ptype != PUBLISH:
                log(f"  <- {NAMES.get(ptype, ptype)} from {client}")

            if ptype == CONNECT:
                offset = 0
                _proto, offset = take_string(body, offset)
                level = body[offset]             # 4 = MQTT 3.1.1, 5 = MQTT 5.0
                offset += 1
                if level >= 5:
                    # FXR readers try MQTT 5.0 first and fall back to 3.1.1.
                    # Answer with a proper v5 CONNACK carrying reason code 0x84
                    # (unsupported protocol version) so the fallback is immediate
                    # instead of waiting for a timeout.
                    client.send(bytes([CONNACK << 4, 3, 0x00, 0x84, 0x00]))
                    log(f"CONNECT   protocol level {level} (MQTT 5.0) from "
                        f"{addr[0]} — replying 'unsupported protocol version'; "
                        f"the client should retry with 3.1.1")
                    break
                connect_flags = body[offset]
                offset += 1
                offset += 2                      # keep-alive
                client.client_id, offset = take_string(body, offset)
                if connect_flags & 0x04:         # will
                    _wt, offset = take_string(body, offset)
                    wl = int.from_bytes(body[offset:offset + 2], "big")
                    offset += 2 + wl
                if connect_flags & 0x80:
                    _user, offset = take_string(body, offset)
                if connect_flags & 0x40:
                    _pwd, offset = take_string(body, offset)
                broker.add(client)
                connected = True
                client.send(bytes([CONNACK << 4, 2, 0, 0]))
                log(f"CONNECT   {client}")

            elif ptype == SUBSCRIBE:
                packet_id = int.from_bytes(body[0:2], "big")
                offset, codes, filters = 2, bytearray(), []
                while offset < len(body):
                    filt, offset = take_string(body, offset)
                    qos = body[offset] & 0x03
                    offset += 1
                    client.subs[filt] = qos
                    filters.append((filt, qos))
                    codes.append(qos)
                ack = packet_id.to_bytes(2, "big") + bytes(codes)
                client.send(bytes([SUBACK << 4]) +
                            encode_remaining_length(len(ack)) + ack)
                for filt, qos in filters:
                    log(f"SUBSCRIBE {client} -> {filt} (qos {qos})")
                    broker.send_retained(client, filt, qos)

            elif ptype == UNSUBSCRIBE:
                packet_id = int.from_bytes(body[0:2], "big")
                offset = 2
                while offset < len(body):
                    filt, offset = take_string(body, offset)
                    client.subs.pop(filt, None)
                    log(f"UNSUB     {client} -> {filt}")
                ack = packet_id.to_bytes(2, "big")
                client.send(bytes([UNSUBACK << 4]) +
                            encode_remaining_length(len(ack)) + ack)

            elif ptype == PUBLISH:
                qos, retain = (flags >> 1) & 0x03, bool(flags & 0x01)
                topic, offset = take_string(body, 0)
                packet_id = None
                if qos > 0:
                    packet_id = int.from_bytes(body[offset:offset + 2], "big")
                    offset += 2
                payload = body[offset:]
                if qos == 1 and packet_id is not None:
                    ack = packet_id.to_bytes(2, "big")
                    client.send(bytes([PUBACK << 4]) +
                                encode_remaining_length(len(ack)) + ack)
                sent = broker.publish(topic, payload, qos, retain)
                preview = payload.decode("utf-8", "replace")
                if len(preview) > 100:
                    preview = preview[:100] + f"... ({len(payload)} bytes)"
                log(f"PUBLISH   {client} -> {topic} qos{qos}"
                    f"{' retain' if retain else ''} -> {sent} subscriber(s): {preview}")

            elif ptype == PUBACK:
                pass  # delivery is fire-and-forget; nothing to retry

            elif ptype == PINGREQ:
                client.send(bytes([PINGRESP << 4, 0]))

            elif ptype == DISCONNECT:
                log(f"DISCONNECT {client}")
                break

            else:
                log(f"ignoring unsupported packet type {ptype} from {client}")

    except ssl.SSLError as exc:
        # With TLS 1.3 the server completes its side of the handshake before the
        # client certificate arrives, so a missing or untrusted client cert
        # surfaces here on the first read rather than at wrap_socket().
        reason = getattr(exc, "reason", None) or exc
        log(f"TLS REJECT {addr[0]}:{addr[1]}: {reason}")
    except (ConnectionError, OSError, ValueError, IndexError) as exc:
        if connected:
            log(f"DROPPED   {client}: {type(exc).__name__}: {exc}")
        else:
            log(f"REJECTED  {addr[0]}:{addr[1]} before CONNECT: "
                f"{type(exc).__name__}: {exc}")
    finally:
        broker.remove(client)
        try:
            sock.close()
        except OSError:
            pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--host", default="0.0.0.0",
                    help="bind address (default 0.0.0.0 so the reader can reach it)")
    ap.add_argument("--port", type=int, default=8883)
    ap.add_argument("--certs", default=CERTS)
    ap.add_argument("--allow-anonymous", action="store_true",
                    help="do not require a client certificate (verifyPeer:false case)")
    ap.add_argument("--no-tls", action="store_true",
                    help="plain MQTT, no TLS (use port 1883). Isolates network "
                         "reachability from certificate problems — nothing is "
                         "encrypted, so lab use only")
    ap.add_argument("-v", "--verbose", action="store_true",
                    help="log control packets too, not just publishes")
    args = ap.parse_args()

    server_crt = os.path.join(args.certs, "server.crt")
    server_key = os.path.join(args.certs, "server.key")
    ca_crt = os.path.join(args.certs, "ca.crt")
    context = None
    if not args.no_tls:
        for path in (server_crt, server_key, ca_crt):
            if not os.path.isfile(path):
                sys.exit(f"missing {path} — run: py -3 gen_certs.py")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(server_crt, server_key)
        context.load_verify_locations(ca_crt)
        context.verify_mode = (ssl.CERT_NONE if args.allow_anonymous
                               else ssl.CERT_REQUIRED)

    broker = Broker(args.verbose)
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
        # Windows: SO_REUSEADDR would let a second broker bind the same port and
        # silently steal connections. Fail fast instead.
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
    else:
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        listener.bind((args.host, args.port))
    except OSError as exc:
        sys.exit(f"cannot bind {args.host}:{args.port} — {exc}\n"
                 f"Another broker is probably still running.")
    listener.listen(16)

    if context is None:
        log(f"MQTT broker (PLAIN, no TLS) on {args.host}:{args.port}")
        log("  nothing is encrypted — reachability testing only")
    else:
        log(f"MQTT TLS broker on {args.host}:{args.port}")
        log(f"  server cert : {server_crt}")
        log(f"  trusted CA  : {ca_crt}")
        log(f"  client cert : {'optional' if args.allow_anonymous else 'REQUIRED'}")
    log("Ctrl+C to stop")

    try:
        while True:
            raw, addr = listener.accept()
            if context is None:
                log(f"TCP CONN  {addr[0]}:{addr[1]}")
                sock = raw
            else:
                try:
                    sock = context.wrap_socket(raw, server_side=True)
                except (ssl.SSLError, OSError) as exc:
                    reason = getattr(exc, "reason", None) or exc
                    log(f"TLS REJECT {addr[0]}:{addr[1]}: {reason}")
                    raw.close()
                    continue
            threading.Thread(target=handle_client, args=(broker, sock, addr),
                             daemon=True).start()
    except KeyboardInterrupt:
        log(f"stopping — {broker.published} publish(es), "
            f"{broker.delivered} delivery(ies)")
    finally:
        listener.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
