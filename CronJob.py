#!/usr/bin/python

from emails import email_read
import json
import os
import sys
import imaplib
from file_share import mail_file
import csv

imap_url ='imap.gmail.com'
my_mail = imaplib.IMAP4_SSL(imap_url)
#get json
"""
freq = {"days": None, "hours" : None, "minutes" : None}

Rmail = None

with open('usepass.csv', 'w') as f:
    json.dump(data, f)
"""
usepass = {}
Rmail = ""
freq = ""
def Config():
    global usepass,Rmail,freq
    data = ""
    x=5
    while x!=0:
        x = input("1:Set Up Script\n2:Update Script\n0:Exit: ")
        if x=='0':
            break
        elif x=='1':
            usepass={}
            Rmail=input("Receiver Email: ")
            users = input("Enter User Emails: ").split()
            passw =input("Enter User Passwords: ").split()
            freq = input("minute hour dayofmonth month dayofweek: ")
            for i in range(len(users)):
                usepass[users[i]] = passw[i]
            print(usepass)
        elif x=='2':
            ch = input("1:Add User\n2:Update Frequency\n3:Update Receiver Email\n0:Exit: ")
            if ch=='0':
                break
            elif ch=='1':
                user = input("Enter Email: ")
                usepass[user] = input("Enter Password: ")
            elif ch =='2':
                freq = input("minute hour dayofmonth month dayofweek: ")
            elif ch=='3':
                Rmail=input("Receiver Email: ")
    with open("cronrmail.txt",'w') as f:
        f.write(Rmail)
    with open("cronusers.txt",'w') as f:
        for line in usepass.keys():
            data += line.strip()+","
        f.write(data)
    data = ""
    with open("cronpasswords.txt",'w') as f:
        for line in usepass.values():
            data += line.strip()+","
        f.write(data)
    with open("cronfreq.txt",'w') as f:
        f.write(freq)

with open("cronrmail.txt",'r') as f:
    Rmail = f.readline().strip()
with open("cronusers.txt",'r') as f:
    users = f.readline()[:-1].split(",")
with open("cronpasswords.txt",'r') as f:
    passw = f.readline()[:-1].split(",")
for i in range(len(users)):
    usepass[users[i].strip()] = passw[i].strip()
with open("cronfreq.txt",'r') as f:
    freq = f.readline().strip()
if len(sys.argv)<2:
    Config()
print(freq,usepass,Rmail)
input()
csvls = []
os.system("sudo crontab -l > mycron")
os.system("sudo echo \""+freq+" ./CronJob.py 1\" > mycron")
os.system("sudo crontab mycron")
os.system("sudo rm mycron")

for i in usepass.keys():
    my_mail = imaplib.IMAP4_SSL(imap_url)
    password = usepass[i]
    csvls.append(email_read(my_mail,i,password))

#4:Email Class Normal, 10:AttachmentClass not_cyberbullying
sus = []
check = ["Sender", "Subject", "Email Body", "Email Datetime", "Email Class", "Attachment Type", "Filepath", "Password", "Malware?", "Attachment Summary", "Class Of Attachment","Ranking"]
for fil in csvls:
    with open(fil,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row == check:
                continue
            if row[4].strip() != "Normal":
                sus.append(row)

if sus!= []:
    with open('Sus.csv','w') as f:
        writer = csv.writer(f)
        writer.writerows(sus)
    mail_file('Sus.csv',Rmail)


