import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import formataddr
from email import encoders

# Gmail credentials (use environment variables for safety)
GMAIL_USER = os.getenv('GMAIL_USER')  # Your Gmail address
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD')  # App password for Gmail
GMAIL_NAME = os.getenv('GMAIL_NAME')  # Your Name

# Function to list all PDFs in the './docs/' directory
def list_pdfs():
    pdf_files = [f for f in os.listdir('./docs/') if f.endswith('.pdf')]
    if not pdf_files:
        return []
    print("\nAvailable PDFs:")
    for idx, file in enumerate(pdf_files, 1):
        print(f"{idx}. {file}")
    return pdf_files

# Function to remove a PDF
def remove_pdf(pdfs):
    try:
        pdf_num = int(input("\nEnter the number of the PDF to remove (or 0 to skip): "))
        if 1 <= pdf_num <= len(pdfs):
            removed_pdf = pdfs.pop(pdf_num - 1)
            print(f"Removed {removed_pdf}")
        elif pdf_num == 0:
            print("No PDFs removed.")
        else:
            print("Invalid number. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")
    return pdf_num

def send_email(sender_name, sender_email, recipient_name, recipient_email, company, job, selected_pdfs):
    try:
        # Create the email
        subject = f"Application for {job} at {company} - {sender_name}"
        body = f"Hi {recipient_name},\n\nI recently came across the posting for the {job} position at {company} on LinkedIn and feel that my skills and experience align well with the role.\nI've attached my resume along with this email and would appreciate the opportunity for a quick chat or interview to discuss how I can contribute to {company}'s team!\n\nThanks,\n{sender_name}"
        msg = MIMEMultipart()
        msg['From'] = formataddr((sender_name, sender_email))
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        # Attach documents
        for doc in selected_pdfs:
            file_path = f"./docs/{doc}"
            try:
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename={doc}')
                msg.attach(part)
            except Exception as e:
                    print(f"Failed to attach {doc}: {e}")

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
    sender_name = GMAIL_NAME
    sender_email = GMAIL_USER
    pdfs = list_pdfs()
    selected_pdfs = pdfs.copy()

    if not pdfs:
        continue_choice = input("No PDFs found in ./docs/\nTo continue press 'y' / Press any other key to exit: ").lower()
        if continue_choice != 'y':
            return
    else:
        while True:
            pdf_num = remove_pdf(selected_pdfs)
            if not selected_pdfs:
                print("No PDFs left to remove.")
                break
            if pdf_num == 0: break
            continue_choice = input("Do you want to remove another PDF? (y/n): ").lower()
            if continue_choice != 'y':
                break
            else:
                print("\nAvailable PDFs:")
                for idx, file in enumerate(selected_pdfs, 1):
                    print(f"{idx}. {file}")


    if not GMAIL_NAME or not GMAIL_USER or not GMAIL_PASSWORD:
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
                job = row['Job']
                send_email(sender_name, sender_email, name, email, company, job, selected_pdfs)

    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
    except KeyError as e:
        print(f"Error: Missing column in CSV: {e}")

if __name__ == "__main__":
    main()
