import os
import configparser

import openai

from helper.outputparser import CommaSeparatedListOutputParser

from templates.rewrite import RewriteTemplate


class OpenAIModel():
    """
    A class representing an OpenAI model.

    Attributes:
    api_type (str): The OpenAI API api type.
    api_version (str): The OpenAI API api version.
    api_key (str): The OpenAI API api key.
    api_base (str): The OpenAI API base endpoint.
    """
    
    api_version = None
    api_type = None
    api_key = None
    api_base = None
    llm = None
    
    def __init__(self):
        """
        Initializes the OpenAI API.
        """
        self.init_openai_api()

    def __init__(self, configfile: str = 'config.ini'):
        """
        Initializes the OpenAI API with a specific config.ini.
        """
        self.init_openai_api(configfile)

    def init_openai_api(self, configfile: str = 'config.ini'):
        """
        Initializes the OpenAI API by reading the access token from a config file.
        """
        try:
            config = configparser.ConfigParser()
            config.read(configfile)
            self.api_key = config['openai']['api_key']  # Read the api_key from the config file
            self.api_base = config['openai']['api_base']  # Read the endpoint from the config file
            self.api_version = config['openai']['api_version']  # Read the api_version from the config file
            self.api_type = config['openai']['api_type']  # Read the api_type from the config file
            print("LLM now configured using the configuration")
        except Exception as e:
            print(f"Error initializing OpenAI from {configfile}: {e}")

        os.environ["OPENAI_API_TYPE"] = self.api_type
        os.environ["OPENAI_API_VERSION"] = self.api_version
        os.environ["OPENAI_API_KEY"] = self.api_key
        os.environ["OPENAI_API_BASE"] = self.api_base

    def generate_prompt(self, template: str, request_text: str, model: str="generative_ai", temperature: float = 0.25, max_tokens: int = 1000):
        """
        Generates prompt using the openai model.

        Args:
        template (str): The template used to tell OpenAi what to do with the following request.
        request_text (str): The text to be used as input for the model to generate the prompt.
        model (str): The name of the OpenAI model to use.
        max_tokens (int): The maximum number of tokens to generate.

        Returns:
        str: The generated text.
        """        
        delimiter = "```" 
        
        messages = [
        {"role": "system", "content": template},
        {"role": "user", "content": f"{delimiter}{request_text}{delimiter}"},
        {"role": "assistant", "content": f"Relevant for the user's question: {delimiter}{request_text}{delimiter}"}   
        ]
        
        openai.api_base = self.api_base
        openai.api_key = self.api_key
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        
        try:
            response = openai.ChatCompletion.create(
                engine=model,
                messages=messages,
                temperature=temperature, 
                max_tokens=max_tokens, 
            )
            return response.choices[0].message["content"]  
        except Exception as e:
            print(f"Error occured: {e}")
        return None
    
    

    
    def get_completion_from_messages(self, messages, engine="generative_ai", temperature=0.25, max_tokens=1000):
        openai.api_base = self.api_base
        openai.api_key = self.api_key
        openai.api_type = self.api_type
        openai.api_version = self.api_version
        
        response = openai.ChatCompletion.create(
            engine=engine,
            messages=messages,
            temperature=temperature, 
            max_tokens=max_tokens, 
        )
        return response.choices[0].message["content"]  

       

#testcases
if __name__ == '__main__':
    model = OpenAIModel()
    
    system_message = f"""Hello, you will receive content of a mail that the user received.\
                        The user is a consultant working in the IT.\
                        Received mail could be either in english or german.\
                        Translate it to german if necessary,\
                        then summarize it and tell if the mail is for work or private reasons,\
                        if he got something to do and if he needs to answer that mail.\
                        I want a section with the summary, how urgent it is in percent and a section with an prefered answer\
                        to the received mail. Try to sound in that answer section like the user is answering,\
                        so the sender wont notice that its not coming from the user.\
                        Always add a answer, even if its not urgent!\
                        Answer in the language that the mail was written in.\
                        """

    input = input("input: ")

    print(model.generate_prompt(system_message,input))