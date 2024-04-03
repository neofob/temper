#!/usr/bin/env python3

import argparse
from flask import Flask, json

import temper

def update_usb_devices(t):
    try:
        t.usb_devices = temper.USBList().get_usb_devices()
    except Exception as e:
        print(f"Error updating USB devices: {e}")

parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", default="0.0.0.0", help="host to bind to, default: 0.0.0.0")
parser.add_argument("-p", "--port", type=int, default=2610, help="port to listen to, default: 2610")
parser.add_argument("-d", "--debug", action='store_true', help="debug mode, default: False")
args = parser.parse_args()

app = Flask("temper")
t = temper.Temper()

available_endpoints = {
    "/list": lambda: json.dumps(t.usb_devices, indent=2, sort_keys=True),
    "/metrics": lambda: json.dumps(t.read(), indent=2)
}

print(f"Available endpoints:")
for endpoint, _ in available_endpoints.items():
    print(f"{endpoint} = list available USB devices or return available metrics from temper USB devices")

@app.route('/<path:path>')
def endpoint(path):
    if path in available_endpoints:
        update_usb_devices(t)
        return available_endpoints[path]()
    else:
        return "Not Found", 404

if __name__ == '__main__':
    app.run(host=args.host, port=args.port, debug=args.debug)
