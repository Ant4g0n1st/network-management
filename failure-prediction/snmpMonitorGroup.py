from snmpAgentMonitor import SnmpAgentMonitor
from snmpAgentInfo import SnmpAgentInfo

class SnmpMonitorGroup:

    def __init__(self):
        self.monitors = dict()
        self.agents = list()
        self.queue = list()

    def addAgentMonitor(self, agentInfo):
        self.commitPending()
        if not self.containsAgentMonitor(agentInfo):
            identifier = agentInfo.getIdentifier()
            self.monitors[identifier] = SnmpAgentMonitor(agentInfo)
            self.monitors[identifier].setGroup(self)
            self.agents.append(agentInfo)

    def containsAgentMonitor(self, agentInfo):
        return (agentInfo.getIdentifier() in self.monitors)

    def removeAgentMonitor(self, agentInfo):
        if self.containsAgentMonitor(agentInfo):
            del self.agents[self.agents.index(agentInfo)]
            self.monitors[agentInfo.getIdentifier()].stop()
            del self.monitors[agentInfo.getIdentifier()]

    def getAgentList(self):
        self.commitPending()
        return self.agents

    def __del__(self):
        for agent, monitor in self.monitors.items():
            monitor.stop()

    # We remove agents on a lazy way to avoid
    # issues when removing from the monitor.
    def stageRemoval(self, agentInfo):
        self.queue.append(agentInfo)

    def commitPending(self):
        for agent in self.queue:
            self.removeAgentMonitor(agent)
        self.queue.clear()

