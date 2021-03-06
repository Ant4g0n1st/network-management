from snmpNotificationMessages import LinkDownMessage
from snmpAgentInfo import SnmpAgentInfo

import sys

COMMUNITY = 'Victor4cv5'

hostname = input()

address = input()

# The addresses come as:
#   UDP [agent]:port->[server]:port
address = address.split(' ')[-1]
address = address.split('->')

server = address[-1].split(':')
serverAddr =  server[0][1:-1]
serverPort = server[-1]

agent = address[0].split(':')
agentAddr = agent[0][1:-1]
agentPort = agent[-1]

# We are expected to receive:
#   sysUpTime
#   snmpTrapOID
#   ifIndex
#   ifDescr
#   ifAdminStatus
#   ifOperStatus

oids = dict()

for line in sys.stdin:
    tokens = line.split()
    oids[tokens[0]] = tokens[-1]

trap = dict()

for key in oids:                                                                                                      
    if key.startswith('iso.3.6.1.2.1.2.2.1.2.'):
        trap['ifDescr'] = oids[key]
        break

trap['serverAddress'] = serverAddr
trap['serverPort'] = serverPort

trap['agentAddress'] = agentAddr
trap['agentPort'] = agentPort

agentInfo = SnmpAgentInfo(agentAddr, COMMUNITY)
message = LinkDownMessage(agentInfo, trap)
message.sendMessage()

