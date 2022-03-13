import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QDialog, QSizePolicy, QHBoxLayout, QVBoxLayout
from PyQt5.QtCore import Qt, QTime, pyqtSignal, QSettings

from pyqt_notifier.pyqtNotifier import NotifierWidget
from pyqt_timer.settingsDialog.settingsDialog import SettingsDialog
from pyqt_timer_label.timerLabel import TimerLabel
from pyqt_svg_icon_pushbutton import SvgIconPushButton


class Timer(QWidget):
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

        self.__startPauseBtn = SvgIconPushButton()
        self.__stopBtn = SvgIconPushButton()
        self.__settingsBtn = SvgIconPushButton()

        self.__startPauseBtn.setToolTip('Start')
        self.__stopBtn.setToolTip('Stop')
        self.__settingsBtn.setToolTip('Settings')

        btns = [self.__startPauseBtn, self.__stopBtn, self.__settingsBtn]

        self.__startPauseBtn.setIcon('ico/play.svg')
        self.__stopBtn.setIcon('ico/stop.svg')
        self.__settingsBtn.setIcon('ico/settings.svg')

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignCenter)
        for btn in btns:
            btn.setMaximumWidth(btn.sizeHint().width())
            lay.addWidget(btn)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        self.__timerLbl = TimerLabel()
        self.__timerLbl.doubleClicked.connect(self.__settings)
        self.__timerLbl.resetSignal.connect(self.__reset)
        self.__timerLbl.stopped.connect(self.__stop)

        lay = QVBoxLayout()
        lay.addWidget(self.__timerLbl)
        lay.addWidget(bottomWidget)

        self.setLayout(lay)

        self.__timerInit()

    def __timerInit(self):
        self.__startPauseBtn.setObjectName('start')

        self.__startPauseBtn.clicked.connect(self.__start)
        self.__stopBtn.clicked.connect(self.__timerLbl.reset)
        self.__settingsBtn.clicked.connect(self.__settings)

        self.__timerLbl.setStartHour(self.__hour)
        self.__timerLbl.setStartMinute(self.__min)
        self.__timerLbl.setStartSecond(self.__sec)

        self.__startPauseBtn.setEnabled(False)
        self.__stopBtn.setEnabled(False)

    def __start(self):
        try:
            if self.__startPauseBtn.objectName() == 'start':
                self.__prepare()
                self.__timerLbl.start()
                self.__startPauseBtn.setObjectName('pause')
                self.__startPauseBtn.setIcon('ico/pause.svg')
                self.__startPauseBtn.clicked.connect(self.__pauseOrRestart)
                self.__stopBtn.setEnabled(True)
        except Exception as e:
            print(e)
            print(sys.exc_info()[2].tb_lineno)
            print(sys.exc_info())

    def __prepare(self):
        self.__settingsBtn.setEnabled(False)
        self.__timerLbl.doubleClicked.disconnect(self.__settings)

    def __pauseOrRestart(self):
        try:
            if self.__startPauseBtn.objectName() == 'pause':
                self.__timerLbl.pause()
                self.__startPauseBtn.setIcon('ico/play.svg')
                self.__startPauseBtn.setToolTip('Restart')
                self.__startPauseBtn.setObjectName('restart')
            elif self.__startPauseBtn.objectName() == 'restart':
                self.__timerLbl.restart()
                self.__startPauseBtn.setIcon('ico/pause.svg')
                self.__startPauseBtn.setToolTip('Pause')
                self.__startPauseBtn.setObjectName('pause')
        except Exception as e:
            print(e)

    def __notifyTimesUp(self):
        self.__notifier = NotifierWidget('Notice', 'Times up.')
        notifierRefreshBtn = QPushButton('Restart')
        notifierRefreshBtn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        notifierRefreshBtn.clicked.connect(self.__start)
        self.__notifier.addWidgets([notifierRefreshBtn])
        self.__notifier.show()

    def __reset(self):
        self.__startPauseBtn.setToolTip('Start')
        self.__startPauseBtn.setObjectName('start')
        self.__startPauseBtn.setIcon('ico/play.svg')

        self.__startPauseBtn.clicked.disconnect(self.__pauseOrRestart)
        self.__startPauseBtn.clicked.connect(self.__start)

        self.__settingsBtn.setEnabled(True)
        self.__stopBtn.setEnabled(False)

        self.__timerLbl.doubleClicked.connect(self.__settings)

    def __stop(self):
        try:
            self.__reset()
            self.__notifyTimesUp()
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

            self.__timerLbl.setText(task_time_text)
            self.__startPauseBtn.setEnabled(task_time_text != '00:00:00')