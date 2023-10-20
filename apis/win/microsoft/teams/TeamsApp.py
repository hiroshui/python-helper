import os
import time
from time import sleep
from enum import Enum
#import pygetwindow as gw
import pyautogui

import os
from time import sleep
import pyautogui


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

    click_button(self, button)
        Clicks the specified button.

    click_button_by_name(self, button_name)
        Finds and clicks the specified button by name.
    """

    config_values = None
    pause = 0
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
        self.special_cmds = SpecialCommands(self)

    def open(self):
        """
        Opens the Microsoft Teams application.
        """
        teams_path = self.config_values['Runtime']['local_user_path'] + self.config_values['Settings']['teams_app_path']
        print(f"Starting Teams in {teams_path}")
        os.startfile(f"{teams_path}")
        sleep(self.pause)
     
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
    
    def click_button(self, button):
        """
        Clicks the specified button.

        Parameters:
        -----------
        button : tuple
            A tuple containing the x and y coordinates of the button's center.
        """
        pyautogui.moveTo(button)
        pyautogui.click()
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
        self.click_button(button)
        
    def exec_special_cmd(self, cmd_name):
        """
        Executes the specified special command.

        Parameters:
        -----------
        cmd_name : SpecialCommands
            The name of the special command to execute.
        """
        try:
            cmd = self.special_cmds[cmd_name]
        except KeyError as ke:
            print(f"Unknown special command: {cmd_name}, error: {ke}")
            return False
    
        if cmd == SpecialCommands.GO_TO_SETTINGS:
            self.special_cmds.go_to_settins()
        
        return True
        
class SpecialCommands(Enum):
        GO_TO_SETTINGS = 1
        # Add more special commands here

class SpecialCommands:
    app = None
    def __init__(self, app : TeamsApp):
        self.app = app

    def go_to_settins(self):
        self.app.open()
        self.app.click_button_by_name("dots")
        self.app.click_button_by_name("settings")