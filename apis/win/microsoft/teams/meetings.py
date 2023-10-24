
import pyautogui
import time

from pyautogui import Point as pyPoint
from models.meeting import Meeting

class Meetings():

    meeting_list = [](Meeting)
    
    def start_meeting(self, meeting : Meeting):
        raise NotImplementedError("This method is not implemented yet.")
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
        
    def add(self, meeting: Meeting):
        self.meeting_list.append(meeting)
    
    def remove(self, meeting: Meeting):
        self.meeting_list.remove(meeting)

    def remove(self, meetingname: str):
        meeting = self.meeting_list.find(meetingname)
        self.meeting_list.remove(meeting)