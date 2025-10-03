from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QLabel, QPushButton
from PyQt5 import uic
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import sys 


class Alarm_Ringing(QMainWindow):
    def __init__(self):
        super(Alarm_Ringing, self).__init__()

        # Load the UI file
        uic.loadUi("G:/Python/Projects/Alarm Clock/alarm_ringing.ui", self)

        # Find widgets from the UI
        self.frame = self.findChild(QFrame, "frame")

        # Labels for alarm info
        self.alarm_ringing_label = self.findChild(QLabel, "alarm_ringing_label")
        self.alarm_name_cl = self.findChild(QLabel, "alarm_name")
        self.alarm_time_cl = self.findChild(QLabel, "alarm_time")

        # Stop button
        self.stop_alarm = self.findChild(QPushButton, "pushButton")

        # Connect stop button to close method
        self.stop_alarm.clicked.connect(self.close_)

        self.alarm_ring_win = None

        # Media player for alarm sound
        self.player = QMediaPlayer()

    # Update UI with alarm info and start playing sound
    def update_info(self, time, name, song_path):
        print(time, name, song_path)  # Debugging log
        self.alarm_time_cl.setText(time)   # Show alarm time
        self.alarm_name_cl.setText(name)   # Show alarm name

        self.show()  # Display the ringing window
        
        # Load the alarm sound
        url = QUrl.fromLocalFile(song_path)
        content = QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()  # Play alarm sound

    # Stop alarm sound and close window
    def close_(self):
        self.close()
        self.player.stop()
 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Alarm_Ringing()
    window.show()
    sys.exit(app.exec_())
