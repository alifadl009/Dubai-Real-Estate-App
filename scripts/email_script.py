import dotenv
import os
from email.message import EmailMessage
import smtplib


def send_email(subject, message):
    try:
        dotenv.load_dotenv()

        email = os.getenv('EMAIL')
        password = os.getenv('PASSWORD')
        receiver = os.getenv('RECIPIENT')
        server = os.getenv('SERVER')
        port = os.getenv('PORT')

        msg = EmailMessage()
        msg.set_content(message)

        msg['Subject'] = subject
        msg['FROM'] = email
        msg['To'] = receiver

        server = smtplib.SMTP('smtp.gmail.com', port=port)
        server.starttls()
        server.login(user=email, password=password)
        server.send_message(msg)
        server.quit()
        print(f"Email sent successfully to {receiver}")
        
    except Exception as e:
        print(f"Failed to send email. Error: {str(e)}")
