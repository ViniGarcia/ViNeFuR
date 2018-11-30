import socket
import threading
from scapy.all import *

signatureTable = [(71, (70, b'\x90\xf6')), (None, (60, b'\x07\x03\x04')), (346, (54, b'\xf9\xa0\xba\xa8\x81\x8d\xdc'))]

firstIface = 'eth0'
firstIfaceFlows = ['52:54:00:00:00:65']
secondIface = 'eth1'
secondIfaceFlows = ['52:54:00:a1:54:c0']

def inOutServer():

    global signatureTable
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

        if TCP in et:

            if et[IP][TCP].dport == 443:

                for signature in signatureTable:

                    if signature[0] != None:
                        if len(et[IP][TCP]) != signature[0]:
                            continue

                    if signature[1] != None:
                        if len(et[IP][TCP]) < (signature[1][0] + len(signature[1][1])):
                            continue

                        if len(signature[1][1]) > 1:
                            if bytes(et[IP][TCP])[signature[1][0]-1:(signature[1][0] - 1 + len(signature[1][1]))] != signature[1][1]:
                                continue
                        else:
                            if bytes(et[IP][TCP])[signature[1][0]-1] != signature[1][1][0]:
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
