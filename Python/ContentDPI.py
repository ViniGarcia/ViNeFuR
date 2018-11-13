import socket
import threading
import codecs
from scapy.all import *

contentTable = ['porn', 'guns', 'torrent', 'skype', '/status/']

firstIface = 'eth0'
firstIfaceFlows = ['52:54:00:42:84:65']
secondIface = 'eth1'
secondIfaceFlows = ['52:54:00:a1:54:c0']

def inOutServer():
    
    global contentTable
    global firstIface
    global secondIface

    inSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
    inSocket.bind((firstIface, 0))

    outSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW)
    outSocket.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1514)
    outSocket.bind((secondIface, 0))

    for index in range(len(contentTable)):
        contentTable[index] = contentTable[index].encode()

    while True:

        pkt = inSocket.recvfrom(1514)
        try:
            et = Ether(bytes(pkt[0]))
            if not et.src in firstIfaceFlows:
                continue 
        except:
            continue

        if TCP in et:
            if et[IP][TCP].dport == 80:
                data = bytes(et[IP][TCP].payload)
                
                for content in contentTable:
                    if not content in data:
                        continue

                    del et[IP].ihl
                    del et[IP].len
                    del et[IP].chksum
                    et[IP].options = IPOption_RR()
                    et.show2(dump=True)
                    break
            
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
