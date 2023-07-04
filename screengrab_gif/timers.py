from PyQt5.QtCore import QTimer


class Timers:
    def __init__(self):
        self.interval_timer = QTimer()

        self.start_delay_timer = QTimer()
        self.start_delay_timer.setSingleShot(True)

        self.stop_timer = QTimer()
        self.stop_timer.setSingleShot(True)
