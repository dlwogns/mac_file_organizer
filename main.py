import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QListWidget, QPushButton, QFileDialog, QHBoxLayout,
    QCheckBox, QTextEdit, QLineEdit, QSystemTrayIcon, QMenu, QAction
)
from PyQt5.QtCore import Qt

class AutoFileOrganizerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto File Organizer")
        self.setGeometry(300, 300, 400, 500)
        self.setWindowIcon(QtGui.QIcon("icon.png"))  # 아이콘 파일 있으면 설정

        self.initUI()
        self.createTrayIcon()

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

        # 무시 확장자 입력
        self.ignoreLabel = QLabel("❌ 무시할 확장자 (쉼표로 구분)")
        self.ignoreInput = QLineEdit()
        self.ignoreInput.setPlaceholderText(".dmg, .app, ...")

        # 로그 출력 (예시)
        self.logLabel = QLabel("📜 상태 로그")
        self.logBox = QTextEdit()
        self.logBox.setReadOnly(True)

        layout.addWidget(self.folderListLabel)
        layout.addWidget(self.folderList)
        layout.addLayout(btn_layout)
        layout.addWidget(self.bracketRuleCheck)
        layout.addWidget(self.ignoreLabel)
        layout.addWidget(self.ignoreInput)
        layout.addWidget(self.logLabel)
        layout.addWidget(self.logBox)

        self.setLayout(layout)

    def addFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "감시할 폴더 선택")
        if folder:
            self.folderList.addItem(folder)
            self.log(f"폴더 추가: {folder}")

    def removeFolder(self):
        selected_items = self.folderList.selectedItems()
        for item in selected_items:
            self.folderList.takeItem(self.folderList.row(item))
            self.log(f"폴더 삭제: {item.text()}")

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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # 창 닫아도 Tray 아이콘은 살아있게

    window = AutoFileOrganizerApp()
    window.show()

    sys.exit(app.exec_())
