import snmpQuery as snmp

import rrdtool
import time

FILENAME = 'udp.rrd'
SLEEP_TIME = 2

OIDS = [
    '1.3.6.1.2.1.7.1.0',
    '1.3.6.1.2.1.7.4.0'
]

rrdtool.create(FILENAME,
    '--start', 'N',
    '--step', '10',
    'DS:udpIn:COUNTER:20:U:U',
    'DS:udpOut:COUNTER:20:U:U',
    'RRA:AVERAGE:0.5:1:1000')

while True:
    query = snmp.snmpGet(1, 'grupo4cv5', 'localhost', 161, OIDS)
    updateString = 'N:' + ':'.join(list(query.values()))
    rrdtool.update(FILENAME, updateString)
    print(updateString)
    time.sleep(SLEEP_TIME)

