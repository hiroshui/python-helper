from win32gui import FindWindow, GetWindowRect, IsWindowVisible, ShowWindow
import win32con

#This class is used to get the window of a specific Microsoft Teams window
class Window:
    window_tile = None
    window_handle = None
    window_rect = None
    
    def __init__(self, window_title, pop_up=False):
        #this could be improved by using the EnumWindows function
        #currently we are only searching for the window title using Microsoft Teams or classic depending on the pop_up parameter
        self.window_tile = f"{window_title} | Microsoft Teams classic"
        if pop_up:
            self.window_tile = f"{window_title} | Microsoft Teams"
        self.window_handle = FindWindow(None, self.window_tile)        
        self.window_rect   = GetWindowRect(self.window_handle)
        print(f"Window handle: {self.window_handle}")
        
    def get_window_rect(self):
        real_resolution = (self.window_rect[0], self.window_rect[1], self.window_rect[2] - self.window_rect[0], self.window_rect[3] - self.window_rect[1])
        return real_resolution
    
    def is_windows_visible(self):
        return IsWindowVisible(self.window_handle)
        
    def maximize(self):
        ShowWindow(self.window_handle, win32con.SW_MAXIMIZE)