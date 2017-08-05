#!/usr/bin/python3

import sys
import os
import json
from urllib import request

if len(sys.argv) != 6:
	print("Syntax: ./uidextract.py <csrftoken> <sessionid> <mailbox> <lowerbound> <upperbound>")
	exit()

csrftoken = sys.argv[1]
sessionid = sys.argv[2]
mailbox = sys.argv[3]
lowerbound = int(sys.argv[4])
upperbound = int(sys.argv[5])

if upperbound <= lowerbound:
	print("The lower bound must be less than than the upper bound")
	exit()

if upperbound - lowerbound > 500:
	print("The difference between the upper bound and the lower bound must be less than or equal to 500.")
	exit()

print("Getting list of emails")
mdatareq = request.Request('https://app.openmailbox.org/requests/webmail?range='+str(lowerbound)+'-'+str(upperbound)+'&sort=date&order=0&selected=&action=maillist&mailbox='+mailbox)
mdatareq.add_header('Cookie', 'csrftoken='+csrftoken+'; sessionid='+sessionid)
mdataresp = request.urlopen(mdatareq)
metadata = json.loads(mdataresp.read().decode('utf-8'))
uids = []
for line in metadata['partial_list']:
	uids.append(line['uid'])
print("Finished getting list of emails")

os.makedirs('emails_output_dir', exist_ok=True)
print("Created directory emails_output_dir if it didn't already exist")

for uid in uids:
	req = request.Request('https://app.openmailbox.org/requests/webmail?mailbox='+mailbox+'&uid='+str(uid)+'&action=downloadmessage')
	req.add_header('Cookie', 'csrftoken='+csrftoken+'; sessionid='+sessionid)
	resp = request.urlopen(req)

	output = open("emails_output_dir/"+str(uid)+".eml",'w')
	output.write(resp.read().decode('utf-8'))
	output.close()
	print("Saved message " + str(uid))
