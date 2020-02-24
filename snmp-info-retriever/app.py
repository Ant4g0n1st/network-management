from snmpAgentMonitor import SnmpAgentMonitor
from snmpAgentInfo import SnmpAgentInfo 
import appLogger

if __name__ == '__main__':
    appLogger.configureLogger()

    agentInfo = SnmpAgentInfo('localhost', 161, 'grupo4cv5')
    SnmpAgentMonitor(agentInfo)

