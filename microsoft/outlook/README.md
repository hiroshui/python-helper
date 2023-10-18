# Microsoft Outlook Email Processor

This project contains a Python script for processing emails in Microsoft Outlook.

## Installation

To use this script, you will need to have Python 3 installed on your computer. You will also need to install the following packages:

- pandas
- win32com
- configparser

You can install these packages using pip:
`pip install pandas pywin32 configparser`

## Usage

To use the script, you will need to create a configuration file with the following settings:

- setUnread: Whether to mark the original message as read after responding.
- processMails: Whether to export unread emails to a CSV file.
- sleep_timer: The number of seconds to sleep between email checks.

You can then run the script using the following command:

`python email_processor.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.