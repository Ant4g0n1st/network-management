from utilityFunctions import BuildDataSourceString

import rrdConstants
import rrdGraphs
import rrdtool
import shutil
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

    def createDatabase(self, start, alpha, beta, period):
        if os.path.isfile(self.fileName):
            return

        dataSources = [
                BuildDataSourceString(rrdConstants.DS_NETWORK,
                    rrdConstants.TYPE_GAUGE)
            ]

        rowCount = 10 * period

        errorCode = rrdtool.create(self.fileName,
                '--start', start,
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
    
    def update(self, updates):
        rrdtool.update(self.fileName, *updates)

    def makeGraph(self, start, end):
        rrdGraphs.makeNetworkGraph(self.path, start, end)

deltaB = 0.000125
deltaA = 0.005

period = 17

beta = 0.00375
alpha = 0.72

iterations = 5

a = alpha
b = beta

f = open('series.txt', 'r')

updates = [line.strip() for line in f]

f.close()

start = updates[0].split(':')[0]
start = str(int(start) - 300)

end = updates[-1].split(':')[0]
end = str(int(end) + 300)

for i in range(0, iterations):
    for j in range(0, iterations):
        path = '{0}-{1}-{2}'.format(a, b, period)

        gm = GraphMaker(path.replace('.', '_'))
        gm.createDatabase(start, a, b, period)
        gm.update(updates)
        gm.makeGraph(start, end)

        b = round(b + deltaB, 7)

    a = round(a + deltaA, 4)
    b = beta

