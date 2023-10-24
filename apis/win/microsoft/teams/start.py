import os             
import configparser

from TeamsApp import SpecialCommands, SpecialCommandsEnum, TeamsApp
from models.meeting import Meeting

class Startup:
    config_values = {}

    # initialize the Startup class without any parameters
    def __init__(self):
        self.config_values = {}

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
    # Set the DISPLAY environment variable to an empty string
    
    startup = Startup()
    startup.initialize_config()
    startup.initialize_runtime_variables()
    print("Config values:")
    startup.print_config()
    app = TeamsApp(startup.get_config())
    
    #app.exec_special_cmd("go_to_settings")

    special_cmds = SpecialCommands(app)
    
    participants = [""]
    
    meeting = Meeting("Test Meeting", "25.10.2024", "10:30", "11:00", participants)

    special_cmds.execute_special_command(SpecialCommandsEnum.CREATE_MEETING, meeting, "deu")

    #app.exec_special_cmd("create_meeting", "Test Meeting")

    #app.open()
    #app.click_button_by_name("dots")
    #app.click_button_by_name("settings")