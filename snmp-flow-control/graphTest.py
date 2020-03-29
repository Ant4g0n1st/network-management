import rrdtool

rrdtool.graph( "traficoRED.png",
                 "--start",'1582610400',
                "--end","N",
                 "--vertical-label=Bytes/s",
                 "DEF:icmp=localhost/snmp.rrd:icmpInMsgs:AVERAGE",
                 "LINE1:icmp#0000FF:ICMP in Msgs\r")

