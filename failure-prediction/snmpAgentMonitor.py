from snmpNotificationManager import SnmpNotificationManager
from snmpMonitorStorage import SnmpMonitorStorage
from threading import Thread

import snmpPerfQueries as perf
import appConstants
import rrdConstants
import snmpQuery
import logging
import time
import sys

class SnmpAgentMonitor(Thread):

    def __init__(self, snmpAgentInfo):
        Thread.__init__(self)
        self.notificationManager = SnmpNotificationManager(snmpAgentInfo)
        self.storage = SnmpMonitorStorage(snmpAgentInfo)
        self.agent = snmpAgentInfo
        self.running = True
        self.start()

    def setGroup(self, group):
        self.group = group

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

    def run(self):
        while self.running:
            try:
                updates = dict()
              
                updates[rrdConstants.DS_CPU] = perf.getAverageProcessorLoad(self.agent)

                self.storage.updateDatabase(updates)

                #if notificationLevel == rrdConstants.READY:
                #    self.notificationManager.sendNotification() 

                self.notificationManager.flushPending()
                
                time.sleep(appConstants.MONITOR_FREQ)

            except:
                logging.error('Exception while monitoring %s : %s',
                    self.agent, sys.exc_info())
                self.stop()

        self.group.stageRemoval(self.agent)
        self.group = None

