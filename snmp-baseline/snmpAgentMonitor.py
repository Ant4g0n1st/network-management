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

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

    def run(self):
        while self.running:
            try:
                updates = dict()
              
                updates[rrdConstants.DS_MEMORY] = perf.getMemoryUsagePercentage(self.agent)
                updates[rrdConstants.DS_DISK] = perf.getDiskUsagePercentage(self.agent)
                updates[rrdConstants.DS_CPU] = perf.getAverageProcessorLoad(self.agent)

                notificationLevel = self.storage.updateDatabase(updates)
                print(notificationLevel)

                if notificationLevel == rrdConstants.READY:
                    self.notificationManager.sendReadyNotification() 
                elif notificationLevel == rrdConstants.SET:
                    self.notificationManager.sendSetNotification()
                elif notificationLevel == rrdConstants.GO:
                    self.notificationManager.sendGoNotification()

                self.notificationManager.flushPending()
                
                time.sleep(appConstants.MONITOR_FREQ)                

            except:
                logging.error('Exception while monitoring %s : %s',
                    self.agent, sys.exc_info())
                self.stop()

