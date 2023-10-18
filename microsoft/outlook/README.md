# Microsoft Outlook Email Processor

This project contains a Python script for processing emails in Microsoft Outlook.

## Installation

To use this script, you will need to have Python 3 installed on your computer. Also your computer needs to be a Windows client! 

Python can be installed from the official python website: https://www.python.org/downloads/windows/

You will also need to install the following packages:

- pandas
- win32com
- configparser

You can install these packages using pip:
`pip install pandas pywin32 configparser`



## Usage

To use the script, you will need to create a configuration file (config.ini) with the following settings:

- profile_name: The name of the profile to use for accessing the Outlook inbox.
- set_unread: Whether to mark the original message as read after responding.
- save_mails: Whether to export unread emails to a CSV file.
- sleep_timer: The number of seconds to sleep between email checks.
- sound_file: The path to the sound file to play when a new email is received.
- csv_filename: The prefix of the CSV file to export unread emails to.

You can then run the script using the following command:

`python automailer.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.