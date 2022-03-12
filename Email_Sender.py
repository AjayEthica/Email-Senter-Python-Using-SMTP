import smtplib
import configparser
import os,time
import random
from multiprocessing.dummy import Pool as ThreadPool
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
from email.utils import formataddr
from email import encoders
from colorama import init, Fore, Style
init(autoreset=True)

fc = Fore.CYAN
fg = Fore.GREEN
fw = Fore.WHITE
fr = Fore.RED
fb = Fore.BLUE
fy = Fore.YELLOW
fm = Fore.MAGENTA
sn = Style.NORMAL
sb = Style.BRIGHT

config = configparser.ConfigParser()#(interpolation=None)
config.read("config.ini")

SmtpHost = config.get('smtp', 'SmtpHost')
SmtpUser = config.get('smtp', 'SmtpUser')
SmtpPassword = config.get('smtp', 'SmtpPassword')
SmtpEmail = config.get('smtp', 'SmtpEmail')
wait = config.get('smtp', 'TimeWait')
FromNames = open("FromNames.txt","r").read().splitlines()
Subjects = open("Subjects.txt","r").read().splitlines()
print(" SmtpHost: "+sb+fg+SmtpHost)
print(" HostUser: "+sb+fg+SmtpUser)
print(" HostPassword: "+sb+fg+SmtpPassword)
print(" HostEmail: "+sb+fg+SmtpEmail)

no = 0
def send(smail):
    global no
    no+=1
    username = SmtpUser
    password = SmtpPassword
    mail_subject = random.choice(Subjects)
    From = random.choice(FromNames)
    mail_body =  open('letter.html','r').read()
    mimemsg = MIMEMultipart()
    mimemsg['From']= formataddr((str(Header(From, 'utf-8')), SmtpEmail))
    mimemsg['To']= smail
    mimemsg['Subject']=mail_subject
    mimemsg.attach(MIMEText(mail_body, 'html'))
    connection = smtplib.SMTP(host=SmtpHost, port=587)
    connection.starttls()
    connection.login(username,password)
    connection.send_message(mimemsg)
    connection.quit()
    print(sb+fg+" Sent SuccessFully | "+sb+fy+str(no)+" | "+sb+fc+smail)
    fp = open("log.txt","a")
    fp.write("Sned Successfull : "+smail+"\n")
    fp.close()

#==============================================

leads = open("Leads.txt","r").read().splitlines()
for mail in leads:
    time.sleep(int(wait))
    try:
        send(mail)
    except:
        print(sb+fr+"  \n Some Error Ocurred | ...")
        fp = open("log.txt","a")
        fp.write("Failed to send at this address : "+mail+"\n")
        fp.close()
