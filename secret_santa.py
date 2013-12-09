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
# global people

def person(name):
    return filter(lambda p:name==p['name'], people)[0]

def randName(people_set):
    return people_set[random.randint(0,len(people_set)-1)]['name']

def generateChain():
    '''Generate a single cycle of people. The algorithm is dumb, so if there
       are no possible cycles it probably recurses until stack overflow.'''
    chain = [randName(people)]
    while len(chain) < len(people):
        giver = chain[-1]
        eligible = filter(
            lambda p: giver not in p.get('dont_receive',[]) and \
                giver != p['name'] and \
                p['name'] not in chain,
            people)
        if not eligible:
            return generateChain()  # lazy, start over
        chain.append(randName(eligible))
    # make sure last and first person are compatible
    if chain[-1] in person(chain[0]).get('dont_receive',[]):
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
        recipient['address']
        )
    send_mail(giver['email'], "Secret Santa assignment", message)

### go

if __name__ == "__main__":
    parser = OptionParser(usage = "usage: %prog [options] <input>")
    parser.add_option("-f", "--fake",
                      dest="fake", default=False, action="store_true",
                      help="Do a fake run -- generate a cycle without actually sending emails.")
    (options, args) = parser.parse_args()

    if len(args)==0:
        raise Exception("No input provided; please specify a valid JSON file.")

    # read people JSON
    f = open(args[0],'r')
    global people
    people = simplejson.loads(f.read())

    # email each member of chain
    chain = generateChain()
    for i,giver_name in enumerate(chain):
        recipient_name = chain[(i+1)%len(chain)]
        if not options.fake:
            email_assignment(person(giver_name), person(recipient_name))
    if options.fake:
        print chain

