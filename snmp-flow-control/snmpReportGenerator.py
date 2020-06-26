import appConstants
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

        self.template = templateEnv.get_template(appConstants.TEMPLATE_FILE)
    
    # This has to be cleaner.
    def renderGraphs(self, startTime, endTime):
        rrdtool.graph('{0}/{1}.svg'.format(
                        self.resourceFolder,
                        appConstants.DS_INBW
                    ),

                '--imgformat', 'SVG',
                '--start', str(startTime),
                '--end', str(endTime),
            
                '--width', appConstants.GRAPH_WIDTH,
                '--height', appConstants.GRAPH_HEIGHT,
                '--full-size-mode',

                '--title', 'Octetos de Entrada.',
                '--vertical-label=bits/s',

                'DEF:{0}={1}:{2}:{3}'.format('bw',
                        self.resourceFolder + '/' + appConstants.DB_FILENAME,
                        appConstants.DS_INBW,
                        'AVERAGE'
                    ),

                'CDEF:lim=bw,0,' + appConstants.MAX_INBW + ',LIMIT',
                'CDEF:over=lim,UN,1,0,IF',

                'TICK:over#FFEB3B:1.0:  Excesos',
                'AREA:bw#B2FF59:Ancho de Banda de Entrada.', 
                'HRULE:' + appConstants.MAX_INBW + '#FF0000:MaxInBw'
            )
        rrdtool.graph('{0}/{1}.svg'.format(
                        self.resourceFolder,
                        appConstants.DS_OUTBW
                    ),

                '--imgformat', 'SVG',
                '--start', str(startTime),
                '--end', str(endTime),
            
                '--width', appConstants.GRAPH_WIDTH,
                '--height', appConstants.GRAPH_HEIGHT,
                '--full-size-mode',

                '--title', 'Octetos de Salida.',
                '--vertical-label=bits/s',

                'DEF:{0}={1}:{2}:{3}'.format('bw',
                        self.resourceFolder + '/' + appConstants.DB_FILENAME,
                        appConstants.DS_OUTBW,
                        'AVERAGE'
                    ),

                'CDEF:lim=bw,0,' + appConstants.MAX_OUTBW + ',LIMIT',
                'CDEF:over=lim,UN,1,0,IF',

                'TICK:over#FFEB3B:1.0:  Excesos',
                'AREA:bw#40C4FF:Ancho de Banda de Salida.',
                'HRULE:' + appConstants.MAX_OUTBW + '#FF0000:MaxOutBw'
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
                inBwGraphFile = os.path.abspath(
                        '{0}/{1}.png'.format(
                            self.resourceFolder,
                            appConstants.DS_INBW)
                    ),
                outBwGraphFile = os.path.abspath(
                        '{0}/{1}.png'.format(
                            self.resourceFolder,
                            appConstants.DS_OUTBW)
                    )
            )

    def makeReport(self, fileName, startTime, endTime):
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, fileName + '.pdf')
