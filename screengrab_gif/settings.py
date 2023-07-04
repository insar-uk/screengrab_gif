import os
from PyQt5.QtCore import QRect


class Settings:
    def __init__(self):
        self.capture_duration = 3  # Duration of screenshot capture in seconds
        self.capture_interval = 200  # Interval between each screenshot in milliseconds
        self.gif_file_name = "captured_screenshots.gif"  # Name of the output GIF file
        self.screenshot_file_name = "screenshot"  # Name of the screenshot files
        self.screenshot_file_format = "png"  # Format of the screenshot files
        # folder where the screenshots will be saved
        self.screenshot_folder = os.path.join(os.getcwd(), 'screenshots')
        # Delay before starting the screenshot capture in milliseconds
        self.start_delay = 0

        # self.capture_extent = Qt.QApplication.primaryScreen().availableGeometry()  # Type is QRect
        self.capture_extent = QRect(0, 0, 500, 500)  # Type is QRect

    def set_capture_extent(self, capture_extent: QRect):
        self.capture_extent = capture_extent
