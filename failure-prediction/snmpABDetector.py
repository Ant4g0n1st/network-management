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

        rrdtool.tune(self.fileName, 
                '--failure-threshold', rrdConstants.HW_FAILURE_THRESHOLD,
                '--window-length', rrdConstants.HW_WINDOW_LENGTH
            )
    
    # Returns True if there was a failure.
    def update(self, updates):
        updateString = rrdConstants.NOW
        
        for key, value in updates.items():
            updates[key] = str(value) if value != None else rrdConstants.UNKNOWN

        updateString += (':' + updates[rrdConstants.DS_NETWORK])

        rrdtool.update(self.fileName, updateString)
        end = rrdtool.last(self.fileName)

        #begin = str(end - rrdConstants.TIME_FRAME)
        begin = str(end - 5 * 60 * 60)
        end = str(end)

        fail = float(rrdGraphs.makeNetworkGraph(self.path, begin, end))

        if math.isnan(fail):
            return False

        fail = int(fail)

        return fail > 0

