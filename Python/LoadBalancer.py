import socket
import threading
from scapy.all import *

firstIface = 'eth0'
firstIfaceFlows = ['52:54:00:42:84:65']
secondIface = 'eth1'
secondIfaceFlows = ['52:54:00:a1:54:c0']
thirdIface = 'eth2'
thirdIfaceFlows = ['52:54:00:d3:a3:df']

def inOutServer():

    global firstIface
    global secondIface
    global thirdIface
    global firstIfaceFlows

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    inSocket.bind((firstIface, 0))

    outSocket01 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    outSocket01.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    outSocket01.bind((secondIface, 0))

    outSocket02 = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    outSocket02.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    outSocket02.bind((thirdIface, 0))

    while True:

        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in firstIfaceFlows:
                continue 
        except:
            continue
        
        if int(bytes(et.src[-1].encode('utf-8'))[0]) % 2 == 0:
            outSocket01.send(bytes(et))
        else:
            outSocket02.send(bytes(et))        

def outInServer(iface, ifaceFlows):

    global firstIface

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    inSocket.bind((iface, 0))

    outSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    outSocket.bind((firstIface, 0))

    while True:
        
        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in ifaceFlows:
                continue
        except:
            continue
        
        outSocket.send(bytes(et))

inOut = threading.Thread(target=inOutServer,args=())
outIn01 = threading.Thread(target=outInServer,args=(secondIface, secondIfaceFlows))
outIn02 = threading.Thread(target=outInServer,args=(thirdIface, thirdIfaceFlows))
outIn02.start()
outIn01.start()
inOut.start()
inOut.join()
outIn01.join()
outIn02.join()
