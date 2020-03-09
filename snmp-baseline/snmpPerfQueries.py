from appConstants import HR_STORAGE_TABLE_OID

import snmpQuery as snmp

def getStorageTable(snmpAgentInfo):
    return snmp.snmpWalk(
            snmpAgentInfo.snmpVersion,
            snmpAgentInfo.community,
            snmpAgentInfo.address,
            snmpAgentInfo.port,
            HR_STORAGE_TABLE_OID
        )

def getDiskUsagePercentage(snmpAgentInfo):
    table = getStorageTable(snmpAgentInfo)
    if table == None:
        return table

    totalDiskSpace = 0
    totalUsedSpace = 0

    for key, value in table.items():

        # Check if the type is hrStorageFixedDisk.
        if value != '1.3.6.1.2.1.25.2.1.4':
            continue

        # Get the id of the disk at the end of the OID.
        storageId = key.split('.')[-1]

        # Get the size of the disk in allocation units.
        oid = '1.3.6.1.2.1.25.2.3.1.5.{0}'.format(storageId)
        totalDiskSpace += float(table[oid])

        # Get the space used in the disk in allocation units.
        oid = '1.3.6.1.2.1.25.2.3.1.6.{0}'.format(storageId)
        totalUsedSpace += float(table[oid]) 

    #Compute percentage.
    return totalUsedSpace / totalDiskSpace * float(100)

def getMemoryUsagePercentage(snmpAgentInfo):
    table = getStorageTable(snmpAgentInfo) 
    if table == None:
        return table
    
    totalMemorySize = 0
    totalMemoryUsed = 0

    for key, value in table.items():

        # Check if the type is hrStorageRam.
        if value != '1.3.6.1.2.1.25.2.1.2':
            continue

        # Get the id of the memory at the end of the OID.
        storageId = key.split('.')[-1]

        # Get the size of the memory in allocation units.
        oid = '1.3.6.1.2.1.25.2.3.1.5.{0}'.format(storageId)
        totalMemorySize += float(table[oid])

        # Get the space used in the memory in allocation units.
        oid = '1.3.6.1.2.1.25.2.3.1.6.{0}'.format(storageId)
        totalMemoryUsed += float(table[oid]) 

    #Compute percentage.
    return totalMemoryUsed / totalMemorySize * float(100)
    
from snmpAgentInfo import SnmpAgentInfo
#agent = SnmpAgentInfo('localhost', 161, 'grupo4cv5')
agent = SnmpAgentInfo('192.168.0.108', 161, 'grupo4cv5')
print(
getDiskUsagePercentage(agent)
)
print(
getMemoryUsagePercentage(agent)
)
     
