import pysnmp.hlapi as snmp

import appLogger
import threading
import datetime
import logging

def snmpQuery(community, host, oid, port = 161):

    logging.info('New Query [%s, %s, %s, %d]', 
        community, host, oid, port)

    errorIndication, errorStatus, errorIndex, varBinds = next(
            snmp.getCmd(snmp.SnmpEngine(),
                snmp.CommunityData(community),
                snmp.UdpTransportTarget((host, port)),
                snmp.ContextData(),
                snmp.ObjectType(snmp.ObjectIdentity(oid))
            )
        )

    if errorIndication: 
        logging.error(errorIndication)
        return None

    if errorStatus:
        logging.error('%s at %s', errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex) - 1][0] or '?')
        return None

    results = [(str(name), str(value)) for name, value in varBinds]

    return dict(results)

appLogger.configureLogger()

logging.info('Response values : %s', str(snmpQuery('grupo4cv5', 'localhost', '1.3.6.1.2.1.1.1.0')))

