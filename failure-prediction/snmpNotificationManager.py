from appConstants import ALERT_COOLDOWN

import snmpNotificationMessages as msgs

import appConstants
import time

class SnmpNotificationManager:
    
    def __init__(self, agent):
        self.pending = False
        self.agent = agent
        self.last = 0

    def sendNotification(self):
        # Test if the notification cooldown is over.
        now = int(time.time())
        if now - self.last < ALERT_COOLDOWN:
            self.pending = True

        # Send the notification.
        msg = msgs.FailureMessage(self.agent)
        msg.sendMessage()

        self.pending = False
        self.last = now

    def flushPending(self):
        if self.pending:
            self.sendNotification()

