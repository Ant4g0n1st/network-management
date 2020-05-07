import appConstants
import logging

import telnetlib
import ftplib
import sys

class FTPClient:

    def __init__(self, address):
        self.client = ftplib.FTP(address)
        self.client.login(appConstants.RCP_USER,
            appConstants.RCP_PASS)
        
    def getFile(self, srcPath, dstPath):
        f = open(dstPath, 'wb')
        self.client.retrbinary('RETR ' + srcPath, f.write)
        f.close()

    def putFile(self, srcPath, dstPath):
        f = open(srcPath, 'rb')
        self.client.storbinary('STOR ' + dstPath, f)
        f.close()

    def deleteFile(self, fileName):
        self.client.retrbinary(fileName)

    def close(self):
        self.client.quit()

class TelnetClient:

    # Telnet is pretty messy, but useful.
    def __init__(self, address):
        self.client = telnetlib.Telnet(address)
        
        self.client.read_until(b'User: ')
        self.client.write(appConstants.RCP_USER.encode('ascii') + b'\n')

        self.client.read_until(b'Password: ')
        self.client.write(appConstants.RCP_PASS.encode('ascii') + b'\n')

        self.client.read_until(b'>')
        self.client.write(b'enable\n')

    def writeCommand(self, command):
        self.client.read_until(b'#')
        self.client.write(command.encode('ascii') + b'\n')

    def close(self):
        self.client.read_until(b'#')
        self.client.write(b'exit\n')
        self.client.read_all()
        self.client.close()

class ConfigurationManager:

    def __init__(self, agent):
        self.resourceFolder = agent.getIdentifier()
        self.agent = agent

    def restoreConfiguration(self):
        try:
            ftp = FTPClient(self.agent.address) 
            ftp.deleteFile(appConstants.CONFIG_FILE)
            ftp.putFile(self.resourceFolder + '/' + appConstants.CONFIG_FILE,
                appConstants.CONFIG_FILE)
            ftp.close()
            return True
        except:
            logging.error('Exception restoring configuration of %s : %s',
                self.agent, sys.exc_info())
        return False

    def backupConfiguration(self):
        try:
            ftp = FTPClient(self.agent.address) 
            ftp.getFile(appConstants.CONFIG_FILE,
                self.resourceFolder + '/' + appConstants.CONFIG_FILE)
            ftp.close()
            return True
        except:
            logging.error('Exception backing up configuration of %s : %s',
                self.agent, sys.exc_info())
        return False
       
    def dumpConfiguration(self):
        try:
            telnet = TelnetClient(self.agent.address)
            telnet.writeCommand('copy run start')
            telnet.close()
            return True
        except:
            logging.error('Exception dumping configuration of %s : %s',
                self.agent, sys.exc_info())
        return False

