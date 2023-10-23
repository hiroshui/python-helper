
import pyautogui
import time

from pyautogui import Point as pyPoint

class Meetings():

    meeting_list = None
    
    def __init__(self, pause=3, meeting_list=[]):
        self.pause = pause
        self.meeting_list = meeting_list
    
    def find_meeting(self, meeting_name) -> (pyPoint | None):
        if meeting_name not in self.meeting_list:
            raise ValueError("Meeting name not found in meeting list.")
        
        # Locate the meeting button on the screen
        meeting_button = pyautogui.locateCenterOnScreen(meeting_name)
        if meeting_button is None:
            print("Could not find the meeting button on the screen.")
            return None
        return meeting_button
    
    def start_meeting(self, meeting : pyPoint):
        
        # Click the meeting button
        pyautogui.moveTo(pyPoint)
        pyautogui.click()
        time.sleep(self.pause)
        
        # Locate the join button on the screen
        join_button = pyautogui.locateCenterOnScreen("join.PNG")
        if join_button is None:
            print("Could not find the join button on the screen.")
            return
        
        # Click the join button
        pyautogui.moveTo(join_button)
        pyautogui.click()
        time.sleep(self.pause)
        
        # Locate the audio off button on the screen
        audio_off_button = pyautogui.locateCenterOnScreen("audiooff.PNG")
        if audio_off_button is None:
            print("Could not find the audio off button on the screen.")
            return
        
        # Click the audio off button
        pyautogui.moveTo(audio_off_button)
        pyautogui.click()
        time.sleep(self.pause)
        
    def add(self, meetingname):
        pass
    
    def remove(self, meetingname):
        pass
