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

    def run(self):
        while self.running:
            try:
                # We run nfdump to get the UDP traffic.
                # This query reads as:
                #    Check on all traffic records for flows created on
                #    the last five minutes and filter for every entry 
                #    that contains the given ip as an endpoint.
                # The collector (fprobe) daemon is configured to
                # to only care about UDP flows.
                output = subprocess.check_output([
                        'nfdump', '-R', '/var/cache/nfdump/', 
                        '-t', '-300', '-b', '-o', 'csv', 
                        'dst ip {0} or src ip {0}'.format(
                            self.snmpAgentInfo.address)
                    ])
    
                #The output is returned as bytes.
                output = output.decode().split()

                # According to the output format, the average
                # bps is always at the last line in the 
                # fourth position of a list.
                output = output[-1].split(',')
                print(output)

                update = output[3]
                print(update)

                self.storage.updateDatabase(update)

                time.sleep(appConstants.MONITOR_FREQ) 

            except:
                logging.error('Exception while monitoring %s : %s',
                    self.snmpAgentInfo, sys.exc_info())
                self.stop()

