from snmpMonitorStorage import SnmpMonitorStorage
from threading import Thread

import appConstants
import subprocess
import snmpQuery
import logging
import time
import sys

class SnmpAgentMonitor(Thread):

    def __init__(self, snmpAgentInfo):
        Thread.__init__(self)
        self.storage = SnmpMonitorStorage(snmpAgentInfo)
        self.snmpAgentInfo = snmpAgentInfo
        self.running = True
        self.start()

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

    def query():
         

    def run(self):
        while self.running:
            try:

                self.storage.updateDatabase(update)

                time.sleep(appConstants.MONITOR_FREQ) 

            except:
                logging.error('Exception while monitoring %s : %s',
                    self.snmpAgentInfo, sys.exc_info())
                self.stop()

