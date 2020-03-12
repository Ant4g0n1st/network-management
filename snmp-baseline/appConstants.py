#SNMP Version Constants according to the API.

SNMP_V2C = 1
SNMP_V1 = 0

#Monitor Constants.

MONITOR_FREQ = 300

#Nodes to be monitored.

HR_PROCESSOR_LOAD_COLUMN = '1.3.6.1.2.1.25.3.3.1.2'
HR_STORAGE_TABLE_OID = '1.3.6.1.2.1.25.2.3'

SIMPLE_NODES = sorted(
        [
            'udpOutDatagrams',
            'tcpRetransSegs',
            'ipOutRequests',
            'icmpInMsgs'
        ]
    )

COMPLEX_NODES = sorted(
        [
            'ifOutNUcastPkts'
        ]
    )

NAME_TO_OID = {
        'ifOutNUcastPkts'   : '1.3.6.1.2.1.2.2.1.18',
        'tcpRetransSegs'    : '1.3.6.1.2.1.6.12.0',
        'ipOutRequests'     : '1.3.6.1.2.1.4.10.0',
        'udpOutDatagrams'   : '1.3.6.1.2.1.7.4.0', 
        'icmpInMsgs'        : '1.3.6.1.2.1.5.1.0'
    }

COMPLEX_OIDS = [NAME_TO_OID[name] for name in COMPLEX_NODES]
SIMPLE_OIDS = [NAME_TO_OID[name] for name in SIMPLE_NODES]

OID_TO_NAME = dict()
for x in range(0, len(COMPLEX_OIDS)):
    OID_TO_NAME[COMPLEX_OIDS[x]] = COMPLEX_NODES[x]
for x in range(0, len(SIMPLE_OIDS)):
    OID_TO_NAME[SIMPLE_OIDS[x]] = SIMPLE_NODES[x]

#RRDTool Constants

DB_FILENAME = 'perf.rrd'
RRD_COUNTER = 'COUNTER'
RRD_THRESHOLD = '60'
RRD_UNKNOWN = 'U'
RRD_STEP = '20'
RRD_NOW = 'N'

NAME_TO_RRDTYPE = {
        'ifOutNUcastPkts'   : RRD_COUNTER,
        'udpOutDatagrams'   : RRD_COUNTER,
        'tcpRetransSegs'    : RRD_COUNTER, 
        'ipOutRequests'     : RRD_COUNTER,
        'icmpInMsgs'        : RRD_COUNTER
    }

#Report Generator Constants.

TEMPLATE_FILE = 'reportTemplate.html'

