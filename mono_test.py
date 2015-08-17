import serial
from time import sleep


def read_hi_lo(cm):
    raw = []
    sleep(0.01)
    for j in range(cm.inWaiting()):
        raw += cm.read()
    data = int(hex(raw[0]) + hex(raw[1]).replace('0x', ''), 16)
    status = int(hex(raw[2]))
    message = int(hex(raw[3]))
    return data, status, message


cm = serial.Serial("COM1")
properties = ["Position:",
              "Type:",
              "Grooves/mm:",
              "Blaze:",
              "Grating No:",
              "Speed:",
              "Size:",
              "No. of Gratings:",
              "Current Units:",
              "Serial No."]
q_bytes = [0]  # list(range(7)) + [13, 14, 19]
i = 0

cm.write(chr(16).encode())
high, low = divmod(5500, 0x100)
sleep(0.1)
cm.write(chr(high).encode())
sleep(0.1)
cm.write(chr(low).encode())
sleep(0.1)
for q in q_bytes:

    cm.write(chr(56).encode())
    sleep(0.1)
    cm.write(chr(q).encode())
    raw = []

    sleep(0.01)
    for j in range(cm.inWaiting()):
        raw += cm.read()
    data = int(hex(raw[0]) + hex(raw[1]).replace('0x', ''), 16)
    print(raw, properties[i], data)
    i += 1

# print("Currently at {0} nm".format(data/10))
cm.close()
