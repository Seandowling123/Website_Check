import time
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from credentials import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, SENDER_PASSWORD, RECIPIENT_EMAIL

# Check the website status
def check_website(website):
    try:
        response = requests.get(f"https://{website}")
        print(website, response)
        if response.status_code != 200:
            send_alert_email(website, response.status_code)
    except requests.exceptions.RequestException as e:
        send_alert_email(str(e))

# Send an alert email
def send_alert_email(website, status):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = f"Website check alert for {website}"
    body = f"The website {website} is not returning status code 200.\nCurrent status: {status}"
    msg.attach(MIMEText(body, "plain"))

    # Send the email
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()  # Use TLS
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, msg.as_string())

# Entry Point
if __name__ == "__main__":
    time.sleep(30)
    websites = ['mariadowlingtherapy.com', 'seand.ie']
    for website in websites:
        check_website(website)
