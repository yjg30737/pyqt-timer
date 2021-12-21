import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QSizePolicy, QApplication, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTime, QTimer, pyqtSignal, QSettings

from pyqt_resource_helper.pyqtResourceHelper import PyQtResourceHelper
from pyqt_notifier.pyqtNotifier import NotifierWidget
from pyqt_timer.settingsDialog.settingsDialog import SettingsDialog
from pyqt_timer.timerLabel import TimerLabel


class TimerGadget(QWidget):
    printSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__settings_struct = QSettings('timerSettings.ini', QSettings.IniFormat)
        self.__hour = int(self.__settings_struct.value('hour', 0))
        self.__min = int(self.__settings_struct.value('min', 0))
        self.__sec = int(self.__settings_struct.value('sec', 0))
        self.__initUi()

    def __initUi(self):
        self.setWindowFlags(Qt.WindowCloseButtonHint)

        self.__startPauseBtn = QPushButton()
        self.__stopBtn = QPushButton()
        self.__settingsBtn = QPushButton()

        self.__startPauseBtn.setToolTip('Start')
        self.__stopBtn.setToolTip('Stop')
        self.__settingsBtn.setToolTip('Settings')

        btns = [self.__startPauseBtn, self.__stopBtn, self.__settingsBtn]

        PyQtResourceHelper.setStyleSheet(btns, ['style/button.css'])
        PyQtResourceHelper.setIcon(btns, ['ico/play.png', 'ico/stop.png', 'ico/settings.png'])

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignCenter)
        for btn in btns:
            btn.setMaximumWidth(btn.sizeHint().width())
            lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        self.__timer_lbl = TimerLabel()
        self.__timer_lbl.doubleClicked.connect(self.__settings)

        lay = QVBoxLayout()
        lay.addWidget(self.__timer_lbl)
        lay.addWidget(bottomWidget)

        self.setLayout(lay)

        self.__timerInit()

    def __timerInit(self):
        self.__startPauseBtn.setObjectName('start')

        self.__startPauseBtn.clicked.connect(self.__start)
        self.__stopBtn.clicked.connect(self.__stop)
        self.__settingsBtn.clicked.connect(self.__settings)

        self.__taskTimeLeft = QTime(self.__hour, self.__min, self.__sec)
        self.__timer = QTimer(self)

        self.__startPauseBtn.setEnabled(False)
        self.__stopBtn.setEnabled(False)

    def __start(self):
        try:
            if self.__startPauseBtn.objectName() == 'start':
                # adding action to timer
                self.__timer.timeout.connect(self.__timer_ticking)
                self.__timer.singleShot(self.__taskTimeLeft.msec(), self.__prepare_to_timer)
                # update the timer every second
                self.__timer.start(1000)
                self.__startPauseBtn.setObjectName('pause')
                PyQtResourceHelper.setIcon([self.__startPauseBtn], ['ico/pause.png'])
                self.__startPauseBtn.clicked.connect(self.__pause_and_restart)

                self.__stopBtn.setEnabled(True)
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

    def __prepare_to_timer(self):
        self.__settingsBtn.setEnabled(False)
        self.__timer_lbl.doubleClicked.disconnect(self.__settings)
        self.__timer_ticking()

    def __pause_and_restart(self):
        try:
            if self.__startPauseBtn.objectName() == 'pause':
                self.__timer.stop()
                PyQtResourceHelper.setIcon([self.__startPauseBtn], ['ico/play.png'])
                self.__startPauseBtn.setObjectName('restart')
            elif self.__startPauseBtn.objectName() == 'restart':
                self.__timer.start()
                PyQtResourceHelper.setIcon([self.__startPauseBtn], ['ico/pause.png'])
                self.__startPauseBtn.setObjectName('pause')
        except Exception as e:
            print(e)

    def __notify_times_up(self):
        self.__notifier = NotifierWidget('Notice', 'Times up.')
        refreshBtn = QPushButton('Restart')
        refreshBtn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        refreshBtn.clicked.connect(self.__start)
        self.__notifier.addWidgets([refreshBtn])
        self.__notifier.show()

    def __timer_ticking(self):
        try:
            self.__taskTimeLeft = self.__taskTimeLeft.addSecs(-1)
            time_left_text = self.__taskTimeLeft.toString('hh:mm:ss')
            self.__timer_lbl.setText(time_left_text)
            if '23:59:59' == time_left_text:
                self.__notify_times_up()
                self.__stop()
            else:
                pass
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

    def __stop(self):
        try:
            self.__taskTimeLeft = QTime(self.__hour, self.__min, self.__sec)
            self.__timer_lbl.setText(self.__taskTimeLeft.toString("hh:mm:ss"))

            self.__timer.stop()

            self.__startPauseBtn.setObjectName('start')
            PyQtResourceHelper.setIcon([self.__startPauseBtn], ['ico/play.png'])

            self.__timer.timeout.disconnect(self.__timer_ticking)
            self.__startPauseBtn.clicked.disconnect(self.__pause_and_restart)
            self.__startPauseBtn.clicked.connect(self.__start)

            self.__settingsBtn.setEnabled(True)
            self.__stopBtn.setEnabled(False)

            self.__timer_lbl.doubleClicked.connect(self.__settings)

        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

    def __settings(self):
        dialog = SettingsDialog()
        reply = dialog.exec()
        if reply == QDialog.Accepted:

            self.__hour, self.__min, self.__sec = dialog.get_time()

            # self.__show_event_f = dialog.get_show_event_list_flag()
            self.__taskTimeLeft = QTime(self.__hour, self.__min, self.__sec)
            task_time_text = self.__taskTimeLeft.toString('hh:mm:ss')

            self.__timer_lbl.setText(task_time_text)
            self.__startPauseBtn.setEnabled(task_time_text != '00:00:00')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    timerGadget = TimerGadget()
    timerGadget.show()
    app.exec_()