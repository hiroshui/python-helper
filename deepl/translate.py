import requests
import os
from os.path import exists
import sys


class DeeplHelper:
    
    def __init__(self, url='https://api-free.deepl.com/v2/translate', token_file='token'):
        """
        Initializes a new instance of the DeeplHelper class.

        Parameters:
        - url (str): The URL of the DeepL API.
        - token_file (str): The name of the file containing the API token.
        """
        self.url = url
        self.token_file = token_file

    def send_translation_request(self, data):
        """
        Sends a translation request to the DeepL API.

        Parameters:
        - data (dict): The data to send in the request.

        Returns:
        - response (requests.Response): The response from the API.
        """
        print(f"Translating '{data['text']}' to {data['target_lang']}")
        response = requests.post(self.url, data=data)
        response.raise_for_status()
        return response

    def check_for_file(self):
        """
        Checks if the API token file exists and returns its contents.

        Returns:
        - file_contents (str): The contents of the API token file.
        """
        if exists(self.token_file):
            print(f"File {self.token_file} found.")
            with open(self.token_file, "r") as f:
                return f.read().strip()
        else:
            raise FileNotFoundError(f"File '{self.token_file}' not found.")

    def translate_file(self, input_file, output_file, target_lang):
        """
        Translates a plain text file line by line and writes the translated output to a new file.

        Parameters:
        - input_file (str): The name of the input file to translate.
        - output_file (str): The name of the output file to write the translated output to.
        - target_lang (str): The target language to translate the text to.
        """
        # Get the API token from a file
        token = self.check_for_file()

        # Open the input and output files
        with open(input_file, "r") as f_in, open(output_file, "w") as f_out:
            # Translate each line of the input file and write the translated output to the output file
            for line in f_in:
                # Define the data to send in the request
                data_to_send = {
                    "auth_key": token,
                    "target_lang": target_lang,
                    "text": line.strip()
                }

                # Send the translation request to the API
                response = self.send_translation_request(data_to_send)

                # Parse the response JSON
                r_json = response.json()

                # Extract the translation from the response
                try:
                    translation = r_json["translations"][0]["text"]
                    f_out.write(f"{translation}\n")
                except (KeyError, IndexError):
                    print("Error: Invalid response from API")

    def run(self):
        """
        Runs the DeeplHelper program.

        Prompts the user for a target language and text to parse, then sends a translation request to the DeepL API
        and prints the translated text and detected source language.
        """
        # Get the target language and text to parse from the user
        target_lang = input("Enter target language (DE, EN, etc) to parse: ")
        text_to_parse = input("Enter text to parse: ")

        # Get the API token from a file
        token = self.check_for_file()

        # Define the data to send in the request
        data_to_send = {
            "auth_key": token,
            "target_lang": target_lang,
            "text": text_to_parse
        }

        # Send the translation request to the API
        response = self.send_translation_request(data_to_send)

        # Parse the response JSON
        r_json = response.json()

        # Extract the translation and detected source language from the response
        try:
            translation = r_json["translations"][0]["text"]
            translated_lang = r_json["translations"][0]["detected_source_language"]
            print(f"Translated from {translated_lang}: '{translation}'")
        except (KeyError, IndexError):
            print("Error: Invalid response from API")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: Input file name not provided.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = input_file.split(".")[0] + "_en.txt"
    deepl = DeeplHelper()
    deepl.translate_file(input_file, output_file, "EN")