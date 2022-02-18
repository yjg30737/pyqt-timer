from setuptools import setup, find_packages

setup(
    name='pyqt-timer',
    version='0.1.0',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    package_data={'pyqt_timer.style': ['button.css'], 'pyqt_timer.ico': ['play.png', 'pause.png', 'stop.png', 'settings.png']},
    description='Simple timer made out of PyQt',
    url='https://github.com/yjg30737/pyqt-timer.git',
    install_requires=[
        'PyQt5>=5.8',
        'pyqt-resource-helper @ git+https://git@github.com/yjg30737/pyqt-resource-helper.git@main',
        'pyqt-notifier @ git+https://git@github.com/yjg30737/pyqt-notifier.git@main',
        'pyqt-timer-label @ git+https://git@github.com/yjg30737/pyqt-timer-label.git@main'
    ]
)