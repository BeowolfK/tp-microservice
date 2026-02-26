import json


def publish_event(pub_socket, event: str, data: dict):
    payload = json.dumps(data)
    pub_socket.send_string(f"{event} {payload}")
