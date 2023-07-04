from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSpinBox, QFormLayout
from PyQt5.QtCore import Qt


class UiControls(QWidget):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings
        self.layout = QFormLayout()  # type: ignore

        # Start and stop buttons. Add these as small, horizontal buttons.
        self.start_button = QPushButton("Start")
        self.start_button.setEnabled(True)
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)
        hbox = QHBoxLayout()
        hbox.addWidget(self.start_button)
        hbox.addWidget(self.stop_button)
        self.layout.addRow(hbox)

        # Time controls
        self.duration_spinbox = QSpinBox()
        self.duration_spinbox.setMinimum(1)
        self.duration_spinbox.setMaximum(60)
        self.duration_spinbox.setValue(self.settings.capture_duration)
        self.layout.addRow("Duration (s):", self.duration_spinbox)

        self.interval_spinbox = QSpinBox()
        self.interval_spinbox.setMinimum(10)
        self.interval_spinbox.setMaximum(1000)
        self.interval_spinbox.setValue(self.settings.capture_interval)
        self.layout.addRow("Interval (ms):", self.interval_spinbox)

        self.start_delay_spinbox = QSpinBox()
        self.start_delay_spinbox.setMinimum(0)
        self.start_delay_spinbox.setMaximum(10000)
        self.start_delay_spinbox.setValue(self.settings.start_delay)
        self.layout.addRow("Start delay (ms):", self.start_delay_spinbox)

        # Add a row of space in between the time controls and the extent controls
        self.layout.addRow(QLabel(" "))

        # Add some labels to describe the extent controls
        hBoxExtentLabels = QHBoxLayout()
        hBoxExtentLabels.addWidget(QLabel("Top"))
        hBoxExtentLabels.addWidget(QLabel("Left"))
        hBoxExtentLabels.addWidget(QLabel("Width"))
        hBoxExtentLabels.addWidget(QLabel("Height"))
        self.layout.addRow(hBoxExtentLabels)

        # 4 elements: top, left, width, height
        self.extent_top_spinbox = QSpinBox()
        self.extent_top_spinbox.setMinimum(0)
        self.extent_top_spinbox.setMaximum(10000)
        self.extent_top_spinbox.setValue(self.settings.capture_extent.top())

        self.extent_left_spinbox = QSpinBox()
        self.extent_left_spinbox.setMinimum(0)
        self.extent_left_spinbox.setMaximum(10000)
        self.extent_left_spinbox.setValue(self.settings.capture_extent.left())

        self.extent_width_spinbox = QSpinBox()
        self.extent_width_spinbox.setMinimum(0)
        self.extent_width_spinbox.setMaximum(10000)
        self.extent_width_spinbox.setValue(self.settings.capture_extent.width())

        self.extent_height_spinbox = QSpinBox()
        self.extent_height_spinbox.setMinimum(0)
        self.extent_height_spinbox.setMaximum(10000)
        self.extent_height_spinbox.setValue(self.settings.capture_extent.height())

        extentHBox = QHBoxLayout()
        extentHBox.addWidget(self.extent_top_spinbox)
        extentHBox.addWidget(self.extent_left_spinbox)
        extentHBox.addWidget(self.extent_width_spinbox)
        extentHBox.addWidget(self.extent_height_spinbox)
        self.layout.addRow(extentHBox)

        self.change_extent_button = QPushButton("Change Extent from Input Boxes")
        # self.layout.addRow(self.extent_label, self.change_extent_button)
        self.layout.addRow(self.change_extent_button)

        # Button for grabbing the extent
        self.grab_extent_button = QPushButton("Grab Extent via Mouse")
        self.layout.addRow(self.grab_extent_button)

        # Add a row of space in between the extent controls and the folder controls
        self.layout.addRow(QLabel(" "))

        # Folder controls
        self.screenshot_folder_label = QLabel(self.settings.screenshot_folder)
        self.screenshot_folder_label.setWordWrap(True)
        self.change_folder_button = QPushButton("Change Extent")

        hboxFolder = QHBoxLayout()
        hboxFolder.addWidget(self.screenshot_folder_label)
        hboxFolder.addWidget(self.change_folder_button)
        self.layout.addRow("Output folder:", hboxFolder)

        self.open_folder_button = QPushButton("Open Output Folder")
        self.layout.addRow(self.open_folder_button)

        # self.delete_screenshots_button = QPushButton("Delete Screenshots")
        # self.layout.addRow(self.delete_screenshots_button)

        # self.create_gif_button = QPushButton("Create GIF")
        # self.layout.addRow(self.create_gif_button)

        # Add a row of space in between the folder controls and the info label
        self.layout.addRow(QLabel(" "))

        # Info label
        self.info_label = QLabel("Ready")
        # Centre and make big
        self.info_label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.info_label.setStyleSheet("font-size: 20px")
        self.layout.addRow(self.info_label)

        # Add a row of space in between the info label and the mouse position label
        self.layout.addRow(QLabel(" "))

        # Label at the bottom for mouse x and y coordinates
        self.mouse_position_label = QLabel("Mouse position: n/a")
        # Put this on the right side
        hboxMousePos = QHBoxLayout()
        hboxMousePos.addStretch(1)
        hboxMousePos.addWidget(self.mouse_position_label)
        self.layout.addRow(hboxMousePos)

        # Set the layout
        self.setLayout(self.layout)
