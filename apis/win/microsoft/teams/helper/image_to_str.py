import os
import pyautogui
import pytesseract
import cv2
import numpy as np

class ImageHelper():
    
    config_values = None
    
    def __init__(self, config_values: dict):
        self.config_values = config_values
        pytesseract.pytesseract.tesseract_cmd = self.config_values['Runtime']['local_user_path'] + self.config_values['Settings']['tesseract_exec_path']
        os.environ["TESSDATA_PREFIX"] = self.config_values['Runtime']['local_user_path'] + self.config_values['Settings']['tesseract_data_path']
  
    def find_coordinates_text(self, textcontent, language, resolution):
        print(f"resolution is {resolution}")
        if resolution is None:
            # Take a screenshot of the main screen
            screenshot = pyautogui.screenshot()
        else:
            screenshot = pyautogui.screenshot(region=resolution)

        # Convert the screenshot to grayscale
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2GRAY)

        # Find the provided text (text) on the grayscale screenshot 
        # using the provided language (language)
        data = pytesseract.image_to_data(img, lang=language, output_type='data.frame')

        # Find the coordinates of the provided text (text)
        try:
            x, y = data[data['text'] == textcontent]['left'].iloc[0], data[data['text'] == textcontent]['top'].iloc[0]

        except IndexError:
            # The text was not found on the screen
            return None

        # Text was found, return the coordinates
        return (x, y)