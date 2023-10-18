import os
import datetime
import time
import pythoncom
import logging
import pandas as pd
import win32com.client as win32
import winsound
import configparser

from models.enums import OutlookImportance, OutlookItems

class EmailProcessor:
    """
    A class for processing emails in Outlook.

    Attributes:
    - config_file (str): The path to the configuration file.
    -   set_unread (bool): Whether to mark the original message as read after responding.
    -   save_mails (bool): Whether to export unread emails to a CSV file.
    -   sleep_timer (int): The number of seconds to sleep between email checks.
    -   sound_file (str): The path to the sound file to play when a new email is received.
    -   csv_filename (str): The prefix of the CSV file to export unread emails to.
    - logger (logging.Logger): The logger object for logging messages.
    - outlook (win32com.client.Dispatch): The Outlook application object.
    - inbox (win32com.client.CDispatch): The default inbox folder.
    - messages (win32com.client.CDispatch): The collection of messages in the inbox.
    """

    def __init__(self, config_file: str, logger : logging.Logger):
        """
        Initializes a new instance of the EmailProcessor class.

        Parameters:
        - config_file (str): The path to the configuration file.
        - logger (logging.Logger): The logger object for logging messages.
        """
        self.logger = logger

        self.outlook = win32.Dispatch("Outlook.Application")
        self.inbox = self.outlook.GetNamespace("MAPI").GetDefaultFolder(6)
        self.messages = self.inbox.Items
        self.messages.Sort("[ReceivedTime]", True)

        # Read the config file
        config = configparser.ConfigParser()
        config.read(config_file)

         # Define a variable for the profile name to read from the config file
        PROFILE_NAME = config.get('GLOBAL', 'profile_name')

        # Get the setUnread and processMails values from the config file
        self.set_unread = config.getboolean(PROFILE_NAME, 'set_unread')
        self.save_mails = config.getboolean(PROFILE_NAME, 'save_mails')
        self.sleep_timer = config.getint(PROFILE_NAME, 'sleep_timer')
        self.sound_file = config.get(PROFILE_NAME, 'sound_file')
        self.csv_filename = config.get(PROFILE_NAME, 'csv_filename')

    def respond_to_emails(self):
        """
        Responds to unread emails in the inbox.
        """
        for message in self.messages:
            if message.Unread:
                sender_email = message.SenderEmailAddress
                sender_first_name = sender_email.split(".")[0].title()
                subject = message.Subject
                #body = message.Body

                #see how important the email is
                importance = OutlookImportance(message.Importance)
                
                text =  f"Hi {sender_first_name},\nich melde mich gleich bei Dir.\n\nBeste Grüße"
                
                if importance == "HIGH":
                    text =  f"Hi {sender_first_name},\nich melde mich gleich bei Dir.\nIch habe verstanden, dass es sich um eine dringende Angelegenheit handelt.\n\nBeste Grüße"

                # Define the email parameters
                recipient_email = sender_email
                response_subject = f"Re: {subject}"
                response_body = text

                # Connect to Outlook
                mail = self.outlook.CreateItem(OutlookItems.EMAIL.value)

                # Set the email properties
                mail.To = recipient_email
                mail.Subject = response_subject
                mail.Body = response_body

                # Send the email
                try:
                    mail.Send()
                    self.logger.info(f"Sent response to {sender_email}")
                    print(f"Sent response to {sender_email}")
                except Exception as e:
                    self.logger.error(f"Error sending response to {sender_email}: {e}")
                    print(f"Error sending response to {sender_email}: {e}")

                if self.set_unread:
                    # Mark the original message as read
                    try:
                        message.Unread = False
                    except Exception as e:
                        self.logger.error(f"Error marking message as read: {e}")
                        print(f"Error marking message as read: {e}")

                # Play a sound
                sound_file=self.sound_file
                if os.path.exists(sound_file):
                    print(f"about to print sound {sound_file}")
                    winsound.PlaySound(sound_file, winsound.SND_FILENAME)
                else:
                    print(f"Warning: sound file {sound_file} not found! Will use default sound.")
                    winsound.PlaySound("SystemAsterisk", winsound.SND_ALIAS)

    def export_unread_emails_to_csv(self):
        """
        Exports unread emails to a CSV file.
        """
        data = []
        for message in self.messages:
            if message.Unread:
                sender_email = message.SenderEmailAddress
                subject = message.Subject
                body = message.Body
                self.logger.info(f"Received email from {sender_email}")

                # Add the email content to the data list
                data.append([sender_email, subject, body])

        # Create a DataFrame from the data list
        df = pd.DataFrame(data, columns=['Sender', 'Subject', 'Body'])

        date_string = datetime.datetime.now().strftime("%Y-%m-%d")
        filename = f"{self.csv_filename}_{date_string}.csv"
        try:
            df.to_csv(filename, index=False)
        except Exception as e:
            self.logger.error(f"Error writing to CSV: {e}")
            print(f"Error writing to CSV: {e}") 

    def run(self):
        """
        Runs the email processing loop.
        """
        while True:
            self.logger.info("Checking for new emails...")
            print("Checking for new emails...")
            pythoncom.CoInitialize()
            if self.save_mails:
                self.export_unread_emails_to_csv()
            self.respond_to_emails()
            print(f"About to sleep for {self.sleep_timer} seconds...")
            time.sleep(self.sleep_timer)