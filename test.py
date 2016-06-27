import smtplib
import RPi.GPIO as GPIO
from  email.mime.text import MIMEText

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(17, GPIO.IN)
#print GPIO.input(17)

smtpObj = smtplib.SMTP

passW = 'sendSomeMails1'
acc = 'koboldul@sendgrid.com'
to = 'koboldul@gmail.com'
url = 'smtp.sendgrid.net'
port = int(587)

message = MIMEText('mmmmmmm')
message['Subject']='weather bot'
message['From']='farmbot@sendgrid.com'
message['To']='koboldul@gmail.com'


try:
	smtpObj = smtplib.SMTP(url, port)
	smtpObj.starttls()
	smtpObj.login('koboldul', passW)
	smtpObj.sendmail(acc, to, message.as_string())         
	print "Successfully sent email"
except Exception as e:
	print e
	print "Error: unable to send email"

