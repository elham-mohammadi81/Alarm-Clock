from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QPushButton, QScrollArea, QWidget, QVBoxLayout
from PyQt5 import uic
from create_alarm import Create_Alarm
from alarm_ringing import Alarm_Ringing
from Pomodoro import Pomodoro
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtMultimedia import QMediaPlayer
import sys
from datetime import datetime, timedelta

class Alarm_Clock(QMainWindow):

    # Custom signal emitted when an alarm rings (time, name, song)
    alarm_ring = pyqtSignal(str, str, str)

    def __init__(self):
        super(Alarm_Clock, self).__init__()

        # Load the .ui file created in Qt Designer
        uic.loadUi("G:\Python\Projects\Alarm Clock\Alarm_clock.ui", self)

        # Find all required widgets by object name from the .ui file
        self.ScrollArea = self.findChild(QScrollArea, "scrollArea")
        self.Qframe1 = self.findChild(QFrame, "frame")
        self.Qframe2 = self.findChild(QFrame, "frame_2")
        self.Qframe3 = self.findChild(QFrame, "frame_3")

        self.alarm_title_label = self.findChild(QLabel, "alarm_title_label")
        self.alarm_label = self.findChild(QLabel, "alarm_label")
        self.user_alarm_label = self.findChild(QLabel, "user_alarm_label")
        self.date = self.findChild(QLabel, "Date")

        self.Alarm_Clock_Button = self.findChild(QPushButton, "alarm_clock_Button")
        self.World_Clock_Button = self.findChild(QPushButton, "world_clock_Button")
        self.Pomodoro_Clock_Button = self.findChild(QPushButton, "Pomodoro_Button")
        self.Create_New_Alarm_Button = self.findChild(QPushButton, "Create_new_alarm_Button")
        self.Quick_Alarm_5_Button = self.findChild(QPushButton, "Quick_alarm_5_Button")
        self.Quick_Alarm_10_Button = self.findChild(QPushButton, "Quick_alarm_10_Button")
        self.Quick_Alarm_15_Button = self.findChild(QPushButton, "Quick_alarm_15_Button")
        self.Quick_Alarm_30_Button = self.findChild(QPushButton, "Quick_alarm_30_Button")
        self.Quick_Alarm_1h_Button = self.findChild(QPushButton, "Quick_alarm_1h_Button")

        self.label = self.findChild(QLabel, "label")

        # Scroll area setup to hold alarms dynamically
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_layout.setSpacing(10)
        self.scroll_layout.setContentsMargins(10, 10, 10, 10)
        self.scroll_layout.addWidget(self.user_alarm_label, alignment=Qt.AlignCenter)  # Title "Your Alarms"
        self.scroll_widget.setLayout(self.scroll_layout)
        self.ScrollArea.setWidget(self.scroll_widget)
        self.ScrollArea.setWidgetResizable(True)

        # Timer to update clock every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_time)
        self.timer.start(1000)

        # Timer to check alarms every second
        self.check_timer = QTimer()
        self.check_timer.timeout.connect(self.check_alarms)

        # Set current date at startup
        self.time = datetime.now()
        date_string = self.time.strftime("%A ,%B %d , %Y")
        self.date.setText(date_string)
        self.show_time()

        # Connect buttons
        self.Create_New_Alarm_Button.clicked.connect(self.Open_Create_page)
        self.Pomodoro_Clock_Button.clicked.connect(self.Open_pomodoro_page)

        self.create_new_alarm = None

        # Quick alarm buttons (5, 10, 15, 30 minutes, 1 hour)
        self.Quick_Alarm_5_Button.clicked.connect(lambda: self.quick_alarm('5'))
        self.Quick_Alarm_10_Button.clicked.connect(lambda: self.quick_alarm('10'))
        self.Quick_Alarm_15_Button.clicked.connect(lambda: self.quick_alarm('15'))
        self.Quick_Alarm_30_Button.clicked.connect(lambda: self.quick_alarm('30'))
        self.Quick_Alarm_1h_Button.clicked.connect(lambda: self.quick_alarm('1'))

        # List to store alarms
        self.alarms = []
        # Media player for alarm sound
        self.player = QMediaPlayer()
        self.show()

    # Create quick alarm by adding minutes/hours
    def quick_alarm(self, time):
        if time == '5':
            quick_alarm = datetime.now() + timedelta(minutes=5)
        elif time == '10':
            quick_alarm = datetime.now() + timedelta(minutes=10)
        elif time == '15':
            quick_alarm = datetime.now() + timedelta(minutes=15)
        elif time == '30':
            quick_alarm = datetime.now() + timedelta(minutes=30)
        elif time == '1':
            quick_alarm = datetime.now() + timedelta(hours=1)
        
        # Add alarm to list and UI
        self.add_alarm_frame(
            quick_alarm.hour,
            quick_alarm.minute,
            'Quick Alarm',
            "G:\Python\Projects\Alarm Clock\jingle-bells-alarm-clock-version-129333.mp3"
        )

    # Open Pomodoro timer page
    def Open_pomodoro_page(self):
        self.pomodoroPage = Pomodoro()
        self.pomodoroPage.show()

    # Update digital clock and date
    def show_time(self):
        now = datetime.now()
        self.label.setText(now.strftime("%H:%M:%S"))
        self.date.setText(now.strftime("%A ,%B %d, %Y"))

    # Open create-alarm page
    def Open_Create_page(self, checked):
        if self.create_new_alarm is None or not self.create_new_alarm.isVisible():
            self.create_new_alarm = Create_Alarm()
            # Connect custom signal from Create_Alarm
            self.create_new_alarm.alarm_created.connect(self.add_alarm_frame)
        self.create_new_alarm.show()

    # Add alarm frame to scroll area and store alarm info
    def add_alarm_frame(self, hour, minutes, alarm_name, song):
        frame_alarm = QFrame(self.scroll_widget)
        frame_layout = QVBoxLayout(frame_alarm)
        frame_alarm.setStyleSheet("background-color: #F8E8EE; border-radius: 20px;")
        frame_layout.setContentsMargins(10, 10, 10, 10)

        # Alarm time label
        label_new_alarm = QLabel(f"{hour}:{minutes}", frame_alarm)
        label_new_alarm.setFont(QFont('MS Shell Dlg 2', 19))

        # Alarm name label
        label_name_alarm = QLabel(alarm_name, frame_alarm)
        label_name_alarm.setFont(QFont('MS Shell Dlg 2', 12))

        # Delete button for alarm
        delete_button = QPushButton(frame_alarm)
        delete_button.setStyleSheet("background-color: #F8E8EE ;border-radius: 20px;")
        delete_button.setIcon(QIcon("G:/Python/Projects/Alarm Clock/Waste-Garbage-Can-Vector-PNG-Clipart.png"))

        # Add widgets to alarm frame
        frame_layout.addWidget(label_new_alarm)
        frame_layout.addWidget(label_name_alarm)
        frame_layout.addWidget(delete_button, alignment=Qt.AlignRight)
        frame_alarm.setLayout(frame_layout)
        self.scroll_layout.addWidget(frame_alarm)

        # Save alarm info
        alarm_dic = {
            "time": f"{hour}:{minutes}",
            "song_path": song,
            "name": alarm_name,
            "triggered": False,
            "frame": frame_alarm
        }
        self.alarms.append(alarm_dic)

        # Start checking alarms if not already running
        if not self.check_timer.isActive():
            self.check_timer.start(1000)

    # Check alarms every second
    def check_alarms(self):
        now = datetime.now().strftime("%H:%M")
        for alarm in self.alarms:
            # Trigger alarm if time matches and not triggered yet
            if now == alarm["time"] and alarm["triggered"] == False:
                alarm["triggered"] = True
                self.alarm_ringing = Alarm_Ringing()
                self.alarm_ring.connect(self.alarm_ringing.update_info)

                # Emit signal with alarm info
                self.alarm_ring.emit(alarm["time"], alarm["name"], alarm["song_path"])


# Run application
app = QApplication(sys.argv)
window = Alarm_Clock()
app.exec_()
