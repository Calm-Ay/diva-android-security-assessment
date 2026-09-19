#!/usr/bin/env python3
import frida

device = frida.get_device("127.0.0.1:6555", timeout=5)
session = device.attach("Diva")
script = session.create_script("send('attached')")
script.load()
print("Frida 16 attach and script load succeeded.")
script.unload()
session.detach()

