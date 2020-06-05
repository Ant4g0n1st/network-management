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

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.fileName = '/' + appConstants.DB_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self):
        if os.path.isfile(self.fileName):
            return

        dataSources = [
                BuildDataSourceString(rrdConstants.DS_CPU,
                    rrdConstants.TYPE_GAUGE,
                    sampleMin = '0', sampleMax = '100')
            ]

        errorCode = rrdtool.create(self.fileName,
                '--start', rrdConstants.NOW,
                '--step', rrdConstants.STEP,
                *dataSources,
                *rrdConstants.RRA_DEFAULT_SETTINGS
            )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise
    
    def updateDatabase(self, updates):
        updateString = rrdConstants.NOW
        
        for key, value in updates.items():
            updates[key] = str(value) if value != None else rrdConstants.UNKNOWN

        updateString += (':' + updates[rrdConstants.DS_CPU])

        rrdtool.update(self.fileName, updateString)

