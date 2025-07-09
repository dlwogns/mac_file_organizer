import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QListWidget, QPushButton, QFileDialog, QHBoxLayout,
    QCheckBox, QTextEdit, QLineEdit, QSystemTrayIcon, QMenu, QAction
)
import os
import json
from watcher import FolderWatcherThread

CONFIG_FILE = "config.json"

class AutoFileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto File Organizer")
        self.setGeometry(300, 300, 400, 500)
        self.setWindowIcon(QtGui.QIcon("icon.png"))  
        self.initUI()
        self.createTrayIcon()
        self.load_config()  # 설정 불러오기

    def initUI(self):
        layout = QVBoxLayout()

        # 감시 폴더 리스트
        self.folderListLabel = QLabel("📂 감시할 폴더")
        self.folderList = QListWidget()

        btn_layout = QHBoxLayout()
        self.addFolderBtn = QPushButton("➕ 추가")
        self.removeFolderBtn = QPushButton("➖ 삭제")
        self.addFolderBtn.clicked.connect(self.addFolder)
        self.removeFolderBtn.clicked.connect(self.removeFolder)
        btn_layout.addWidget(self.addFolderBtn)
        btn_layout.addWidget(self.removeFolderBtn)

        # [폴더이름] 규칙 ON/OFF
        self.bracketRuleCheck = QCheckBox("[폴더이름] 규칙 활성화")
        self.bracketRuleCheck.stateChanged.connect(self.save_config)

        # 무시 확장자 입력
        self.ignoreLabel = QLabel("❌ 무시할 확장자 (쉼표로 구분)")
        self.ignoreInput = QLineEdit()
        self.ignoreInput.setPlaceholderText(".dmg, .app, ...")
        self.ignoreInput.textChanged.connect(self.save_config)

        # 로그 출력 (예시)
        self.logLabel = QLabel("📜 상태 로그")
        self.logBox = QTextEdit()
        self.logBox.setReadOnly(True)
        
        self.destLabel = QLabel("📂 정리될 목적지 폴더")
        self.destFolderInput = QLineEdit()
        self.destFolderInput.setPlaceholderText("~/Desktop")  # 기본값 안내
        self.destBrowseBtn = QPushButton("찾아보기")
        self.destBrowseBtn.clicked.connect(self.browseDestFolder)
        self.destFolderInput.textChanged.connect(self.save_config)

        dest_layout = QHBoxLayout()
        dest_layout.addWidget(self.destFolderInput)
        dest_layout.addWidget(self.destBrowseBtn)

        layout.addWidget(self.destLabel)
        layout.addLayout(dest_layout)

        layout.addWidget(self.folderListLabel)
        layout.addWidget(self.folderList)
        layout.addLayout(btn_layout)
        layout.addWidget(self.bracketRuleCheck)
        layout.addWidget(self.ignoreLabel)
        layout.addWidget(self.ignoreInput)
        layout.addWidget(self.logLabel)
        layout.addWidget(self.logBox)

        self.setLayout(layout)
        
    def browseDestFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "정리될 목적지 폴더 선택")
        if folder:
            self.destFolderInput.setText(folder)
            self.save_config()

    def addFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "감시할 폴더 선택")
        if folder:
            self.folderList.addItem(folder)
            self.log(f"폴더 추가: {folder}")
            self.save_config()

    def removeFolder(self):
        selected_items = self.folderList.selectedItems()
        for item in selected_items:
            self.folderList.takeItem(self.folderList.row(item))
            self.log(f"폴더 삭제: {item.text()}")
            self.save_config()

    def log(self, message):
        self.logBox.append(message)

    def createTrayIcon(self):
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(QtGui.QIcon("icon.png"))  # 메뉴바 아이콘
        trayMenu = QMenu(self)

        openAction = QAction("설정 열기", self)
        openAction.triggered.connect(self.show)

        exitAction = QAction("종료", self)
        exitAction.triggered.connect(QApplication.instance().quit)

        trayMenu.addAction(openAction)
        trayMenu.addAction(exitAction)

        self.trayIcon.setContextMenu(trayMenu)
        self.trayIcon.show()
        
    def save_config(self):
        data = {
        "folders": [self.folderList.item(i).text()
                    for i in range(self.folderList.count())],
        "bracket_rule": self.bracketRuleCheck.isChecked(),
        "ignore_exts": [ext.strip()
                        for ext in self.ignoreInput.text().split(',') if ext.strip()],
        "destination": self.destFolderInput.text().strip()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f, indent=4)

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                for folder in data.get("folders", []):
                    self.folderList.addItem(folder)
                self.bracketRuleCheck.setChecked(data.get("bracket_rule", True))
                self.ignoreInput.setText(', '.join(data.get("ignore_exts", [])))
                self.destFolderInput.setText(data.get("destination", os.path.expanduser("~/Desktop")))
                self.log("✅ 설정 불러옴")
                
    def startWatching(self):
        folder_list = [self.folderList.item(i).text()
                        for i in range(self.folderList.count())]
        if not folder_list:
            self.log("⚠️ 감시할 폴더를 추가해주세요.")
            return

        bracket_rule = self.bracketRuleCheck.isChecked()
        ignore_exts = [ext.strip()
                        for ext in self.ignoreInput.text().split(',') if ext.strip()]
        
        destination = self.destFolderInput.text().strip()
        if not destination:
            destination = os.path.expanduser("~/Desktop")

        self.watcher_thread = FolderWatcherThread(
            folder_list, self.log, bracket_rule, ignore_exts, destination)
        self.watcher_thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  

    window = AutoFileOrganizerApp()
    window.show()
    window.startWatching()  # 감시 시작
    sys.exit(app.exec_())
