#SNMP Version Constants according to the API.

SNMP_V2C = 1
SNMP_V1 = 0

#Monitor Constants.

MONITOR_FREQ = 20

#RRDTool Constants

RRA_DEFAULT_SETTINGS = [
    'RRA:AVERAGE:0.5:1:120', # 10-hours
    'RRA:AVERAGE:0.5:3:360', # 30-hours
    'RRA:AVERAGE:0.5:9:1080' # 90-hours
]

RRD_THRESHOLD = '60'
RRD_STEP = '30'

DB_FILENAME = 'bw.rrd'
DS_OUTBW = 'outBw'
DS_INBW = 'inBw'

GRAPH_HEIGHT = '320'
GRAPH_WIDTH = '1280'

RRD_COUNTER = 'COUNTER'
RRD_GAUGE = 'GAUGE'

RRD_UNKNOWN = 'U'
RRD_NOW = 'N'

#Report Generator Constants.

TEMPLATE_FILE = 'reportTemplate.html'

