import base64
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from requests import HTTPError

SCOPES = [
        "https://www.googleapis.com/auth/gmail.send",
        "https://mail.google.com/"
    ]
flow = InstalledAppFlow.from_client_secrets_file('client_secret_629156201159-ssmhsqorvjkkuobueqr3tprjcenj9dmp.apps.googleusercontent.com.json', SCOPES)
creds = flow.run_local_server(port=0)

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])

def get_email_content():

    email_content = request.get_json()

    service = build('gmail', 'v1', credentials=creds)
    message = MIMEText(email_content["content"])
    message['to'] = email_content["email"]
    message['subject'] = email_content["subject"]
    create_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    try:
        message = (service.users().messages().send(userId="me", body=create_message).execute())
        print(F'sent message to {message} Message Id: {message["id"]}')
    except HTTPError as error:
        print(F'An error occurred: {error}')
        message = None