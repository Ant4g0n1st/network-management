import appConstants
import logging

class SnmpAgentInfo:

    def __init__(self, address, port, community, snmpVersion = appConstants.SNMP_V2C):
        self.snmpVersion = snmpVersion
        self.community = community
        self.address = address
        self.port = port

    def __str__(self):
        return '[SNMPv{0}, {1}, {2}, {3}]'.format(
            self.snmpVersion + 1,
            self.community,
            self.address,
            self.port,
        )

