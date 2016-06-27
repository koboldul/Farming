import smtplib
import RPi.GPIO as GPIO
from  email.mime.text import MIMEText
from private_data import PrivateData

class Mailer:
	def __init__(self):
		self.smtpObj = smtplib.SMTP

		self.url = PrivateData.SMTP_SERVER
		self.port = int(PrivateData.TLS_PORT)

	def sendStartStopMessage(self, isStart, device):
		state = 'started' if isStart else 'stopped' 
		txt = 'Device {0} was {1}'.format(device, state)
		print txt
		message = MIMEText(txt)
		message['Subject']=txt
		self.sendMail(message)

	def sendErrorMessage(self, error):
		txt = ' Errro  {0}'.format(str(error))
		message = MIMEText(txt)
		message['Subject']='ERROR'
		self.sendMail(message)

	def sendFullStopMessage(self):
		txt = 'Shutting down' 
		message = MIMEText(txt)
		message['Subject']=txt
		self.sendMail(message)

	def sendMessage(self, message):
		txt = message
		m = MIMEText(message)
		m['Suject']='FaRM BOT MESSAGE'	
		self.sendMail(m)

	def sendMail(self, message):
		message['From'] = PrivateData.MAIL_FROM
		message['To'] = PrivateData.MAIL_TO
	
		try:
			smtpObj = smtplib.SMTP(self.url, self.port)
			smtpObj.starttls()
			smtpObj.login(PrivateData.MAIL_USER_ACCOUNT, PrivateData.MAIL_PASSWORD)
			smtpObj.sendmail(PrivateData.MAIL_FROM, PrivateData.MAIL_TO, message.as_string())         
			print "Successfully sent email"
		except Exception as e:
			print e
			print "Error: unable to send email"

