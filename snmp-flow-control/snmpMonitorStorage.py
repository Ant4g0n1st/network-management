from utilityFunctions import BuildDataSourceString

import appConstants
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
                BuildDataSourceString(
                    appConstants.DS_BANDWIDTH, 
                    appConstants.RRD_GAUGE)
            ]

        errorCode = rrdtool.create(self.fileName,
                '--start', appConstants.RRD_NOW,
                '--step', appConstants.RRD_STEP,
                *dataSources,
                *appConstants.RRA_DEFAULT_SETTINGS
            )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise
    
    def updateDatabase(self, update):
        updateString = appConstants.RRD_NOW
        updateString += ':' + update

        rrdtool.update(self.fileName, updateString)

