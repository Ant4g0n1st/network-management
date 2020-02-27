from snmpAgentMonitor import SnmpAgentMonitor
from snmpAgentInfo import SnmpAgentInfo

class SnmpMonitorGroup:

    def __init__(self):
        self.monitors = dict()
        self.agents = list()

    def addAgentMonitor(self, agentInfo):
        if not self.containsAgentMonitor(agentInfo):
            self.monitors[agentInfo.getIdentifier()] = SnmpAgentMonitor(agentInfo)
            self.agents.append(agentInfo)

    def containsAgentMonitor(self, agentInfo):
        return (agentInfo.getIdentifier() in self.monitors)

    def removeAgentMonitor(self, agentInfo):
        if self.containsAgentMonitor(agentInfo):
            del self.monitors[agentInfo.getIdentifier()]

    def __del__(self):
        del self.monitors
