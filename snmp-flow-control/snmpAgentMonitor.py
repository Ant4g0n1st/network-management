from snmpMonitorStorage import SnmpMonitorStorage
from threading import Thread

import snmpQuery as snmp
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

        # Information to compute deltas.
        self.previous = dict()

        self.previous['time'] = int(time.time())
        self.previous['time'] -= appConstants.MONITOR_FREQ

        self.start()

    def stop(self):
        self.running = False

    def __del__(self):
        self.stop()

    def query(self):
        # Get the device's ifTable
        query = snmp.snmpWalk(
                self.snmpAgentInfo.snmpVersion,
                self.snmpAgentInfo.community,
                self.snmpAgentInfo.address,
                self.snmpAgentInfo.port,
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
        ifOutOctets = int(query['1.3.6.1.2.1.2.2.1.16.' + ifIndex])
        ifInOctets = int(query['1.3.6.1.2.1.2.2.1.10.' + ifIndex])

        if not 'ifOutOctets' in self.previous:
            self.previous['ifOutOctets'] = ifOutOctets

        if not 'ifInOctets' in self.previous:
            self.previous['ifInOctets'] = ifInOctets

        deltaOut = ifOutOctets - self.previous['ifOutOctets']
        deltaIn = ifInOctets - self.previous['ifInOctets']
        deltaTime = now - self.previous['time']

        outBandwidth = (deltaOut * 8) / deltaTime
        inBandwidth = (deltaIn * 8) / deltaTime
        
        # Store the current values for the next iteration.
        self.previous['ifOutOctets'] = ifOutOctets
        self.previous['ifInOctets'] = ifInOctets
        self.previous['time'] = now
    
        return {
                appConstants.DS_OUTBW : outBandwidth,
                appConstants.DS_INBW : inBandwidth
            }

    def run(self):
        while self.running:
            try:
                updates = self.query()

                self.storage.updateDatabase(updates)

                time.sleep(appConstants.MONITOR_FREQ) 

            except:
                logging.error('Exception while monitoring %s : %s',
                    self.snmpAgentInfo, sys.exc_info())
                self.stop()

