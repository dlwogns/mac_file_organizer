from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'iconfile': 'icon.icns',
    'packages': [
    'watchdog',
    'PyQt5'
    ],
    'includes': [
    'sip',
    'PyQt5',
    'PyQt5.sip',
    'PyQt5.QtCore',
    'PyQt5.QtGui',
    'PyQt5.QtWidgets',
    'jaraco.text'
    ],
    'plist': {
        'CFBundleName': 'Auto File Organizer',
        'CFBundleDisplayName': 'Auto File Organizer',
        'CFBundleIdentifier': 'com.yourname.autofileorganizer',
        'CFBundleVersion': '1.0.0',
        'LSUIElement': False  # True면 메뉴바 전용
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
