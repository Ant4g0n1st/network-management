from threading import Thread

import snmpQuery
import logging
import sys

class SnmpAgentMonitor(Thread):

    QUERY_OIDS = [
        '1.3.6.1.2.1.1.1.0', 
        '1.3.6.1.2.1.1.5.0'
    ]

    def __init__(self, snmpAgentInfo):
        Thread.__init__(self)
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
                responses = snmpQuery.snmpGet(
                    self.snmpAgentInfo.snmpVersion,
                    self.snmpAgentInfo.community,
                    self.snmpAgentInfo.address,
                    self.snmpAgentInfo.port,
                    SnmpAgentMonitor.QUERY_OIDS
                )
                if responses:
                    logging.info('Response received : %s.', responses)
                else:
                    logging.info('No response received.')
            except:
                logging.log('Exception while monitoring %s : %s',
                    self.snmpAgentInfo, sys.exc_info())
                self.stop()

