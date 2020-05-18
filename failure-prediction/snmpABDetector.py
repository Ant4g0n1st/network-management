from utilityFunctions import BuildDataSourceString

import rrdConstants
import rrdGraphs
import rrdtool
import shutil
import math
import os

class AberrantBehaviorDetector:

    def __init__(self, snmpAgentInfo):
        self.makeStorageFile(snmpAgentInfo)
        self.createDatabase()

    def makeStorageFile(self, snmpAgentInfo):
        self.path = snmpAgentInfo.getIdentifier() 

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.fileName = '/' + rrdConstants.HW_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self):
        if os.path.isfile(self.fileName):
            return

        dataSources = [
                BuildDataSourceString(rrdConstants.DS_NETWORK,
                    rrdConstants.TYPE_GAUGE)
            ]

        errorCode = rrdtool.create(self.fileName,
                '--start', rrdConstants.NOW,
                '--step', rrdConstants.STEP,
                *dataSources,
                *rrdConstants.RRA_DEFAULT_SETTINGS,
                rrdConstants.RRA_HW_SETTINGS
            )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise
    
    # Returns True if there was a failure.
    def update(self, updates):
        updateString = rrdConstants.NOW
        
        for key, value in updates.items():
            updates[key] = str(value) if value != None else rrdConstants.UNKNOWN

        updateString += (':' + updates[rrdConstants.DS_NETWORK])

        print(updateString)

        rrdtool.update(self.fileName, updateString)
        end = rrdtool.last(self.fileName)

        begin = str(end - rrdConstants.TIME_FRAME)
        end = str(end)

        fail = float(rrdGraphs.makeNetworkGraph(self.path, begin, end))

        if math.isnan(fail):
            return False

        fail = int(fail)
        
        print(fail)

        return fail > 0

