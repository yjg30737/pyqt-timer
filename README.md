# pyqt-timer
Simple timer made out of PyQt

## Requirements
PyQt5 >= 5.8

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-timer.git --upgrade```

## Included Package
* <a href="https://github.com/yjg30737/pyqt-notifier.git">pyqt-notifier</a>
* <a href="https://github.com/yjg30737/pyqt-resource-helper.git">pyqt-resource-helper</a>
* <a href="https://github.com/yjg30737/pyqt-timer-label.git">pyqt-timer-label</a> - since v0.2.0

## Usage
* Being able to play/pause/stop the timer after complete the timer settings (press the settings icon or double-click the label(00:00:00)
* When time is over, notifier will show up at the bottom right of the system background. Refresh button on the notifier make the timer operate itself again.

## Example

### Code Example
```python
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    timerGadget = Timer()
    timerGadget.show()
    app.exec_()
```

### Result

Timer

![image](https://user-images.githubusercontent.com/55078043/146874279-76c99dd7-5754-414d-92ff-7a52435aa7a9.png)

Timer settings dialog

![image](https://user-images.githubusercontent.com/55078043/146874301-15e60c7c-f596-43bb-bf2f-16dd0ecc09a7.png)

Ticking timer

![image](https://user-images.githubusercontent.com/55078043/146874339-df61f867-c4c1-4212-8650-9a306324347e.png)

## Note
When time is over pyqt-notifier window will pop up.

This package make new file(timerSettings.ini) in main script to save the hour, minute, second chosen by user.

## See also
* <a href="https://github.com/yjg30737/pyqt-timer-label.git">pyqt-timer-label</a>
* <a href="https://github.com/yjg30737/pyqt-transparent-timer.git">pyqt-transparent-timer</a>
