import argparse
import boto3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def list_dlqs(session):
    sqs_client = session.client('sqs')
    response = sqs_client.list_queues()
    dlq_urls = []

    if 'QueueUrls' in response:
        dlq_urls = response['QueueUrls']

    return dlq_urls

def get_dlq_message_count(session, dlq_url):
    sqs_client = session.client('sqs')
    response = sqs_client.get_queue_attributes(
        QueueUrl=dlq_url,
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
    parser = argparse.ArgumentParser(description="List DLQs and send email report")
    parser.add_argument("--profile", help="AWS profile name", required=True)
    args = parser.parse_args()

    session = boto3.Session(profile_name=args.profile)

    dlqs = list_dlqs(session)

    if dlqs:
        message = "Dead Letter Queues and Their Message Counts:\n\n"
        for dlq_url in dlqs:
            message += f"DLQ URL: {dlq_url}\n"
            message += f"Message Count: {get_dlq_message_count(session, dlq_url)}\n\n"

        send_email(
            smtp_server='smtp-relay.brevo.com',
            smtp_port=587,  # Change if your SMTP server uses a different port
            smtp_username='gudditinaganjaneyulu@gmail.com',
            smtp_password='dJxTUjOLgYwD5qPm',
            sender_email='gudditinaganjaneyulu@gmail.com',  # Your email address
            recipient_email='gudditinaganjaneyulu@gmail.com',  # Recipient email address
            subject='DLQ Message Count Report',
            body=message
        )
    else:
        print("No DLQs found in the AWS account.")
