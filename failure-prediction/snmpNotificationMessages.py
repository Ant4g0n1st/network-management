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
                rrdConstants.HW_GRAPH
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

class FailureMessage(GenericMessage):

    def __init__(self, agent):
        super().__init__(agent)

    def composeMessage(self):
        super(FailureMessage, self).composeMessage()

        sysInfo = self.getAgentSysDescr()

        subject = 'Alerta de Trafico de Red en {0} - Victor A Noriega Morales.'
        subject = subject.format(sysInfo['1.3.6.1.2.1.1.5.0'])

        self.message['Subject'] = subject       

        text = """
                Hola,

                Uno de los dispositivos ha experimentado un comportamiento anomalo en su trafico de red.

                Estos son los detalles del agente:
                
                - Descripcion: {0}
                - Uptime : {1}
                - Contacto : {2}
                - Nombre : {3}
                - Ubicacion : {4}

                - Direccion IP : {5}
                - Comunidad SNMP : {6}
                - Puerto SNMP : {7}

                Hemos incluido una grafica del ancho de banda en el correo.
                Se recomienda revisar el dispositivo.
            """
        text = text.format(sysInfo['1.3.6.1.2.1.1.1.0'],
            sysInfo['1.3.6.1.2.1.1.3.0'],
            sysInfo['1.3.6.1.2.1.1.4.0'],
            sysInfo['1.3.6.1.2.1.1.5.0'],
            sysInfo['1.3.6.1.2.1.1.6.0'],
            self.agent.address,
            self.agent.community,
            self.agent.port)

        self.message.attach(MIMEText(text, 'plain'))

