#SNMP Version Constants according to the API.

SNMP_V2C = 1
SNMP_V1 = 0

#Monitor Constants.

# NetFlow daemon (nfcapd) generates 
# new info every 5-minutes.
MONITOR_FREQ = 300

#Nodes to be monitored.

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

RRA_DEFAULT_SETTINGS = [
    'RRA:AVERAGE:0.5:1:120', # 10-hours
    'RRA:AVERAGE:0.5:3:360', # 30-hours
    'RRA:AVERAGE:0.5:9:1080' # 90-hours
]

RRD_THRESHOLD = '600'
RRD_STEP = '300'

DS_BANDWIDTH = 'bandwidth'
DB_FILENAME = 'bw.rrd'

GRAPH_HEIGHT = '320'
GRAPH_WIDTH = '1280'

RRD_COUNTER = 'COUNTER'
RRD_GAUGE = 'GAUGE'

RRD_UNKNOWN = 'U'
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

