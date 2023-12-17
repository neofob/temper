#!/usr/bin/env python3

import argparse
from flask import Flask, json

import temper

usblist = temper.USBList()

def update_usb_devices(t):

    try:
        t.usb_devices = usb_list.get_usb_devices()
    except Exception as e:
        print(f"Error updating USB devices: {e}")

# parsing config
parser = argparse.ArgumentParser()
parser.add_argument("-H", "--host", default="0.0.0.0", help="host to bind to, default: 0.0.0.0")
parser.add_argument("-p", "--port", type=int, default=2610, help="port to listen to, default: 2610")
parser.add_argument("-d", "--debug", action='store_true', help="debug mode, default: False")
args = parser.parse_args()

app = Flask("temper")
t = temper.Temper()

print(f"Available endpoints:")
print(f"/list = list available USB devices")
print(f"/metrics = return availale metrics from temper USB devices")

@app.route('/list')
def list():
    update_usb_devices(t)
    return json.dumps(t.usb_devices, indent=2, sort_keys=True)

@app.route('/metrics')
def metrics():
    update_usb_devices(t)
    return json.dumps(t.read(), indent=2)

if __name__ == '__main__':
    app.run(host=args.host, port=args.port, debug=args.debug)
