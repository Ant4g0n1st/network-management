from snmpNotificationManager import SnmpNotificationManager
from snmpABDetector import AberrantBehaviorDetector
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
        self.detector = AberrantBehaviorDetector(snmpAgentInfo)
        self.storage = SnmpMonitorStorage(snmpAgentInfo)
        self.agent = snmpAgentInfo
        self.running = True

        # Information to compute deltas.
        self.previous = dict()

        self.previous['time'] = int(time.time())
        self.previous['time'] -= appConstants.MONITOR_FREQ

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
                updates[rrdConstants.DS_NETWORK] = self.queryBandwidth()

                self.storage.updateDatabase(updates)
                print(
                    self.detector.update(updates)
                    )

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

    def queryBandwidth(self):
        # Get the device's ifTable
        query = snmpQuery.snmpWalk(
                self.agent.snmpVersion,
                self.agent.community,
                self.agent.address,
                self.agent.port,
                '1.3.6.1.2.1.2.2.1'
            ) 
        now = int(time.time())

        # Loop through the entries to find the first
        # interface ot type ethernetCsmacd (6)
        ifIndex = None
        
        for key, value in query.items():
            # Check if this is an ifType column.
            if key.startswith('1.3.6.1.2.1.2.2.1.3.'):
                if not value == '6':
                    continue
                # The ifIndex is the las item on the OID.
                ifIndex = key.split('.')[-1]
                break

        if not ifIndex:
            return None
        
        # Compute average speed using deltas
        # and a formula similar to Cisco's.
        ifInOctets = int(query['1.3.6.1.2.1.2.2.1.10.' + ifIndex])

        if not 'ifInOctets' in self.previous:
            self.previous['ifInOctets'] = ifInOctets

        deltaIn = ifInOctets - self.previous['ifInOctets']
        deltaTime = now - self.previous['time']

        inBandwidth = (deltaIn * 8) / deltaTime
        
        # Store the current values for the next iteration.
        self.previous['ifInOctets'] = ifInOctets
        self.previous['time'] = now
    
        return inBandwidth

