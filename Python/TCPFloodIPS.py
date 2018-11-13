import socket
import time
import threading
from scapy.all import *

COUNTERS = {}
THRESH = 10000
TIME = 0               

firstIface = 'eth0'
firstIfaceFlows = ['52:54:00:42:84:65']
secondIface = 'eth1'
secondIfaceFlows = ['52:54:00:a1:54:c0']

def TCPFloodDetection(packet):

    global COUNTERS
    global THRESH
    global TIME
    
    currentTime = time.time()
    if currentTime - TIME > 1:
        COUNTERS = {}
        TIME = currentTime

    if packet.haslayer(TCP):
        stream = packet[IP].src + ':' + packet[IP].dst

        if stream in COUNTERS:
            COUNTERS[stream] += 1
        else:
            COUNTERS[stream] = 1

        for stream in COUNTERS:
            if COUNTERS[stream] > THRESH:
                return True

        return False

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

        if IP in et:
            if TCPFloodDetection(et):
                continue
                
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
