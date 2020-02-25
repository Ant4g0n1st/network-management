from snmpMonitorGroup import SnmpMonitorGroup
from snmpAgentInfo import SnmpAgentInfo 
import appLogger

import time
if __name__ == '__main__':
    appLogger.configureLogger()

    snmpMonitorGroup = SnmpMonitorGroup()

    agentInfo = SnmpAgentInfo('localhost', 161, 'grupo4cv5')
    snmpMonitorGroup.addAgentMonitor(agentInfo)
    time.sleep(15)
    agentInfo = SnmpAgentInfo('127.0.0.1', 161, 'grupo4cv5')
    snmpMonitorGroup.addAgentMonitor(agentInfo)

