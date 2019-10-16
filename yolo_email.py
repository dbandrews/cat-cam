from yolo_func import yolo_swag
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

#credentials file for GMAIL emailing
import credentials

#get yolo swaggin:
image = yolo_swag("last_movement.jpg","/home/pi/darknet/cfg",0.5,0.3)

port = 465  # For SSL
pwd = credentials.setup['GMAIL_PWD']
email = credentials.setup['GMAIL_EMAIL']

timestamp = datetime.datetime.now()

subject = "Motion Capture " + timestamp.strftime(
            "%A %d %B %Y %I:%M:%S%p")
body = "Motion captured in the house"
sender_email = email
receiver_email = "dustin.brown.andrews@gmail.com"#,"magg.stuart@gmail.com"]
cc_email = "magg.stuart@gmail.com"
password = pwd

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
message["Cc"] = cc_email  # Recommended for mass emails

# Add body to email
message.attach(MIMEText(body, "plain"))

filename = "prediction.jpg"  # In same directory as script

# Open PDF file in binary mode
with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

# Encode file in ASCII characters to send by email    
encoders.encode_base64(part)

# Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Create a secure SSL context
context = ssl.create_default_context()

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(email, password)
    server.sendmail(email,"dustin.brown.andrews@gmail.com", text)