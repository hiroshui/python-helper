# DeeplHelper

DeeplHelper is a Python script that sends a translation request to the DeepL API and prints the translated text and detected source language.

## Prerequisites

Before running the script, you need to obtain an API key from DeepL. You can sign up for a free account and get an API key [here](https://www.deepl.com/pro#developer).

Please store the token plain inside a new file that you need to create called 'token'.

## Usage

To use the script, simply run the `translate.py` file in your terminal or IDE. 

If you do not specify any parameters, you will be prompted to enter the target language and text to parse. The script will then send a translation request to the DeepL API and print the translated text and detected source language.

If you speficy a file as a parameter, then this file will be translated to EN (english). Be aware that only plain text files are currently supported..

`python translate.py`

`python translate.py test.txt`

## Configuration

The script reads the API key from a file named `token` in the same directory as the script. If the file does not exist, the script will raise a `FileNotFoundError`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
