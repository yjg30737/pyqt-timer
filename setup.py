from setuptools import setup, find_packages

setup(
    name='pyqt-timer',
    version='0.5.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_timer.ico': ['pause.svg', 'play.svg', 'refresh.svg', 'settings.svg', 'stop.svg']},
    description='Simple timer made out of PyQt',
    url='https://github.com/yjg30737/pyqt-timer.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-notifier>=0.0.1',
        'pyqt-timer-label>=0.0.1',
        'pyqt-svg-button>=0.0.1'
    ]
)