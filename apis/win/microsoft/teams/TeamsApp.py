import os
import time
from time import sleep
from enum import Enum
from typing import Any
#import pygetwindow as gw
import pyautogui

class SpecialCommandsEnum(Enum):
    GO_TO_SETTINGS = 1
    GO_TO_CALENDAR = 2
    CREATE_MEETING = 3

class TeamsApp:
    """
    A class for interacting with the Microsoft Teams application.

    Attributes:
    -----------
    config_values : dict
        A dictionary containing configuration values for the TeamsApp instance.

    Methods:
    --------
    __init__(self, config_values : dict)
        Initializes a TeamsApp instance with the given configuration values.

    open(self)
        Opens the Microsoft Teams application.

    is_open(self)
        Checks if the Microsoft Teams application is already open and focused.

    find_button(self, button_name)
        Finds the specified button on the screen.

    click_element(self, button)
        Clicks the specified element.

    click_button_by_name(self, button_name)
        Finds and clicks the specified button by name.
    """

    config_values = None
    pause = 0
    initial_delay = 0
    special_cmds = None
 
    def __init__(self, config_values : dict):
        """
        Initializes a TeamsApp instance with the given configuration values.

        Parameters:
        -----------
        config_values : dict
            A dictionary containing configuration values for the TeamsApp instance.
        """
        self.config_values = config_values
        self.pause = int(self.config_values['Settings']['pause'])
        self.initial_delay = int(self.config_values['Settings']['initial_delay'])
        self.special_cmds = SpecialCommands(self)

    def open(self):
        """
        Opens the Microsoft Teams application.
        """
        teams_path = self.config_values['Runtime']['local_user_path'] + self.config_values['Settings']['teams_app_path']
        print(f"Starting Teams in {teams_path}")
        os.startfile(f"{teams_path}")
        sleep(self.initial_delay)
     
    def is_open(self):
        """
        Checks if the Microsoft Teams application is already open and focused.

        Returns:
        --------
        bool
            True if the Microsoft Teams application is open and focused, False otherwise.
        """
        raise Exception("Not implemented")
        # check if Teams is already opened and focused
        #teams_window = gw.getWindowsWithTitle('Microsoft Teams')
        #if len(teams_window) > 0:
        #    teams_window[0].activate()
        #    return True
        #return False

    def find_button(self, button_name):
        """
        Finds the specified button on the screen.

        Parameters:
        -----------
        button_name : str
            The name of the button to find.

        Returns:
        --------
        tuple or None
            A tuple containing the x and y coordinates of the button's center, or None if the button could not be found.
        """
        button_path = self.config_values['Runtime']['button_path']
        button_fullpath = f"{button_path}/{button_name}.png"
        print(f"Looking for button: {button_fullpath}")
        button = pyautogui.locateCenterOnScreen(button_fullpath)
        if button is None:
            print("Could not find the button on the screen.")
            return None
        return button
    
    def click_element(self, element):
        """
        Clicks the specified pygui-element.

        Parameters:
        -----------
        button : tuple
            A tuple containing the x and y coordinates of the elements's center.
        """
        pyautogui.moveTo(element)
        pyautogui.click()
        sleep(self.pause)
        
    def insert_text(self, element, text):
        """
        Inserts text into the specified pygui-element.

        Parameters:
        -----------
        element : tuple
            A tuple containing the x and y coordinates of the elements's center.
        text : str
            The text to insert.
        """
        pyautogui.moveTo(element)
        pyautogui.click()
        pyautogui.write(text)
        sleep(self.pause)
    
    def click_button_by_name(self, button_name):
        """
        Finds and clicks the specified button by name.

        Parameters:
        -----------
        button_name : str
            The name of the button to click.
        """
        button = self.find_button(button_name)
        if button is None:
            return
        self.click_element(button)
        
    def locate_textfield(self, textfield_content):
        """
        Finds the specified textfield on the screen.

        Parameters:
        -----------
        textfield_content : str
            The content of the textfield to find.

        Returns:
        --------
        tuple or None
            A tuple containing the x and y coordinates of the textfield's center, or None if the textfield could not be found.
        """
        textfield = pyautogui.locateCenterOnScreen(textfield_content)
        if textfield is None:
            print("Could not find the textfield on the screen.")
            return None
        return textfield
        
    def exec_special_cmd(self, cmd_name, *args):
        """
        Executes the specified special command.

        Parameters:
        -----------
        cmd_name : SpecialCommands
            The name of the special command to execute.
        """
        
        cmd_enum = getattr(SpecialCommandsEnum, cmd_name.upper())
        
        return self.special_cmds.execute_special_command(cmd_enum, args=args)


class SpecialCommands:
    app = None
        
    def __init__(self, app : TeamsApp):
        self.app = app
        
    def go_to_settings(self):
        self.app.open()
        self.app.click_button_by_name("dots")
        self.app.click_button_by_name("settings")
        
    def go_to_calendar(self):
        self.app.open()
        self.app.click_button_by_name("calendar")
    
    def create_meeting(self, meeting_name):
        self.app.open()
        self.app.click_button_by_name("calendar")
        titel_field = self.app.locate_textfield("Title")
        self.app.insert_text(titel_field, meeting_name)
    
    # Add more methods here for each entry in SpecialCommandsEnum
    def execute_special_command(self, cmd_name : SpecialCommandsEnum, *args):
        """
        Executes the specified special command.

        Parameters:
        -----------
        cmd_name : SpecialCommandsEnum
            The name of the special command to execute.
        """
        try:
            cmd = getattr(self, cmd_name.name.lower())(*args)
        except AttributeError as ae:
            print(f"Unknown special command: {cmd_name}, error: {ae}")
            return False
        cmd()
        return True
    
    # Add more special commands here
