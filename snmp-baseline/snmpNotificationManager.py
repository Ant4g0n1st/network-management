import appConstants
import time

class SnmpNotificationManager:
    
    def __init__(self, agent):
        self.readyPending = False
        self.setPending = False
        self.goPending = False

        self.agent = agent

        self.lastReady = 0
        self.lastSet = 0
        self.lastGo = 0

    def flushPending(self):
        if self.goPending:
            if self.sendGoNotification():
                self.readyPending = False
                self.setPending = False

        if self.setPending:
            if self.sendSetNotification():
                self.readyPending = False 

        if self.readyPending:
            self.sendReadyNotification()

    def sendReadyNotification(self):
        now = int(time.time())
        if now - self.lastReady < appConstants.ALERT_TIMEOUT:
            self.readyPending = True
            return False 
        print('Ready : ', self.agent)
        self.readyPending = False
        self.lastReady = now
        return True

    def sendSetNotification(self):
        now = int(time.time())
        if now - self.lastSet < appConstants.ALERT_TIMEOUT:
            self.setPending = True
            return False 
        print('Set: ', self.agent)
        self.setPending = False
        self.lastSet = now
        return True

    def sendGoNotification(self):
        now = int(time.time())
        if now - self.lastGo < appConstants.ALERT_TIMEOUT:
            self.goPending = True
            return False 
        print('Go : ', self.agent)
        self.goPending = False
        self.lastGo = now
        return True

