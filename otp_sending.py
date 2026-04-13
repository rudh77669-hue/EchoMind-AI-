import smtplib
import random
import pandas as pd 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_otp_email(receiver_email):
    df=pd.read_csv("user_detail.csv")
    print("hello")
    sender_email = "enter your email"
    sender_password = "ndrn byfs zwog ujul"


    # Generate random 6-digit OTP
    otp = str(random.randint(100000, 999999))

    # Create the email content
    msg = MIMEMultipart()
    msg['From'] = f"password rsest{sender_email}"
    msg['To'] = receiver_email
    msg['Subject'] = "Your OTP Code"


    body = f"Your OTP code is {otp}. It will expire in 5 minutes. for user Id {df.loc[df["Email"]==receiver_email,'User Id'].values[0]}"
    msg.attach(MIMEText(body, 'plain'))
    # Send email via Gmail SMTP
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print("✅ OTP sent successfully!")
        print(otp)
        return otp
    except Exception as e:
        print("❌ Error sending OTP:", e)
        return None
