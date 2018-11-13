import socket
import threading
from scapy.all import *

firstIface = 'eth0'
firstIfaceFlows = ['52:54:00:42:84:65']
secondIface = 'eth1'
secondIfaceFlows = ['52:54:00:a1:54:c0']

def inOutServer():

    global firstIface
    global secondIface

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    inSocket.bind((firstIface, 0))

    outSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    outSocket.bind((secondIface, 0))

    while True:

        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in firstIfaceFlows:
                continue
        except:
            continue

        drop = False
        if IP in et:
            for opt in et[IP].options:
                if bytes(opt) == b'\x07\x03\x04':
                    drop = True
                    break

        if not drop:
            outSocket.send(bytes(et))

def outInServer():

    global firstIface
    global secondIface

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    inSocket.bind((secondIface, 0))

    outSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    outSocket.bind((firstIface, 0))

    while True:
        
        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in secondIfaceFlows:
                continue
        except:
            continue

        outSocket.send(bytes(et))

inOut = threading.Thread(target=inOutServer,args=())
outIn = threading.Thread(target=outInServer,args=())
outIn.start()
inOut.start()
inOut.join()
