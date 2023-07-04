# use window32 api to capture screen
import win32gui # noqa
import win32ui
import win32con
import win32api

from PyQt5.QtCore import QRect


def capture_screen(filename='screenshot', extent=None):
    # get window handle
    hWnd = win32gui.GetDesktopWindow()

    # get window size
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    # If extent is not specified, capture the entire screen
    if extent is not None:
        if isinstance(extent, QRect):  # Check if its QRect
            left, top, width, height = extent.getRect()
        elif len(extent) == 4:  # Check if its a list of 4 elements
            left, top, width, height = extent
        else:
            raise ValueError('Extent must be a QRect or a list of 4 elements')

    # create device context
    hDC = win32gui.GetWindowDC(hWnd)
    srcDC = win32ui.CreateDCFromHandle(hDC)

    # create compatible dc
    memDC = srcDC.CreateCompatibleDC()

    # create bitmap
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcDC, width, height)
    memDC.SelectObject(bmp)
    memDC.BitBlt((0, 0), (width, height), srcDC, (left, top), win32con.SRCCOPY)

    # convert bitmap to png
    bmp.SaveBitmapFile(memDC, filename + '.png')

    # release
    memDC.DeleteDC()
    win32gui.DeleteObject(bmp.GetHandle())
