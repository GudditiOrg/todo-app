import os
import argparse
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

def list_queues(session):
    sqs_client = session.client('sqs')
    response = sqs_client.list_queues()
    queue_urls = []

    if 'QueueUrls' in response:
        queue_urls = response['QueueUrls']

    return queue_urls

def get_queue_message_count(session, queue_url):
    sqs_client = session.client('sqs')
    response = sqs_client.get_queue_attributes(
        QueueUrl=queue_url,
        AttributeNames=['ApproximateNumberOfMessages']
    )
    return int(response['Attributes']['ApproximateNumberOfMessages'])

def send_email(smtp_server, smtp_port, smtp_username, smtp_password, sender_email, recipient_email, subject, body, attachment=None):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    if attachment:
        with open(attachment, 'rb') as file:
            part = MIMEApplication(file.read(), Name="dlq_report.csv")
            part['Content-Disposition'] = f'attachment; filename="{attachment}"'
            msg.attach(part)

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Email could not be sent: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List Queues (DLQs and Normal Queues) and send email report")
    parser.add_argument("--profile", help="AWS profile name", required=True)
    args = parser.parse_args()

    session = boto3.Session(profile_name=args.profile)

    queues = list_queues(session)

    if queues:
        message = "Queues and Their Message Counts:\n\n"
        for queue_url in queues:
            message += f"Queue URL: {queue_url}\n"
            message += f"Queue Name: {queue_url.split('/')[-1]}\n"
            message += f"Message Count: {get_queue_message_count(session, queue_url)}\n\n"

        send_email(
            smtp_server=os.getenv('SMTP_SERVER'),
            smtp_port=int(os.getenv('SMTP_PORT')),
            smtp_username=os.getenv('SMTP_USERNAME'),
            smtp_password=os.getenv('SMTP_PASSWORD'),
            sender_email=os.getenv('SENDER_EMAIL'),
            recipient_email=os.getenv('RECIPIENT_EMAIL'),
            subject='Queue Message Count Report',
            body=message
        )
    else:
        print("No Queues found in the AWS account.")
