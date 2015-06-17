import config

import sys
from optparse import OptionParser
import simplejson
import random

import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime


### for generating pairings

def generateChain():
    '''
    Generate a single cycle of people. The logic is really dumb, so if
    there are no possible cycles it probably recurses until stack overflow.
    '''
    chain = [random.choice(people.values())['name']]
    while len(chain) < len(people.values()):
        giver = chain[-1]
        eligible = map(lambda p: p['name'],
            filter(lambda p: giver not in p.get('block', []) and \
                giver != p['name'] and \
                p['name'] not in chain,
            people.values()))
        if not eligible:
            return generateChain()  # lazy, start over
        chain.append(random.choice(eligible))
    # make sure last and first person are compatible
    if chain[-1] in people[chain[0]].get('block', []):
        return generateChain()
    return chain

### for sending email

def send_mail(to, subject, body):
    msg = MIMEMultipart('alternative')
    msg['subject'] = subject
    msg['To'] = to
    msg['From'] = config.SENDER
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP(config.SMTP)
    server.starttls()
    server.login(config.SENDER, config.PASSWORD)
    server.sendmail(config.SENDER, [to], msg.as_string())
    server.quit()

def email_assignment(giver, recipient):
    '''my formatting for sent emails'''
    message = "Hi {0},<br>\
        Your Secret Santee is <b>{1}</b>.<br>\
        Roommates: {2}<br>\
        Address: {3}<br>\
        <br>\
        Secret Santa is on Friday, Dec 20. God be with ye.<br>\
        <br>\
        This message is automatically generated, do not respond."
    message = message.format(
        giver['name'], recipient['name'],
        recipient.get('roommates', ''),
        recipient.get('address', '')
        )
    send_mail(giver['email'], "Secret Santa assignment", message)

### go

if __name__ == "__main__":
    parser = OptionParser(usage = "usage: %prog [options] <input>")
    parser.add_option("--fake",
                      dest="fake", default=False, action="store_true",
                      help=("Do a fake run -- generate a cycle without "
                            "actually sending emails."))
    (options, args) = parser.parse_args()

    if len(args)==0:
        raise Exception("No input provided; please specify a valid JSON file.")

    # load people info
    f = open(args[0],'r')
    global people
    people = simplejson.loads(f.read())
    for name, person in people.iteritems():
      people[name]['name'] = name

    # make blacklisting bidirectional
    for name, person in people.iteritems():
      for blockee_name in person.get('block', []):
        if blockee_name in people:
          people[blockee_name]['block'] = (
            people[blockee_name].get('block', []) + [name])

    # email each member of chain
    chain = generateChain()
    for i,giver_name in enumerate(chain):
        recipient_name = chain[(i+1)%len(chain)]
        if not options.fake:
            email_assignment(people['giver_name'], people['recipient_name'])
            print 'Sending email %d' % i
    if options.fake:
        print chain
