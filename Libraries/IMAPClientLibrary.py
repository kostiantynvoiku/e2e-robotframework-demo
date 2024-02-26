import email
import time
import ssl
import re
from imapclient import IMAPClient, DELETED
from datetime import datetime
from datetime import timedelta
from robot.api import logger
from robot.api.deco import keyword, library
from email.header import decode_header, make_header


@library(scope='GLOBAL')
class IMAPClientLibrary:

    def __init__(self, country_code=''):
        self.imap_host = "imap.googlemail.com"
        self.imap_user = ""
        self.imap_password = ""
        self.country_code = country_code.upper()

    @keyword
    def get_mail_to_by_subject(self, mail, subject, timeout=5):
        subj = subject.encode('utf-8')
        since = datetime.now() - timedelta(minutes=1)
        wait_until = datetime.now() + timedelta(minutes=timeout)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(host=self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder(self.country_code)
            wait_message = f"INFO: Waiting for email to '{mail}' with subject '{subject}' received since '{since}'"
            messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj, b'TO', mail, u'SINCE', since])
            while len(messages) < 1:
                if wait_until < datetime.now():
                    raise AssertionError(f"No emails '{subject}' until timeout")
                logger.console(wait_message)
                time.sleep(15)
                client.select_folder(self.country_code)
                messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj, b'TO', mail, u'SINCE', since])
            response = client.fetch(messages, ['RFC822'])
            msg = response[messages[0]][b'RFC822']
            mime_msg = email.message_from_bytes(msg)
            logger.console(f"INFO: Email '{subject}' received in folder '{self.country_code}'")
            client.delete_messages(messages, silent=True)
            client.expunge()
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/html':
                    payload = part.get_payload(decode=True)
            return payload.decode('utf-8', errors='ignore')

    @keyword
    def get_mail_by_subject(self, subject, timeout=5):
        subj = subject.encode('utf-8')
        wait_until = datetime.now() + timedelta(minutes=timeout)
        since = datetime.now() - timedelta(minutes=1)
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder(self.country_code)
            wait_message = f"INFO: Waiting for email with subject '{subject}' received since '{since}'"
            messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj, u'SINCE', since])
            while len(messages) < 1:
                if wait_until < datetime.now():
                    raise AssertionError(f"No emails '{subject}' until timeout")
                logger.console(wait_message)
                time.sleep(15)
                client.select_folder(self.country_code)
                messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj, u'SINCE', since])
            response = client.fetch(messages, ['RFC822'])
            msg = response[messages[0]][b'RFC822']
            # Get recipient's email address:
            for msgid, data in client.fetch(messages, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']
                recipient = envelope.to[0]
            mime_msg = email.message_from_bytes(msg)
            logger.console(f"INFO: Email '{subject}' received by '{recipient}' in folder '{self.country_code}'")
            client.delete_messages(messages, silent=True)
            client.expunge()
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/html':
                    payload = part.get_payload(decode=True)
            return dict(payload=payload.decode('utf-8', errors='ignore'), recipient=recipient)

    @keyword
    def delete_email_by_subject(self, subject):
        subj = subject.encode('utf-8')
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder(self.country_code)
            messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj])
            client.add_flags(messages, [DELETED])
            client.expunge()
            logger.console(f"INFO: Email '{subject}' deleted from folder '{self.country_code}'")

    @keyword
    def clean_robot_folder(self):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder(self.country_code)
            messages = client.search(['NOT', 'DELETED'])
            client.add_flags(messages, [DELETED])
            client.expunge()
            logger.console(f"INFO: '{self.country_code}' folder is clean")

    @keyword
    def get_full_email_log(self, email_address):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder('[Gmail]/All Mail')
            messages_encoded = client.search([b'CHARSET', b'UTF-8', b'TO', email_address])
            while len(messages_encoded) < 1:
                raise AssertionError(f"No emails received by {email_address}")
            messages = []
            for msgid, data in client.fetch(messages_encoded, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']
                decoded_message = make_header(decode_header(envelope.subject.decode('utf-8')))
                messages.append(f"'{decoded_message}' received on {envelope.date}")
        return messages

    @keyword
    def get_links_from_email(self, mail_body, text_in_link):
        all_links = re.findall(r'href=[\'"]?([^\'" >]+)', mail_body)
        links_to_return = []
        for link in all_links:
            if text_in_link in link:
                links_to_return.append(link)
        return links_to_return

    @keyword
    def get_full_email_log_titles(self, email_address):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder('[Gmail]/All Mail')
            messages_encoded = client.search([b'CHARSET', b'UTF-8', b'TO', email_address])
            while len(messages_encoded) < 1:
                raise AssertionError(f"No emails received by {email_address}")
            messages = []
            for msgid, data in client.fetch(messages_encoded, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']
                decoded_message = make_header(decode_header(envelope.subject.decode('utf-8')))
                messages.append(decoded_message)
        return messages

    @keyword
    def get_mail_to_by_subjects(self, mail, subject1, subject2):
        subj1 = subject1.encode('utf-8')
        subj2 = subject2.encode('utf-8')
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder('[Gmail]/All Mail')
            logger.console(f"INFO: Looking for email to '{mail}' with subject '{subject1}'")
            messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj1, b'TO', mail])
            if len(messages) < 1:
                logger.console(f"INFO: No email received. Looking for another subject: '{subject2}'")
                messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj2, b'TO', mail])
                if len(messages) < 1:
                    raise AssertionError("No emails received!")
            response = client.fetch(messages, ['RFC822'])
            msg = response[messages[0]][b'RFC822']
            mime_msg = email.message_from_bytes(msg)
            logger.console("INFO: Email received")
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/html':
                    payload = part.get_payload(decode=True)
            return payload.decode('utf-8', errors='ignore')

    @keyword
    def get_mail_by_subjects(self, subject1, subject2):
        subj1 = subject1.encode('utf-8')
        subj2 = subject2.encode('utf-8')
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        with IMAPClient(self.imap_host, ssl_context=ssl_context) as client:
            client.login(self.imap_user, self.imap_password)
            client.select_folder(self.country_code)
            logger.console(f"INFO: Looking for email with subject '{subject1}'")
            messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj1])
            if len(messages) < 1:
                logger.console(f"INFO: No email received. Looking for another subject: '{subject2}'")
                messages = client.search([b'CHARSET', b'UTF-8', b'SUBJECT', subj2])
                if len(messages) < 1:
                    raise AssertionError("No emails received!")
            response = client.fetch(messages, ['RFC822'])
            msg = response[messages[0]][b'RFC822']
            # Get recipient's email address:
            for msgid, data in client.fetch(messages, ['ENVELOPE']).items():
                envelope = data[b'ENVELOPE']
                recipient = envelope.to[0]
            mime_msg = email.message_from_bytes(msg)
            logger.console("INFO: Email received")
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/html':
                    payload = part.get_payload(decode=True)
            return dict(payload=payload.decode('utf-8', errors='ignore'), recipient=recipient)
