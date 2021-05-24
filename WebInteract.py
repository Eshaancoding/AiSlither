import win32gui 
import win32ui 
import win32con 
import win32api
from PIL import Image
import time
import numpy as np
from math import ceil
import ctypes


class WebInteract:

    # determine the size of all monitors in pixels 
    width = 600
    height = 600 
    left = 0    
    top = 0 
    hdesktop = None
    desktop_dc = None
    img_dc =  None
    mem_dc = None
    screenshot = None

    def __init__(self, width, height, left, top):
        # box dim
        self.width = width
        self.height = height
        self.left = left
        self.top = top

        ctypes.windll.shcore.SetProcessDpiAwareness(1)

        # grab a handle to the main desktop window 
        self.hdesktop = win32gui.GetDesktopWindow() 

        # set window to correct location
        print("You have 3 second to click the desired window!")
        for i in range(3, 0, -1):
            print(i)
            time.sleep(1)
        hwnd = win32gui.GetForegroundWindow()
        # set DPI awareness
        win32gui.MoveWindow(hwnd, left, top, ceil(1 * self.width), ceil(1 * self.height), True)
    
        # create a device context 
        self.desktop_dc = win32gui.GetWindowDC(self.hdesktop) 
        self.img_dc = win32ui.CreateDCFromHandle(self.desktop_dc) 
        
        # create a memory based device context 
        self.mem_dc = self.img_dc.CreateCompatibleDC() 

        time.sleep(1)

    def mouseLeftDown (self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)

    def mouseLeftUp (self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

    def mouseMove (self, x, y):
        win32api.SetCursorPos((x,y))

    def capture (self, show=False):

        # create a bitmap object 
        self.screenshot = win32ui.CreateBitmap() 
        self.screenshot.CreateCompatibleBitmap(self.img_dc, self.width, self.height) 
        self.mem_dc.SelectObject(self.screenshot) 
        
        # copy the screen into our memory device context 
        self.mem_dc.BitBlt((0, 0), (self.width, self.height), self.img_dc, (self.left, self.top), win32con.SRCCOPY) 
        
        # convert to PIL Image
        bmpinfo = self.screenshot.GetInfo()
        bmpstr = self.screenshot.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        if show: 
            im.show()

        return im
        #return np.array(im)

    def __del__ (self):        
        # free our objects 
        if self.mem_dc != None and self.screenshot != None:
            self.mem_dc.DeleteDC() 
            win32gui.DeleteObject(self.screenshot.GetHandle())