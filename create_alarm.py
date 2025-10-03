from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QFrame, QLineEdit, QRadioButton
from PyQt5 import uic
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys 


class Create_Alarm(QMainWindow):

    # Custom signal: emits (hour, minutes, alarm_name, song_path)
    alarm_created = pyqtSignal(str, str, str, str)

    def __init__(self):
        super(Create_Alarm, self).__init__()

        # Load the UI file
        uic.loadUi("Create_Alarm.ui", self)

        # Define widgets
        self.frame = self.findChild(QFrame, "frame")
        self.frame_2 = self.findChild(QFrame, "frame_3")

        # Labels
        self.create_alarm_label = self.findChild(QLabel, "create_label")
        self.alarm_time_label = self.findChild(QLabel, "alarm_time_label")
        self.alarm_title_label = self.findChild(QLabel, "alarm_title_label")
        self.alarm_sound_label = self.findChild(QLabel, "alarm_sound_label")

        # ComboBoxes for time selection
        self.hour_comboBox = self.findChild(QComboBox, "hour_comboBox")
        self.minuts_comboBox = self.findChild(QComboBox, "minuts_comboBox")

        # Alarm title input
        self.alarm_title = self.findChild(QLineEdit, "alarm_title")
        
        # Song selection
        self.song = self.findChild(QComboBox, "song")

        # Buttons
        self.Play_unplay = self.findChild(QPushButton, "play_unplay")
        self.Cancel = self.findChild(QPushButton, "cancel_button")
        self.Set_alarm = self.findChild(QPushButton, "set_alarm_button")
        self.Clock_Button = self.findChild(QPushButton, "Clock_button")

        # Repeat option
        self.repeat_daily_RB = self.findChild(QRadioButton, "repeat_day_radioButton")

        # Connect Cancel button to close the window
        self.Cancel.clicked.connect(self.close)
        # When hour changes, update the minutes box
        self.hour_comboBox.currentIndexChanged.connect(self.clock)

        # Connect "Set Alarm" button to alarm creation
        self.Set_alarm.clicked.connect(self.get_alarm_time)

        # Media player for playing alarm preview
        self.player = QMediaPlayer()
        self.Play_unplay.clicked.connect(self.choice_a_song)

    # Adjust minute selection depending on chosen hour
    def clock(self, index):
        if index > 0:
            # If 24h is chosen → force minutes to 00
            if self.hour_comboBox.currentText() == '24':
                self.minuts_comboBox.setEnabled(False)
                self.minuts_comboBox.setCurrentText("00")
            else:
                # Otherwise, allow user to pick minutes
                self.minuts_comboBox.setEnabled(True)
                self.minuts_comboBox.showPopup()
                
    # Collect alarm info and emit signal
    def get_alarm_time(self):
        hour = self.hour_comboBox.currentText()
        minutes = self.minuts_comboBox.currentText()
        alarm_name = self.alarm_title.text()

        # Choose file path based on song selection
        if self.song.currentText() == ' jingle': 
            file_path = r'jingle-bells-alarm-clock-version-129333.mp3'
        elif self.song.currentText() == ' kirby':
            file_path = r'kirby-alarm-clock-127079.mp3'
        elif self.song.currentText() == ' tropical':
            file_path = r'tropical-alarm-clock-168821.mp3'

        song = file_path

        # Emit the alarm info
        self.alarm_created.emit(hour, minutes, alarm_name, song)

        # Close after setting the alarm
        self.close()
        
    # Play selected song for preview
    def choice_a_song(self):
        # Match song with file path
        if self.song.currentText().strip() == 'jingle': 
            file_path = r'jingle-bells-alarm-clock-version-129333.mp3'
        elif self.song.currentText().strip() == 'kirby':
            file_path = r'kirby-alarm-clock-127079.mp3'
        elif self.song.currentText().strip() == 'tropical':
            file_path = r'tropical-alarm-clock-168821.mp3'
  
        # Load and play song in media player
        url = QUrl.fromLocalFile(file_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

        # Stop playback when alarm is set or button is clicked again
        self.Set_alarm.clicked.connect(self.stop_)
        self.Play_unplay.clicked.connect(self.stop_)
            
    # Stop preview playback
    def stop_(self):
        self.player.stop()
        # Reset Play button connection to choice_a_song
        self.Play_unplay.clicked.connect(self.choice_a_song)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Create_Alarm()
    window.show()
    sys.exit(app.exec_())

