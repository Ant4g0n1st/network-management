from utilityFunctions import StoragePathFromAddress, BuildDataSourceString
from threading import Thread

import appConstants
import rrdtool
import shutil
import os

class SnmpMonitorStorage(Thread):

    def __init__(self, snmpAgentInfo):
        Thread.__init__(self)
        self.makeStorageFile(snmpAgentInfo)
        self.createDatabase()

    def makeStorageFile(self, snmpAgentInfo):
        self.path = StoragePathFromAddress(
                snmpAgentInfo.address    
            )

        if os.path.exists(self.path):
            shutil.rmtree(self.path)

        os.makedirs(self.path)

        self.fileName = '/' + appConstants.DB_FILENAME
        self.fileName = self.path + self.fileName

    def createDatabase(self):
        errorCode = rrdtool.create(self.fileName,
                '--start', appConstants.RRD_NOW,
                '--step', appConstants.RRD_STEP,
                BuildDataSourceString(
                    'ifOutNUcastPkts',
                    appConstants.RRD_COUNTER
                ), 
                BuildDataSourceString(
                    'ipOutRequests',
                    appConstants.RRD_COUNTER
                ),
                BuildDataSourceString(
                    'icmpInMsgs',
                    appConstants.RRD_COUNTER
                ),
                BuildDataSourceString(
                    'tcpRetransSegs',
                    appConstants.RRD_COUNTER
                ),
                BuildDataSourceString(
                    'udpOutDatagrams',
                    appConstants.RRD_COUNTER
                ),
                'RRA:AVERAGE:0.5:2:10'
            )

        if errorCode:
            logging.error('Error creating RRDTool file : %s',
                rrdtool.error())
            raise

from snmpAgentInfo import SnmpAgentInfo

SnmpMonitorStorage(SnmpAgentInfo('127.0.0.1', 161, 'grupo4cv5'))

