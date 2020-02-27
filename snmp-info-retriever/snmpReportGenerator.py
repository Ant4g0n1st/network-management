from appConstants import DB_FILENAME, TEMPLATE_FILE

import rrdtool
import pdfkit
import jinja2
import os

class SnmpReportGenerator:

    def __init__(self, agentInfo):
        self.resourceFolder = agentInfo.getIdentifier()
        self.agentInfo = agentInfo
        self.loadTemplate()

    def loadTemplate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath = './')
        templateEnv = jinja2.Environment(loader = templateLoader)
        self.template = templateEnv.get_template(TEMPLATE_FILE)
    
    # This has to be cleaner.
    def renderGraphs(self, startTime, endTime):
        rrdtool.graph(self.resourceFolder + '/ifOutNUcastPkts.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=Packets/s',
                'DEF:{0}={1}:{2}:{3}'.format('outnucast',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'ifOutNUcastPkts',
                        'AVERAGE'
                    ),
                'AREA:outnucast#0000FF:Paquetes Multicast Enviados'
            )
        rrdtool.graph(self.resourceFolder + '/ipOutRequests.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=Packets/s',
                'DEF:{0}={1}:{2}:{3}'.format('ipout',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'ipOutRequests',
                        'AVERAGE'
                    ),
                'AREA:ipout#00FF00:Solicitudes IP'
            )
        rrdtool.graph(self.resourceFolder + '/icmpInMsgs.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=ICMP Msgs/s',
                'DEF:{0}={1}:{2}:{3}'.format('icmp',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'icmpInMsgs',
                        'AVERAGE'
                    ),
                'AREA:icmp#FF0000:Mensajes ICMP'
            )
        rrdtool.graph(self.resourceFolder + '/tcpRetransSegs.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=TCP Retrans/s',
                'DEF:{0}={1}:{2}:{3}'.format('tcpret',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'tcpRetransSegs',
                        'AVERAGE'
                    ),
                'AREA:tcpret#000000:Segmentos TCP Retransmitidos'
            )
        rrdtool.graph(self.resourceFolder + '/udpOutDatagrams.png',
                '--start', str(startTime),
                '--end', str(endTime),
                '--vertical-label=UDP Datagrams/s',
                'DEF:{0}={1}:{2}:{3}'.format('udpout',
                        self.resourceFolder + '/' + DB_FILENAME,
                        'udpOutDatagrams',
                        'AVERAGE'
                    ),
                'AREA:udpout#777777:Datagramas enviados.'
            )
    
    def renderHTML(self):
        self.renderedHTML = self.template.render(
                ifGraphFile = os.path.abspath(
                    self.resourceFolder + '/ifOutNUcastPkts.png'),
                ipGraphFile = os.path.abspath(
                    self.resourceFolder + '/ipOutRequests.png'),
                icmpGraphFile = os.path.abspath(
                    self.resourceFolder + '/icmpInMsgs.png'),
                tcpGraphFile = os.path.abspath(
                    self.resourceFolder + '/tcpRetransSegs.png'),
                udpGraphFile = os.path.abspath(
                    self.resourceFolder + '/udpOutDatagrams.png')
            )

    def makeReport(self, startTime, endTime):
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, 'report.pdf')
