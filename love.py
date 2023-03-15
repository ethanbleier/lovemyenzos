from google.oauth2.service_account import Credentials
import email.message, gspread, smtplib

# Assigning sheet ID variable, sender email and protected password
sheet_id = 'UPDATE ME with sheet id'
sender_email = 'UPDATE ME with email'
sender_password = 'UPDATE ME with password'

# Subject of email
subject = 'UPDATE ME'

# Read textfile and assign to content
with open('textfile.txt', 'r') as file: #create textfile.txt and paste your email
    content = file.read()

# Define scope & authorize credentials
scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = Credentials.from_service_account_file('YOUR RELATIVE PATH TO CREDS, UPDATE ME', scopes=scope)
client = gspread.authorize(creds)

# Open the Google Sheet and worksheet
sheet = client.open_by_key(sheet_id).worksheet('UPDATE ME')

# Read data from Google Sheet
data = sheet.get_all_records()

# Loop through google sheet data
for row in data:
    
    # Read recipient email & first name from google sheet
    recipient_email = row['Email']
    recipient_name = row['First Name']
    
    # Create personalized email
    body_template = content.format(name = recipient_name)
    clean_body = body_template.replace('\xa0', ' ').encode() # gpt3 inspired hack. idk.
    msg = email.message.Message()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_payload(clean_body)

    # Connect to SMTP server and send email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, sender_password)
    s.send_message(msg)
    s.quit()
