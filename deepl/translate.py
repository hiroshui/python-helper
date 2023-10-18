import requests
from os.path import exists

class DeeplHelper:

    @staticmethod
    def send_translation_request(url, data):
        """
        Sends a translation request to the DeepL API.

        Parameters:
        - url (str): The URL of the DeepL API.
        - data (dict): The data to send in the request.

        Returns:
        - response (requests.Response): The response from the API.
        """
        print(f"Translating '{data['text']}' to {data['target_lang']}")
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response

    @staticmethod
    def check_for_file(filename):
        """
        Checks if a file exists and returns its contents.

        Parameters:
        - filename (str): The name of the file to check.

        Returns:
        - file_contents (str): The contents of the file.
        """
        if exists(filename):
            print(f"File {filename} found.")
            with open(filename, "r") as f:
                return f.read().strip()
        else:
            raise FileNotFoundError(f"File '{filename}' not found.")

    @staticmethod
    def run():
        # Set the URL of the DeepL API
        url = 'https://api-free.deepl.com/v2/translate'

        # Get the target language and text to parse from the user
        target_lang = input("Enter target language (DE, EN, etc) to parse: ")
        text_to_parse = input("Enter text to parse: ")

        # Get the API token from a file
        token = DeeplHelper.check_for_file("token")

        # Define the data to send in the request
        data_to_send = {
            "auth_key": token,
            "target_lang": target_lang,
            "text": text_to_parse
        }

        # Send the translation request to the API
        response = DeeplHelper.send_translation_request(url, data_to_send)

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
    DeeplHelper.run()