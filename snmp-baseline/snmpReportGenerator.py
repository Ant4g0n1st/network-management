from appConstants import DB_FILENAME, TEMPLATE_FILE

import rrdConstants
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
    
    def renderGraphs(self, startTime, endTime):
        return

    # This is just because I'm rushing
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
                memoryGraphFile = os.path.abspath(
                    self.resourceFolder + '/' + rrdConstants.MEMORY_GRAPH),
                diskGraphFile = os.path.abspath(
                    self.resourceFolder + '/' + rrdConstants.DISK_GRAPH),
                cpuGraphFile = os.path.abspath(
                    self.resourceFolder + '/' + rrdConstants.CPU_GRAPH)
            )

    def makeReport(self, fileName, startTime, endTime):
        self.renderGraphs(startTime, endTime)
        self.renderHTML()
        pdfkit.from_string(self.renderedHTML, fileName + '.pdf')

