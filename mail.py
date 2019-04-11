import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage

# Resimlerin yollanacagi mail adresi (Yalniz Gmail ile calisir.)
emailAdres = 'iskenderuzuner@gmail.com'
emailSifre = 'iSko42520312031'

# Guncellemeyi gondermek istediginiz e-posta
gidecekEmail = 'iskenderuzuner@gmail.com'

def sendEmail(image):
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Guvenlik Uyarisi'
	msgRoot['From'] = emailAdres
	msgRoot['To'] = gidecekEmail
	msgRoot.preamble = 'Raspberry pi guvenlik kamera guncellemesi'

	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)
	msgText = MIMEText('Akilli guvenlik kamerasi nesne buldu')
	msgAlternative.attach(msgText)

	msgText = MIMEText('<img src="cid:image1">', 'html')
	msgAlternative.attach(msgText)

	msgImage = MIMEImage(image)
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	smtp = smtplib.SMTP('smtp.gmail.com', 587)
	smtp.starttls()
	smtp.login(emailAdres, emailSifre)
	smtp.sendmail(emailAdres, gidecekEmail, msgRoot.as_string())
	smtp.quit()

