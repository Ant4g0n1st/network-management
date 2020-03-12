from utilityFunctions import BuildDataSourceString

import appConstants
import rrdConstants
import rrdGraphs
import rrdtool
import shutil
import math
import os

class SnmpMonitorStorage:

    def __init__(self, snmpAgentInfo):
        self.makeStorageFile(snmpAgentInfo)
        self.createDatabase()

    def makeStorageFile(self, snmpAgentInfo):
        self.path = snmpAgentInfo.getIdentifier() 

        #if os.path.exists(self.path):
        #    shutil.rmtree(self.path)

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.fileName = '/' + appConstants.DB_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self):
        if os.path.isfile(self.fileName):
            return

        dataSources = [
                BuildDataSourceString(rrdConstants.DS_MEMORY,
                    rrdConstants.TYPE_GAUGE,
                    sampleMin = '0', sampleMax = '100'),
                BuildDataSourceString(rrdConstants.DS_DISK,
                    rrdConstants.TYPE_GAUGE,
                    sampleMin = '0', sampleMax = '100'),
                BuildDataSourceString(rrdConstants.DS_CPU,
                    rrdConstants.TYPE_GAUGE,
                    sampleMin = '0', sampleMax = '100')
            ]

        errorCode = rrdtool.create(self.fileName,
                '--start', rrdConstants.NOW,
                '--step', rrdConstants.STEP,
                *dataSources,
                rrdConstants.RRA_DEFAULT_SETTINGS
            )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise

    def pickNotificationLevel(self, perfValues):
        notificationLevel = rrdConstants.NO_ALERT

        for dataSource, performance in perfValues.items():
            for level, limit in rrdConstants.BASELINE[dataSource].items():
                if not performance < limit:
                    if level > notificationLevel:
                        notificationLevel = level

        return notificationLevel
    
    def updateDatabase(self, updates):
        updateString = rrdConstants.NOW
        
        for key, value in updates.items():
            updates[key] = str(value) if value != None else rrdConstants.UNKNOWN

        updateString += (':' + updates[rrdConstants.DS_MEMORY])
        updateString += (':' + updates[rrdConstants.DS_DISK])
        updateString += (':' + updates[rrdConstants.DS_CPU])

        rrdtool.update(self.fileName, updateString)
        end = rrdtool.last(self.fileName)

        begin, end = str(end - rrdConstants.TIME_FRAME), str(end)

        lastMem = float(rrdGraphs.makeMemoryGraph(self.path, begin, end))
        lastDisk = float(rrdGraphs.makeDiskGraph(self.path, begin, end))
        lastCpu = float(rrdGraphs.makeCPUGraph(self.path, begin, end))

        lastMem = lastMem if not math.isnan(lastMem) else 0
        lastDisk = lastDisk if not math.isnan(lastDisk) else 0
        lastCpu = lastCpu if not math.isnan(lastCpu) else 0

        return self.pickNotificationLevel(
                {
                    rrdConstants.DS_MEMORY : lastMem,
                    rrdConstants.DS_DISK : lastDisk,
                    rrdConstants.DS_CPU : lastCpu
                }
            )

