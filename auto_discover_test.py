import visa
import serial
from serial.tools import list_ports
from time import sleep


def visa_discovery():
    queries = ['ID?', 'ID', '*IDN?']
    names = ['MODEL331S',
             'MODEL 2440',
             '34970A',
             '5302',
             'KI4200',
             'HP6634A']
    rm = visa.ResourceManager()
    instr_address = [i for i in rm.list_resources() if "ASRL" not in i]
    sessions = [rm.open_resource(i) for i in instr_address]
    instrs = {}
    for s in sessions:
        s.clear()
    for q in queries:
        for s in sessions:
            s.write(q)
    for s in sessions:
        try:
            reply = s.read()
            for name in names:
                if name in reply:
                    instrs[name] = (
                        "GPIB0::{0}::INSTR".format(s.primary_address))
        except:
            print("failed to read from {0}".format(s))
        s.close()
    return instrs


def com_discovery():
    com_ports = list(list_ports.comports())
    sessions = [serial.Serial(c[0]) for c in com_ports]
    sleep(2)
    replies = ['Shutter', chr(27), 'q']
    instrs = {chr(27): "Monochromator", "Shutter": "Shutter", "q": "5320 LIA"}
    devices = {}
    for s in sessions:
        try:
            s.flush()
            s.write(b'q')
            s.write(chr(27).encode())
            sleep(0.1)
            num_bytes = s.inWaiting()
            if num_bytes == 0:
                continue
            else:
                reply = s.read(num_bytes).decode()
            for r in replies:
                if r in reply:
                    devices[instrs[r]] = s.port
        except:
            print("failed to read from {0}".format(s))
        s.close()
    return devices


for name, key in com_discovery().items():
    print(name, key)
for name, key in visa_discovery().items():
    print(name, "at", key)
