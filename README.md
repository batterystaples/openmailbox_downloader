# openmailbox_downloader
Save a local copy of your openmailbox emails without using IMAP

## Motivation
On 5th August 2017, [openmailbox.org](https://openmailbox.org) changed its service by requiring people to pay for IMAP. No warning was given for this, and I have not been able to find a simple way to download all of my emails from the server.

## Dependencies
For this tool to work, you need to install Python 3, and the module listed in requirements.txt.

If you have pip installed, you can do this with the command:
`pip3 install -r requirements.txt`

## How this tool works
To use this tool, you need to [log in to openmailbox's webmail](https://app.openmailbox.org/login).

Then, you will need to view the cookies that openmailbox has put on your computer. In particular, you will need to find the _sessionid_ and the _csrftoken_.

Then, you need to run this command:
`./uidextract.py <csrftoken> <sessionid> <mailbox> <lowerbound> <upperbound>`

where _csrftoken_ and _sessionid_ are the two cookies you found earlier, mailbox is the folder you want to download from (usually 'INBOX') and lowerbound and upperbound are the lowest and highest number messages you want respectively.

You can list your mailboxes (folders) using this command:
`./uidextract.py <csrftoken> <sessionid>`

Note that you can only download a maximum of 500 messages each time you run this script. So, if you have more than 500 messages in a folder, you will have to run it multiple times, changing the upperbound and lowerbound values on each run.

The saved emails will be in the folder `emails_output_dir`.  The format will be `<mailbox_name>-<uid>.eml`.

If the script gets interrupted, the script tries to start from where it left off so you don't have to redownload emails that you have already downloaded.

## Examples

`./uidextract.py eri17r6toiughw3rtg9bv3qcf8o34nqt9y n9o34yqto783bn34yrf3cyo834ytn843qtc3hvukerhgliurhgoi243 INBOX 1 500`

Downloads the first 500 messages from INBOX
