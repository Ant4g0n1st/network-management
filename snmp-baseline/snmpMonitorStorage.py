from utilityFunctions import BuildDataSourceString

import appConstants
import rrdConstants
import rrdtool
import shutil
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
                    rrdConstants.TYPE_COUNTER),
                BuildDataSourceString(rrdConstants.DS_DISK,
                    rrdConstants.TYPE_COUNTER),
                BuildDataSourceString(rrdConstants.DS_CPU,
                    rrdConstants.TYPE_COUNTER)
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
    
    def updateDatabase(self, updateValues):
        updateString = rrdConstants.NOW + ':'
        updateString += ':'.join(updateValues)
        rrdtool.update(self.fileName, updateString)

