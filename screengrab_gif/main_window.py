
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QSpinBox
from PyQt5.QtCore import QTimer, QDateTime, QRect
import sys
import os
from screengrab_gif.screenshotter import capture_screen
from screengrab_gif.gif_coverter import create_gif
from screengrab_gif.settings import Settings
from screengrab_gif.ui_controls import UiControls


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Instantiate the settings
        self.settings = Settings()
        self.setWindowTitle("Screengrab GIF")

        # Instantiate the UI elements
        self.ui_elements = UiControls(self.settings)

        # Connect the signals and slots
        self.ui_elements.start_button.clicked.connect(self.start_screenshots)
        self.ui_elements.stop_button.clicked.connect(self.stop_screenshots)
        self.ui_elements.change_folder_button.clicked.connect(self.change_folder)
        self.ui_elements.open_folder_button.clicked.connect(lambda: os.startfile(self.settings.screenshot_folder))
        # self.ui_elements.delete_screenshots_button.clicked.connect(self.delete_screenshots)
        # self.ui_elements.create_gif_button.clicked.connect(self.create_gif)
        self.ui_elements.change_extent_button.clicked.connect(lambda value: self.change_extent())

        # Track the mouse position
        self.mouse_timer = QTimer()
        self.mouse_timer.timeout.connect(self.track_mouse)
        self.mouse_timer.start(100)

        # Colour the extent buttons red when modified
        self.ui_elements.extent_left_spinbox.valueChanged.connect(lambda value: self.extent_value_not_saved(self.ui_elements.extent_left_spinbox))
        self.ui_elements.extent_top_spinbox.valueChanged.connect(lambda value: self.extent_value_not_saved(self.ui_elements.extent_top_spinbox))
        self.ui_elements.extent_width_spinbox.valueChanged.connect(lambda value: self.extent_value_not_saved(self.ui_elements.extent_width_spinbox))
        self.ui_elements.extent_height_spinbox.valueChanged.connect(lambda value: self.extent_value_not_saved(self.ui_elements.extent_height_spinbox))

        # add a screen_extent_grabber widget to the layout
        from screengrab_gif.ScreenExtentWidget import ScreenExtentGrabber
        self.screen_extent_grabber = ScreenExtentGrabber(self)
        self.screen_extent_grabber.set_main_window_handle(self)
        self.ui_elements.grab_extent_button.clicked.connect(self.start_capture_extent)

        # Display the elements on the screen
        self.setCentralWidget(self.ui_elements)
        self.layout = QVBoxLayout()  # type: ignore
        self.layout.addWidget(self.ui_elements)

        # Resize the window to fit the controls
        self.resize(650, 410)

    def start_capture_extent(self):
        # Resize the screen extent grabber layout to cover the entire screen
        self.screen_extent_grabber.resize(QApplication.desktop().screenGeometry().width(), QApplication.desktop().screenGeometry().height())
        # Make the screen extent grabber widget transparent
        self.screen_extent_grabber.setWindowOpacity(0.125)
        # Show the screen extent grabber widget
        self.screen_extent_grabber.show()

    def capture_extent_updated(self, extent_rect):
        # Do something with the capture extent rectangle
        # print("Capture extent updated:", extent_rect)
        self.change_extent(extent_rect)

    def track_mouse(self):
        # Get the mouse position
        mouse_position = QApplication.desktop().cursor().pos()

        # Update the mouse position label
        self.ui_elements.mouse_position_label.setText(f"Mouse Position: {mouse_position.x()}, {mouse_position.y()}")

    def extent_value_not_saved(self, eleChanged: QSpinBox = None):  # type: ignore
        self.ui_elements.change_extent_button.setStyleSheet("background-color: red")
        # if an element is provided, change its background colour to red
        if eleChanged is not None:
            eleChanged.setStyleSheet("background-color: red")

    def change_folder(self):
        new_folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if new_folder:
            self.settings.screenshot_folder = new_folder

    def delete_screenshots(self):
        # Get the file extension for screenshots
        file_extension = self.settings.screenshot_file_format.lower()

        # Delete all the screenshots in the output folder
        for file_name in os.listdir(self.settings.screenshot_folder):
            if file_name.endswith(file_extension):
                os.remove(os.path.join(self.settings.screenshot_folder, file_name))

    def start_screenshots(self):
        self.ui_elements.start_button.setEnabled(False)
        self.ui_elements.stop_button.setEnabled(True)

        # Get the values from the controls
        self.settings.capture_duration = self.ui_elements.duration_spinbox.value()
        self.settings.capture_interval = self.ui_elements.interval_spinbox.value()
        self.settings.start_delay = self.ui_elements.start_delay_spinbox.value()

        # Wait for the specified delay before starting the screenshots
        self.ui_elements.info_label.setText("Waiting for delay...")
        QTimer.singleShot(self.settings.start_delay, self.start_screenshots_delayed)

    def start_screenshots_delayed(self):
        self.ui_elements.info_label.setText("Capturing screenshots...")
        # Delete all the existing screenshots in the output folder
        self.delete_screenshots()

        # Start the timer to capture screenshots at the specified interval
        self.interval_timer = QTimer(self)
        self.interval_timer.start(self.settings.capture_interval)
        self.interval_timer.timeout.connect(self.capture_screenshot)

        # Start the stop timer to stop capturing after the specified duration
        self.stop_timer = QTimer(self)
        self.stop_timer.setSingleShot(True)
        self.stop_timer.timeout.connect(self.stop_screenshots)
        self.stop_timer.start(self.settings.capture_duration * 1000)

    def stop_screenshots(self):
        self.ui_elements.start_button.setEnabled(True)
        self.ui_elements.stop_button.setEnabled(False)
        self.ui_elements.info_label.setText("Screenshots stopped.")

        # Stop the timers
        self.interval_timer.stop()
        self.stop_timer.stop()

        # Convert the captured screenshots to a GIF
        self.create_gif()

    def create_gif(self):
        # Update the info label
        self.ui_elements.info_label.setText("Creating GIF...")
        # Create a GIF from the screenshots
        create_gif(self.settings.screenshot_folder, self.settings.capture_duration)
        # Update the info label
        self.ui_elements.info_label.setText("GIF created.")

    def capture_screenshot(self):
        # Generate the screenshot file path with timestamp
        current_datetime = QDateTime.currentDateTime().toString("yyyy-MM-dd_hh-mm-ss-zzz")
        screenshot_path = os.path.join(self.settings.screenshot_folder, f"{current_datetime}")
        # Capture a screenshot and save it to the specified file
        capture_screen(screenshot_path, self.settings.capture_extent)

    def change_extent(self, newExtent: QRect = QRect()):
        # check if a newExtent was passed in
        if newExtent == QRect():
            # Get the values from the controls
            self.settings.capture_extent = QRect(
                self.ui_elements.extent_left_spinbox.value(),
                self.ui_elements.extent_top_spinbox.value(),
                self.ui_elements.extent_width_spinbox.value(),
                self.ui_elements.extent_height_spinbox.value()
            )
        else:
            self.settings.capture_extent = newExtent

        # Update the extent values in the UI. Capture extent is a QRect object, so we can use its methods
        self.ui_elements.extent_top_spinbox.setValue(self.settings.capture_extent.top())
        self.ui_elements.extent_left_spinbox.setValue(self.settings.capture_extent.left())
        self.ui_elements.extent_width_spinbox.setValue(self.settings.capture_extent.width())
        self.ui_elements.extent_height_spinbox.setValue(self.settings.capture_extent.height())

        # Set their background colour back to normal
        self.ui_elements.extent_top_spinbox.setStyleSheet("")
        self.ui_elements.extent_left_spinbox.setStyleSheet("")
        self.ui_elements.extent_width_spinbox.setStyleSheet("")
        self.ui_elements.extent_height_spinbox.setStyleSheet("")
        self.ui_elements.change_extent_button.setStyleSheet("")

        # Update the extent info label
        # self.ui_elements.extent_label.setText(str(self.settings.capture_extent))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
