#!/usr/bin/env python3
"""Observe DIVA's Java-to-native access check in an authorized local lab."""

import time
import frida


def on_message(message, data):
    if message["type"] == "send":
        print(f"[+] {message['payload']}")
    else:
        print(f"[!] {message}")


device = frida.get_device("127.0.0.1:6555", timeout=5)
session = device.attach("Diva")
script = session.create_script(
    """
    Java.perform(function () {
        const DivaJni = Java.use('jakhar.aseem.diva.DivaJni');
        const access = DivaJni.access.overload('java.lang.String');
        access.implementation = function (candidate) {
            send('DivaJni.access candidate: ' + candidate);
            const result = access.call(this, candidate);
            send('DivaJni.access return value: ' + result);
            return result;
        };
        send('Hook loaded. Enter the native secret and tap the DIVA button.');
    });
    """
)
script.on("message", on_message)
script.load()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[*] Detaching.")
finally:
    script.unload()
    session.detach()

