from appConstants import DB_FILENAME, TEMPLATE_FILE, DS_BANDWIDTH, GRAPH_WIDTH, GRAPH_HEIGHT

import snmpQuery
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
        rrdtool.graph(self.resourceFolder + '/bw.png',
                '--start', str(startTime),
                '--end', str(endTime),
            
                '--width', GRAPH_WIDTH,
                '--height', GRAPH_HEIGHT,
                '--full-size-mode',

                '--title', 'Ancho de Banda Promedio.',
                '--vertical-label=bits/s',
                'DEF:{0}={1}:{2}:{3}'.format('bw',
                        self.resourceFolder + '/' + DB_FILENAME,
                        DS_BANDWIDTH,
                        'AVERAGE'
                    ),
                'AREA:bw#B2FF59:Ancho de Banda Promedio.'
            )

    def getAgentSysInfo(self):
        return snmpQuery.snmpWalk(
                self.agentInfo.snmpVersion,
                self.agentInfo.community,
                self.agentInfo.address,
                self.agentInfo.port,
                '1.3.6.1.2.1.1'
            )
    
    def renderHTML(self):
        sysInfo = self.getAgentSysInfo()

        # This is just because I'm rushing
        # Same story, different time
        sysDescr = sysInfo['1.3.6.1.2.1.1.1.0'].lower()
        logo = 'mine.png' # Minecraft logo fallback for the memes.
        if 'windows' in sysDescr:
            logo = 'windows.png'
        elif 'linux' in sysDescr:
            logo = 'linux.png'

        self.renderedHTML = self.template.render(
                agentOSLogo = os.path.abspath(logo),
                agentCommunity = self.agentInfo.community,
                agentSysName = sysInfo['1.3.6.1.2.1.1.5.0'],
                agentSysDescr = sysInfo['1.3.6.1.2.1.1.1.0'],
                agentSysUpTime = sysInfo['1.3.6.1.2.1.1.3.0'],
                agentSysContact = sysInfo['1.3.6.1.2.1.1.4.0'],
                agentSysLocation = sysInfo['1.3.6.1.2.1.1.6.0'],
                bwGraphFile = os.path.abspath(
                    self.resourceFolder + '/bw.png')
            )

    def makeReport(self, fileName, startTime, endTime):
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, fileName + '.pdf')
