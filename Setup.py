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
	call(['apt-get', 'install', 'webfsd'])

def baseInternalConfigure(bridgesQuantity):

	for bridge in range(bridgesQuantity):
		bridgeID = 'br' + str(bridge)
		call(['brctl', 'addbr', bridgeID])
		call(['ifconfig', bridgeID, 'up'])
		call(['ethtool', '-K', bridgeID, 'rx', 'off', 'tx', 'off', 'sg', 'off', 'tso', 'off', 'ufo', 'off', 'gso', 'off', 'gro', 'off', 'lro', 'off'])

def baseExternalConfigure(bridgesQuantity, baseNetwork, physicalInterface):

	baseInternalConfigure(bridgesQuantity)
	call(['brctl', 'addif', 'br0', physicalInterface])
	call(['route', 'add', '-net', baseNetwork+'.0', 'netmask', '255.255.255.0', 'br0'])
	call(['route', 'add', 'default', 'gw', baseNetwork+'.1', 'br0'])


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


def startHTTPServer(directoryPath):

	call(['webfsd', '-F', '-R', directoryPath, '-p', '80'])


def startHTTPSServer(directoryPath, pemCertificate, pemKey):

	call(['webfsd', '-F', '-S', '-C', pemCertificate, '-K', pemKey, '-R', directoryPath, '-p', '443'])


def help():
	print('--')
	print('-ec -> Environment Configure')
	print('-bci bridgesQuantity -> Base Configure for Internal Traffic')
	print('-bce bridgesQuantity baseNetwork physicalInterface -> Base Configure for External Traffic')
	print('-nvc ifacesQuantity -> NFV VM Configure')
	print('-gvc ifacesQuantity baseNetwork ipBegin -> General VM Configure')
	print('-dr -> Download Repository')
	print('-http directoryPath -> Start HTTP Server')
	print('-https directoryPath pemCertificate pemKey -> Start HTTPS Server')
	print('--')

if len(sys.argv) > 1:
	
	if sys.argv[1] == '-ec':
		
		if len(sys.argv) == 2:
			environmentConfigure()
		else:
			help()
		exit()

	if sys.argv[1] == '-bci':
		
		if len(sys.argv) == 3:
			baseInternalConfigure(int(sys.argv[2]))
		else:
			help()
		exit()

	if sys.argv[1] == '-bce':

		if len(sys.argv) == 5:
			baseExternalConfigure(int(sys.argv[2]), sys.argv[3], sys.argv[4])
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
		
		if len(sys.argv) == 2:
			downloadRepository()
		else:
			help()
		exit()

	if sys.argv[1] == '-http':

		if len(sys.argv) == 3:
			startHTTPServer(sys.argv[2])
		else:
			help()
		exit()

	if sys.argv[1] == '-https':

		if len(sys.argv) == 5:
			startHTTPSServer(sys.argv[2], sys.argv[3], sys.argv[4])
		else:
			help()
		exit()
	
	help()

else:
	help()
