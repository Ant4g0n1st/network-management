from utilityFunctions import BuildDataSourceString

import rrdConstants
import rrdGraphs
import rrdtool
import shutil
import math
import os

class GraphMaker:

    def __init__(self, path):
        self.makeStorageFile(path)

    def makeStorageFile(self, path):
        self.path = path 

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        self.fileName = '/' + rrdConstants.HW_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self, alpha, beta, period):
        if os.path.isfile(self.fileName):
            return

        dataSources = [
                BuildDataSourceString(rrdConstants.DS_NETWORK,
                    rrdConstants.TYPE_GAUGE)
            ]

        rowCount = 10 * period

        errorCode = rrdtool.create(self.fileName,
                '--start', rrdConstants.NOW,
                '--step', rrdConstants.STEP,
                *dataSources,
                *rrdConstants.RRA_DEFAULT_SETTINGS,
                rrdConstants.RRA_HW_SETTINGS.format(rowCount, alpha, beta, period)
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
        rrdtool.update(self.fileName, *updates)

    def MakeGraph(self, start, end):
        rrdGraphs.makeNetworkGraph(self.path, begin, end)

