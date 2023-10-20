import os             
import time
from time import sleep
from datetime import datetime
import configparser
from TeamsApp import TeamsApp

class Startup:
    config_values = None

    # initialize the Startup class without any parameters
    def __init__(self):
        self.config_values = {}

    def run(self):
        pass
        #tbd: add code for startup

    # now we will initialize the config based on the given path
    def initialize_config(self, path='config.ini'):
        # create a ConfigParser object
        config = configparser.ConfigParser()
        # read the config.ini file
        config.read(path)
        # loop through all sections in the config file
        for section in config.sections():
            # create a new dictionary for the section
            section_dict = {}
            # loop through all options in the section
            for option in config.options(section):
                # add the option and its value to the section dictionary
                section_dict[option] = config.get(section, option)
            # add the section dictionary to the config_values dictionary
            self.config_values[section] = section_dict
    
    def initialize_runtime_variables(self):
        try:
            #add runtime config values
            image_path = os.path.join(os.path.dirname(__file__), 'images')
            button_path = os.path.join(image_path, 'buttons')
            local_user_path = os.path.expanduser("~")
            #add those variables to the config as a own section
            section_dict = {}
            section_dict["image_path"] = image_path
            section_dict["button_path"] = button_path
            section_dict["local_user_path"] = local_user_path
            self.config_values['Runtime'] = section_dict
        except Exception as e:
            print(e)
    
    # we want to be able to get the config values from outside of the class
    def get_config(self):
        return self.config_values
    
    def print_config(self):
        for section, options in self.config_values.items():
            print(f"[{section}]")
            for option, value in options.items():
                print(f"{option} = {value}")

if __name__ == "__main__":
    startup = Startup()
    startup.initialize_config()
    startup.initialize_runtime_variables()
    print("Config values:")
    startup.print_config()
    app = TeamsApp(startup.get_config())
    
    app.open()
    app.click_button_by_name("dots")