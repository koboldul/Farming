import smtplib
import RPi.GPIO as GPIO
from  email.mime.text import MIMEText
from private_data import PrivateData

class Mailer:
	def __init__(self):
		self.smtpObj = smtplib.SMTP

		self.url = PrivateData.SMTP_SERVER
		self.port = int(PrivateData.TLS_PORT)

	def send_message(self, message, subject):
		m = MIMEText(message)
		m['Suject']= subject	
		self.send_mail(m)

	def send_mail(self, message):
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

