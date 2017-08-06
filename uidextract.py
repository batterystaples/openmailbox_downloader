#!/usr/bin/python3

import sys
import os
import json
import requests
from requests.packages.urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


def get_emails(csrftoken, sessionid, mailbox, lowerbound, upperbound):
    print("Getting list of emails")
    # Create a session object from requests library
    s = requests.Session()
    retries = Retry(total=10, backoff_factor=1,
                    status_forcelist=[500, 502, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.headers.update({'Cookie': 'csrftoken={0};'
                      'sessionid={1}'.format(csrftoken, sessionid)})
    mdatareq = 'https://app.openmailbox.org/requests/webmail?range={0}-{1}&sort=date&order=0&selected=&action=maillist&mailbox={2}'.format(lowerbound, upperbound, mailbox)
    print(mdatareq)

    metadata = json.loads(s.get(mdatareq).text)
    print(metadata)
    uids = []
    for line in metadata['partial_list']:
        uids.append(line['uid'])
    print("Finished getting list of emails")

    os.makedirs('emails_output_dir', exist_ok=True)
    print("Created directory emails_output_dir if it didn't already exist")

    for uid in uids:
        if not os.path.isfile('emails_output_dir/' + str(uid) + ".eml"):
            req = 'https://app.openmailbox.org/requests/webmail?mailbox={0}&uid={1}&action=downloadmessage'.format(mailbox, str(uid))
            resp = s.get(req, stream=True)
            with open('emails_output_dir/' + str(uid) + '.eml', 'wb') as eml:
                for chunk in resp:
                    eml.write(chunk)
            print("Saved message " + str(uid))
        else:
            print("Already downloaded " + str(uid))

def list_folders(csrftoken, sessionid):
    print("Getting list of folders")
    # Create a session object from requests library
    s = requests.Session()
    retries = Retry(total=10, backoff_factor=1,
                    status_forcelist=[500, 502, 504])
    s.mount('https://', HTTPAdapter(max_retries=retries))
    s.headers.update({'Cookie': 'csrftoken={0};'
                      'sessionid={1}'.format(csrftoken, sessionid)})
    mdatareq = 'https://app.openmailbox.org/requests/webmail?action=folderlist'
    print(mdatareq)

    metadata = json.loads(s.get(mdatareq).text)
    print(metadata)

    print('\nFolder names:')
    for line in metadata['folders']:
        print(line['name'])

if __name__ == '__main__':
    if len(sys.argv) == 3:
        csrftoken = sys.argv[1]
        sessionid = sys.argv[2]

        list_folders(csrftoken, sessionid)

    elif len(sys.argv) == 6:
        csrftoken = sys.argv[1]
        sessionid = sys.argv[2]
        mailbox = sys.argv[3]
        lowerbound = sys.argv[4]
        upperbound = sys.argv[5]

        if int(upperbound) <= int(lowerbound):
            print("The lower bound must be less than than the upper bound")
            exit()
        if int(upperbound) - int(lowerbound) > 500:
            print('The difference between the upper bound and the lower'
                  'bound must be less than or equal to 500.')
            exit()

        get_emails(csrftoken, sessionid, mailbox, lowerbound, upperbound)

    else:
        print('Syntax:')
        print('For listing folders\n\t./uidextract.py <csrftoken> <sessionid> ')
        print('For getting emails\n\t./uidextract.py <csrftoken> <sessionid> <mailbox> <lowerbound> <upperbound>')
        exit()
