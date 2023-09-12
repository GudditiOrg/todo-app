# DLQ Report Script

This script retrieves information about queues in an AWS account, including Dead Letter Queues (DLQs), and sends a report via email.

## Installation

1. Clone the repository

  ```bash
   git clone https://github.com/your_username/dlq-report-script.git
  ```
2. Navigate to the project directory
  ```bash
  cd dlq-report-script
  ``` 
3. Install the required dependencies

  ```bash
  pip install -r requirements.txt
  ```

## Configuration
Create a .env file in the project directory with the following content, and replace the placeholders with your actual values:

  ```bash
  SMTP_SERVER=your_smtp_server
  SMTP_PORT=587
  SMTP_USERNAME=your_smtp_username
  SMTP_PASSWORD=your_smtp_password
  SENDER_EMAIL=your_sender_email
  RECIPIENT_EMAIL=your_recipient_email

  ```
## Running the Script
Run the script using the following command:

  ```bash
  python dlq-report.py --profile dev

  ```

> Replace dev with your AWS profile name.    