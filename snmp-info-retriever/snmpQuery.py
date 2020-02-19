import pysnmp.hlapi.asyncore as snmp

import threading
import datetime
import logging

def snmpCallbackFunction(snmpEngine, sendRequestHandle, errorIndication,
    errorStatus, errorIndex, varBinds, cbCtx):

    if errorIndication: 
        logging.error(errorIndication)
        return

    if errorStatus:
        logging.error('%s at %s', errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
        return
    
    for name, value in varBinds:
        logging.info('Response received : %s = %s', name, value)

    cbCtx.set()    

def snmpQuery(community, host, oid, port = 161):
    logging.info('New Query [%s, %s, %s, %d]', 
        community, host, oid, port)
    
    snmpEngine = snmp.SnmpEngine()

    snmpResponseEvent = threading.Event()

    snmp.getCmd(snmpEngine,
        snmp.CommunityData(community),
        snmp.UdpTransportTarget((host, port)),
        snmp.ContextData(),
        snmp.ObjectType(snmp.ObjectIdentity(oid)),
        cbFun = snmpCallbackFunction,
        cbCtx = snmpResponseEvent)

    snmpEngine.transportDispatcher.runDispatcher()

    snmpResponseEvent.wait()

loggerFormat = '%(asctime)s %(levelname)s %(module)s.%(funcName)s'
loggerFormat += ' [line = %(lineno)d] : %(message)s' 

logging.basicConfig(format = loggerFormat,
    datefmt = '%m/%d/%Y %I:%M:%S %p',
    #filename = 'logs/meow.log',
    level = logging.DEBUG)

snmpQuery('grupo4cv5', 'localhost', '1.3.6.1.2.1.1.1.0')

