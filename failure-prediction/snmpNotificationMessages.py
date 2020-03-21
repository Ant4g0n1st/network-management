from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import snmpQuery as snmp
import rrdConstants
import smtplib

class GenericMessage:
    
    def __init__(self, agent):
        self.root = agent.getIdentifier()
        self.message = MIMEMultipart()
        self.agent = agent

        self.loadCredentials()
        self.loadRecipients()
        self.attachGraphs()
        self.composeMessage()

    def loadCredentials(self):
        f = open('credentials.txt', 'r')
        tokens = f.read().strip().split()

        self.password = tokens[-1]
        self.user = tokens[0]

        f.close()

    def loadRecipients(self):
        f = open('recipients.txt', 'r')

        self.recipient = f.read().strip()

        f.close()

    def attachGraphs(self):
        graphFiles = [
                #rrdConstants.MEMORY_GRAPH,
                #rrdConstants.DISK_GRAPH,
                rrdConstants.CPU_GRAPH
            ]
        
        for fileName in graphFiles:
            f = open(self.root + '/' + fileName, 'rb')
            img = MIMEImage(f.read())
            self.message.attach(img)
            f.close()

    def getAgentSysDescr(self):
        return snmp.snmpWalk(
                self.agent.snmpVersion,
                self.agent.community,
                self.agent.address,
                self.agent.port,
                '1.3.6.1.2.1.1'
            )

    def composeMessage(self):
        self.message['To'] = self.recipient
        self.message['From'] = self.user

    def sendMessage(self):
        serverAddress = 'smtp.gmail.com:587'

        smtpServer = smtplib.SMTP(serverAddress)
        smtpServer.starttls()

        smtpServer.login(self.user, self.password)

        smtpServer.sendmail(self.user, 
            self.recipient, self.message.as_string())

        smtpServer.quit()

class GoMessage(GenericMessage):

    def __init__(self, agent):
        super().__init__(agent)

    def composeMessage(self):
        super(GoMessage, self).composeMessage()

        sysInfo = self.getAgentSysDescr()

        subject = 'Victor Alberto Noriega Morales - Alerta GO para '
        subject += sysInfo['1.3.6.1.2.1.1.5.0']

        self.message['Subject'] = subject       

        text = """
                Hola, éste es un correro respecto al desempeño del dispositivo {0}.
                Es importante que ejecutes un plan de acción ya que el rendimiento 
                del dispositivo ha superado el tercer umbral de alerta.
            """.format(sysInfo['1.3.6.1.2.1.1.1.0'])

        self.message.attach(MIMEText(text, 'plain'))

class SetMessage(GenericMessage):

    def __init__(self, agent):
        super().__init__(agent)

    def composeMessage(self):
        super(SetMessage, self).composeMessage()

        sysInfo = self.getAgentSysDescr()

        subject = 'Victor Alberto Noriega Morales - Alerta SET para '
        subject += sysInfo['1.3.6.1.2.1.1.5.0']

        self.message['Subject'] = subject       

        text = """
                Hola, éste es un correro respecto al desempeño del dispositivo {0}.
                Su rendimiento ha superado el segundo umbral de alerta,
                es el momento para comenzar a formular un plan de acción.
            """.format(sysInfo['1.3.6.1.2.1.1.1.0'])

        self.message.attach(MIMEText(text, 'plain'))

class ReadyMessage(GenericMessage):

    def __init__(self, agent):
        super().__init__(agent)

    def composeMessage(self):
        super(ReadyMessage, self).composeMessage()

        sysInfo = self.getAgentSysDescr()

        subject = 'Victor Alberto Noriega Morales - Alerta READY para '
        subject += sysInfo['1.3.6.1.2.1.1.5.0']

        self.message['Subject'] = subject       

        text = """
                Hola, éste es un correo respecto al desempeño del dispositivo {0}. 
                Ha superado el primer umbral de alerta,
                te recomendamos que investigues más al respecto.
            """.format(sysInfo['1.3.6.1.2.1.1.1.0'])

        self.message.attach(MIMEText(text, 'plain'))
