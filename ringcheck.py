import os
import sys
import ConfigParser
from twilio.rest import TwilioRestClient

config = ConfigParser.RawConfigParser()
config.read([os.path.expanduser("~/.twilio.conf")])
account_sid = config.get('twilio', 'account_sid')
auth_token = config.get('twilio', 'auth_token')
phone_number = config.get('twilio', 'phone_number')
call_sound_url = config.get('twilio', 'call_sound_url')

class Ringcheck(object):

    def __init__(self):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.client = TwilioRestClient(self.account_sid, self.auth_token)

    def check_number(self, number):
        try:
            c = self.client.calls.create(to=number, from_=phone_number, url=call_sound_url)
        except:
            # invalid phone number
            return None

        while True:
            c.update_instance()
            if c.status != c.QUEUED:
                c.cancel()
                c.hangup()
                break
        return c

if __name__ == "__main__":
    ringcheck = Ringcheck()
    c = ringcheck.check_number(sys.argv[1])
    if not c:
        print "The phone number you attempted to dial (%s) is invalid." % (sys.argv[1])
        sys.exit(1)
    else:
        active = "in an unknown state"
        if c.status in [c.RINGING, c.IN_PROGRESS, c.COMPLETED, c.NO_ANSWER]:
            active = "in service"
        elif c.status == c.BUSY:
            active = "busy"
        elif c.status == c.FAILED:
            active = "not in service"
        print "The phone number you dialed (%s) is %s. (Status: %s)" % (sys.argv[1], active, c.status)

