from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class MailSender:
    """sending emails using SMTP with login credentials."""
    def __init__(self,email,password):
        self.email = email
        self.password = password

    def prepare_email(self,message):
        """Creating the email message."""
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = self.email
        msg['Data'] = "Data" 
        msg.attach(MIMEText(message,'plain')) 
        return msg

    def sendmail(self, message):
        """Sends the prepared email using Gmail's SMTP server."""
        msg = self.prepare_email(message)
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
                print("Email with scraped Javascript and CSS files have been sent!")
        except Exception as e:
            print("Failed to send email:", e)
