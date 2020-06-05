from appConstants import HR_PROCESSOR_LOAD_COLUMN

import snmpQuery as snmp

def getAverageProcessorLoad(snmpAgentInfo):
    table = snmp.snmpWalk(
            snmpAgentInfo.snmpVersion,
            snmpAgentInfo.community,
            snmpAgentInfo.address,
            snmpAgentInfo.port,
            HR_PROCESSOR_LOAD_COLUMN
        )
    if table == None:
        return table

    totalProcessorLoad = 0
    processorCount = 0

    # Compute the total load of all processors.
    for key, value in table.items():
        totalProcessorLoad += float(value)
        processorCount += 1 

    # Compute the average.
    if not processorCount:
        return totalProcessorLoad

    return totalProcessorLoad / float(processorCount)
    
