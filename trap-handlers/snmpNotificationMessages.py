from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import snmpQuery as snmp
import smtplib

class GenericMessage:
    
    def __init__(self, agent, trap):
        self.root = agent.getIdentifier()
        self.message = MIMEMultipart()
        self.agent = agent
        self.trap = trap

        self.loadCredentials()
        self.loadRecipients()
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

class LinkDownMessage(GenericMessage):

    def __init__(self, agent, trap):
        super().__init__(agent, trap)

    def composeMessage(self):
        super(LinkDownMessage, self).composeMessage()

        sysInfo = self.getAgentSysDescr()

        subject = 'Victor A Noriega Morales - linkDown en {0}'
        subject = subject.format(self.trap['agentAddress'])

        self.message['Subject'] = subject       

        text = """
                Hola,

                    Este es un correo para informarte que la interfaz {0} en {1} [{2}] ha cambiado su estado a DOWN.
                    Ha llegado una trap al servidor {8} por el puerto {9}.

                    Estos son los detalles del agente:

                    - Descripcion : {3}
                    - Uptime : {4}
                    - Contacto : {5}
                    - Nombre : {6}
                    - Ubicacion : {7}

                    Recomendamos revisar el dispositivo.
            """

        text = text.format(self.trap['ifDescr'],
            sysInfo['1.3.6.1.2.1.1.5.0'],
            self.trap['agentAddress'],
            sysInfo['1.3.6.1.2.1.1.1.0'],
            sysInfo['1.3.6.1.2.1.1.3.0'],
            sysInfo['1.3.6.1.2.1.1.4.0'],
            sysInfo['1.3.6.1.2.1.1.5.0'],
            sysInfo['1.3.6.1.2.1.1.6.0'],
            self.trap['serverAddress'],
            self.trap['serverPort'])

        self.message.attach(MIMEText(text, 'plain'))

class LinkUpMessage(GenericMessage):

    def __init__(self, agent, trap):
        super().__init__(agent, trap)

    def composeMessage(self):
        super(LinkUpMessage, self).composeMessage()

        sysInfo = self.getAgentSysDescr()

        subject = 'Victor A Noriega Morales - linkUp en {0}'
        subject = subject.format(self.trap['agentAddress'])

        self.message['Subject'] = subject       

        text = """
                Hola,

                    Este es un correo para informarte que la interfaz {0} en {1} [{2}] ha cambiado su estado a UP.
                    Ha llegado una trap al servidor {8} por el puerto {9}.

                    Estos son los detalles del agente:

                    - Descripcion : {3}
                    - Uptime : {4}
                    - Contacto : {5}
                    - Nombre : {6}
                    - Ubicacion : {7}

                    Recomendamos revisar el dispositivo.
            """

        text = text.format(self.trap['ifDescr'],
            sysInfo['1.3.6.1.2.1.1.5.0'],
            self.trap['agentAddress'],
            sysInfo['1.3.6.1.2.1.1.1.0'],
            sysInfo['1.3.6.1.2.1.1.3.0'],
            sysInfo['1.3.6.1.2.1.1.4.0'],
            sysInfo['1.3.6.1.2.1.1.5.0'],
            sysInfo['1.3.6.1.2.1.1.6.0'],
            self.trap['serverAddress'],
            self.trap['serverPort'])

        self.message.attach(MIMEText(text, 'plain'))

