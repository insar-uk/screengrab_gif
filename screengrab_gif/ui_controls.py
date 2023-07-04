from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QSpinBox, QFormLayout


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

        # Extent controls
        # self.extent_label = QLabel()
        # self.extent_label.setWordWrap(True)
        # self.extent_label.setText("Extent: " + str(self.settings.capture_extent))
        # # button to drag the extent
        self.change_extent_button = QPushButton("Change")
        # self.layout.addRow(self.extent_label, self.change_extent_button)
        self.layout.addRow(self.change_extent_button)

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

        # Button for grabbing the extent
        self.grab_extent_button = QPushButton("Grab Extent")
        self.layout.addRow(self.grab_extent_button)

        # Folder controls
        self.screenshot_folder_label = QLabel(self.settings.screenshot_folder)
        self.screenshot_folder_label.setWordWrap(True)
        self.change_folder_button = QPushButton("Change Extent")

        hbox = QHBoxLayout()
        hbox.addWidget(self.screenshot_folder_label)
        hbox.addWidget(self.change_folder_button)
        self.layout.addRow("Output folder:", hbox)

        self.open_folder_button = QPushButton("Open Output Folder")
        self.layout.addRow(self.open_folder_button)

        self.delete_screenshots_button = QPushButton("Delete Screenshots")
        self.layout.addRow(self.delete_screenshots_button)

        self.create_gif_button = QPushButton("Create GIF")
        self.layout.addRow(self.create_gif_button)

        # Info label
        self.info_label = QLabel("Ready")
        self.layout.addRow(self.info_label)

        # Label at the bottom for mouse x and y coordinates
        self.mouse_position_label = QLabel("Mouse position: n/a")
        # Put this on the right side
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.mouse_position_label)
        self.layout.addRow(hbox)

        # Set the layout
        self.setLayout(self.layout)
