from snmpAgentMonitor import SnmpAgentMonitor
from snmpAgentInfo import SnmpAgentInfo

class SnmpMonitorGroup:

    def __init__(self):
        self.monitors = dict()
        self.devices = list()

    def addAgentMonitor(self, agentInfo):
        self.monitors[agentInfo.getIdentifier()] = SnmpAgentMonitor(agentInfo)
        print(self.monitors)


