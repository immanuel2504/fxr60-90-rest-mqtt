#!/usr/bin/env python3
import argparse
import json
import socket
import sys
import time
import uuid


def encode_remaining_length(length):
    encoded = bytearray()
    while True:
        digit = length % 128
        length //= 128
        if length:
            digit |= 0x80
        encoded.append(digit)
        if not length:
            return bytes(encoded)


def encode_string(value):
    encoded = value.encode("utf-8")
    return len(encoded).to_bytes(2, "big") + encoded


def send_packet(connection, packet_type, payload):
    connection.sendall(bytes([packet_type]) + encode_remaining_length(len(payload)) + payload)


def receive_packet(connection):
    packet_type = connection.recv(1)
    if not packet_type:
        raise ConnectionError("MQTT broker closed the connection")
    multiplier = 1
    remaining_length = 0
    while True:
        digit = connection.recv(1)
        if not digit:
            raise ConnectionError("MQTT broker closed the connection")
        remaining_length += (digit[0] & 127) * multiplier
        if not digit[0] & 128:
            break
        multiplier *= 128
    payload = bytearray()
    while len(payload) < remaining_length:
        chunk = connection.recv(remaining_length - len(payload))
        if not chunk:
            raise ConnectionError("MQTT broker closed the connection")
        payload.extend(chunk)
    return packet_type[0] >> 4, bytes(payload)


def main():
    parser = argparse.ArgumentParser(
        description="Publish an optional management command and print MQTT responses/events."
    )
    parser.add_argument("--host", default="10.117.229.9")
    parser.add_argument("--port", type=int, default=1883)
    parser.add_argument("--command-topic", default="fxr60-lab/mcmd")
    parser.add_argument("--response-topic", default="fxr60-lab/mrsp")
    parser.add_argument("--event-topic", default="fxr60-lab/mevents")
    parser.add_argument(
        "--payload",
        help="Path to a JSON command payload. No command is published when omitted.",
    )
    parser.add_argument("--listen-seconds", type=int, default=30)
    args = parser.parse_args()

    payload = None
    if args.payload:
        try:
            with open(args.payload, encoding="utf-8") as payload_file:
                payload = json.load(payload_file)
        except (OSError, json.JSONDecodeError) as error:
            parser.error(f"cannot read JSON payload: {error}")

    client_id = f"pfx-test-{uuid.uuid4().hex[:12]}"
    connect_payload = b"\x00\x04MQTT\x04\x02\x00\x3c" + encode_string(client_id)
    subscriptions = b"\x00\x01" + b"".join(
        encode_string(topic) + b"\x00"
        for topic in (args.response_topic, args.event_topic)
    )

    connection = socket.create_connection((args.host, args.port), timeout=10)
    connection.settimeout(1)
    try:
        send_packet(connection, 0x10, connect_payload)
        packet_type, connection_response = receive_packet(connection)
        if packet_type != 2 or len(connection_response) != 2 or connection_response[1] != 0:
            raise ConnectionError(f"MQTT connection failed: {connection_response.hex()}")
        send_packet(connection, 0x82, subscriptions)
        packet_type, subscription_response = receive_packet(connection)
        if packet_type != 9 or subscription_response[:2] != b"\x00\x01":
            raise ConnectionError("MQTT subscription was rejected")
        print(f"subscribed to {args.response_topic} and {args.event_topic}")
        if payload is not None:
            publish_payload = encode_string(args.command_topic) + json.dumps(payload).encode("utf-8")
            send_packet(connection, 0x30, publish_payload)
            print(f"published to {args.command_topic}")

        deadline = time.monotonic() + args.listen_seconds
        while time.monotonic() < deadline:
            try:
                packet_type, message = receive_packet(connection)
            except socket.timeout:
                continue
            if packet_type == 3:
                topic_length = int.from_bytes(message[:2], "big")
                topic = message[2 : 2 + topic_length].decode("utf-8", "replace")
                body = message[2 + topic_length :].decode("utf-8", "replace")
                print(f"{topic}: {body}")
    finally:
        connection.close()


if __name__ == "__main__":
    main()