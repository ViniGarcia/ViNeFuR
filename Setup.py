import sys
from subprocess import call


def environmentConfigure():

	call(['apt-get', 'install', 'bridge-utils'])
	call(['apt-get', 'install', 'ethtool'])

	call(['apt-get', 'install', 'gcc'])
	call(['apt-get', 'install', 'g++'])
	call(['apt-get', 'install', 'python3'])
	call(['apt-get', 'install', 'python3-pip'])
	call(['pip3', 'install', 'scapy'])
	call(['pip3', 'install', 'bottle'])
	call(['apt-get', 'install', 'git'])
	call(['git', 'clone', 'https://github.com/kohler/click.git'])
	call(['./click/configure', '--disable-linuxmodule', '--enable-ip6'])
	call(['click/userlevel/make'])
	call(['click/userlevel/make', 'install'])
	call(['rm', '-r', 'click'])

	call(['apt-get', 'install', 'curl'])
	call(['apt-get', 'install', 'iperf'])
        call(['apt-get', 'install', 'httperf'])
	call(['apt-get', 'install', 'd-itg'])


def baseConfigure(bridgesQuantity):

	for bridge in range(bridgesQuantity):
		bridgeID = 'br' + str(bridge)
		call(['brctl', 'addbr', bridgeID])
		call(['ifconfig', bridgeID, 'up'])
		call(['ethtool', '-K', bridgeID, 'rx', 'off', 'tx', 'off', 'sg', 'off', 'tso', 'off', 'ufo', 'off', 'gso', 'off', 'gro', 'off', 'lro', 'off'])


def nfvVMConfigure(ifacesQuantity):

	for iface in range(ifacesQuantity):
		ifaceID = 'eth' + str(iface)
		call(['ifconfig', ifaceID, 'up'])
		call(['ethtool', '-K', ifaceID, 'rx', 'off', 'tx', 'off', 'sg', 'off', 'tso', 'off', 'ufo', 'off', 'gso', 'off', 'gro', 'off', 'lro', 'off'])


def generalVMConfigure(ifacesQuantity, baseNetwork, ipBegin):

	for iface in range(ifacesQuantity):
		ifaceID = 'eth' + str(iface)
		ifaceIP = baseNetwork + '.' + str(ipBegin)
		call(['ifconfig', ifaceID, ifaceIP, 'up'])
		call(['ethtool', '-K', ifaceID, 'rx', 'off', 'tx', 'off', 'sg', 'off', 'tso', 'off', 'ufo', 'off', 'gso', 'off', 'gro', 'off', 'lro', 'off'])

		ipBegin += 1
	
def downloadRepository():

	call(['git', 'clone', 'https://github.com/ViniGarcia/ViNeFuR.git'])


def help():
	print('--')
	print('-ec -> Environment Configure')
	print('-bc bridgesQuantity -> Base Configure')
	print('-nvc ifacesQuantity -> NFV VM Configure')
	print('-gvc ifacesQuantity baseNetwork ipBegin -> General VM Configure')
	print('-dr -> Download Repository')
	print('--')

if len(sys.argv) > 1:
	
	if sys.argv[1] == '-ec':
		
		if len(sys.argv) == 2:
			environmentConfigure()
		else:
			help()
		exit()

	if sys.argv[1] == '-bc':
		
		if len(sys.argv) == 3:
			baseConfigure(int(sys.argv[2]))
		else:
			help()
		exit()

	if sys.argv[1] == '-nvc':
		
		if len(sys.argv) == 3:
			nfvVMConfigure(int(sys.argv[2]))
		else:
			help()
		exit()

	if sys.argv[1] == '-gvc':
		
		if len(sys.argv) == 5:
			generalVMConfigure(int(sys.argv[2]), sys.argv[3], int(sys.argv[4]))
		else:
			help()
		exit()

	if sys.argv[1] == '-dr':
		
		if len(sys.argv) == 1:
			downloadRepository()
		else:
			help()
		exit()
else:
	help()
