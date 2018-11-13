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
    global firstIfaceFlows

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
            print('eth0 -> ' + str(et.src))
        except:
            continue

        if IP in et:        
            del et[IP].chksum
            et.show2(dump=True)
        outSocket.send(bytes(et))        

def outInServer():

    global firstIface
    global secondIface
    global secondIfaceFlows

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
            print('eth1 -> ' + str(et.src))
        except:
            continue
        
        if IP in et:
            del et[IP].chksum
            et.show2(dump=True)
        outSocket.send(bytes(et))

inOut = threading.Thread(target=inOutServer,args=())
outIn = threading.Thread(target=outInServer,args=())
outIn.start()
inOut.start()
inOut.join()
outIn.join()
