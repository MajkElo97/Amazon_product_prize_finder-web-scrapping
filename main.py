import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

TARGET_PRICE = 65
URL = "https://www.amazon.com/ROCCAT-Wireless-Surround-Superhuman-Lighting/dp/B093MTTDTL?ref_=Oct_DLandingS_D_5edc7aef_66"
HEADER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Accept-Language": "pl,pl-PL;q=0.9,en-US;q=0.8,en;q=0.7"
}

sender = "YOUR EMAIL HERE"
password = "YOUR PASSWORD HERE"
receiver = ["YOUR EMAIL HERE"]

msg = EmailMessage()
msg['Subject'] = 'Low price alert on Your product!!!'
msg['From'] = sender
msg['To'] = ', '.join(receiver)

response = requests.get(url=URL, headers=HEADER)
soup = BeautifulSoup(response.text, "lxml")
price = float(soup.select("span.a-offscreen")[0].getText().split("$")[1])
title = soup.select("span#productTitle")[0].getText().split(",")[0].strip()

if price <= TARGET_PRICE:
    message = f"{title} is now {price}"
    message = f"{message}\n{URL}"
    print(message)
    msg.set_content(message)
    try:
        with smtplib.SMTP("YOUR EMAIL DOMAIN HERE", 587) as connection:
            connection.starttls()
            connection.login(user=sender, password=password)
            connection.sendmail(from_addr=sender, to_addrs=receiver, msg=msg.as_string())
            print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")
