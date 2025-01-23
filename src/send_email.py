import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import os

# Gmail credentials (use environment variables for safety)
GMAIL_USER = os.getenv('GMAIL_USER')  # Your Gmail address
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')  # App password for Gmail

def send_email(sender_name, sender_email, recipient_name, recipient_email, company):
    try:
        # Create the email
        subject = f"Excited to Connect with {company}"
        body = f"Hi {recipient_name},\n\nI wanted to reach out to discuss potential opportunities available at {company}.\nLooking forward to hearing from you!\n\nThanks,\n{sender_name}"

        msg = MIMEMultipart()
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Connect to the Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.send_message(msg)

        print(f"Email sent to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email to {recipient_email}: {e}")


def main():
    # Sender details
    sender_name = "Dhairy Raval"
    sender_email = GMAIL_USER

    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("Please set your Gmail credentials as environment variables.")
        return

    # Read recipients from a CSV file
    input_file = 'recipients.csv'  # Update with your CSV file path

    try:
        with open(input_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                name = row['Name']
                email = row['Email']
                company = row['Company']
                send_email(sender_name, sender_email, name, email, company)

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except KeyError as e:
        print(f"Error: Missing column in CSV: {e}")

if __name__ == "__main__":
    main()

