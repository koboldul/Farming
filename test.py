import smtplib

smtpObj = smtplib.SMTP

passW = 'Malevich1@3$'
acc = 'koboldul@yahoo.com'
to = 'koboldul@gmail.com'
url = 'smtp.mail.yahoo.com'
port = 587

message = """\
        From: %s
        To: %s
        Subject: %s
        %s
        """ % (acc, ", ".join(to), 'sbj', 'mergeee')
# me == the sender's email address
# you == the recipient's email address

try:
	smtpObj = smtplib.SMTP(url, port)
	smtpObj.starttls()
	smtpObj.login(acc, passW)
	smtpObj.sendmail(acc, to, message)         
	print "Successfully sent email"
except Exception as e:
	print e
	print "Error: unable to send email"

