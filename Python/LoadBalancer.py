import socket
import threading
from scapy.all import *

standardIface = 'eth0'
firstIfaceFlows = ['52:54:00:42:84:65']
serverPaths = ['eth1', 'eth2']
serverPathsFlows = [['52:54:00:a1:54:c0'], ['52:54:00:a1:54:c0']]

def inOutServer():

    global standardIface
    global serverPaths

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    inSocket.bind((standardIface, 0))

    serverSockets = []
    serverQuantity = len(serverPaths)

    for path in serverPaths:
    	sSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    	sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    	sSocket.bind((path, 0))
    	serverSockets.append(sSocket)

    while True:

        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in firstIfaceFlows:
                continue
        except:
            continue

        if IP in et:
        	serverSockets[int((et[IP].src).split('.')[-1])%serverQuantity].send(bytes(et))
        else:
        	serverSockets[0].send(bytes(et))

def outInServer(inIface, inIfaceFlows):

    global standardIface

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    inSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    inSocket.bind((inIface, 0))

    outSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    outSocket.bind((standardIface, 0))

    while True:
        
        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in inIfaceFlows:
                continue
        except:
            continue

        outSocket.send(bytes(et))


outInSockets = []
inOut = threading.Thread(target=inOutServer,args=())
for index in range(len(serverPaths)):
    outIn = threading.Thread(target=outInServer,args=(serverPaths[index], serverPathsFlows[index]))
    outIn.start()
    outInSockets.append(outIn)
inOut.start()
inOut.join()
