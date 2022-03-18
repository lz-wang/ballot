import sys
import os

from PySide6.QtCore import QThread, Qt
from PySide6.QtGui import QFont, QCloseEvent
from PySide6.QtWidgets import (QMainWindow, QMessageBox, QComboBox,
                               QWidget, QPushButton, QApplication, QLabel,
                               QHBoxLayout, QVBoxLayout)
from loguru import logger as log

from env import ROOT_DIR
from worker import BallotWorker


def reconnect(signal, slot):
    try:
        signal.disconnect()
    except Exception as e:
        log.debug(f'Qt disconnect error, detail: {str(e)}')
    finally:
        if isinstance(slot, list):
            for sl in slot:
                signal.connect(sl)
        else:
            signal.connect(slot)


class BallotWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.root_path = ROOT_DIR
        self._init_ui()
        self._init_ballot_thread()

    def _init_ui(self):
        self.font = QFont()
        self.font.setFamilies([u"Songti"])
        self.font.setItalic(False)
        self.font.setPointSize(12)

        self.select_label = QLabel('选择抽签人群: ')
        self.select_label.setFont(self.font)
        self.select_label.setFixedWidth(120)

        self.select_box = QComboBox()
        self.select_box.setFixedWidth(370)
        self.select_box.addItems(self.get_txt_files())
        self.select_box.setFont(self.font)

        self.select_refresh_btn = QPushButton('刷新')
        self.select_refresh_btn.clicked.connect(self.refresh_select_box)
        self.select_refresh_btn.setFixedWidth(80)
        self.select_refresh_btn.setFont(self.font)

        select_layout = QHBoxLayout()
        select_layout.addWidget(self.select_label)
        select_layout.addWidget(self.select_box)
        select_layout.addWidget(self.select_refresh_btn)
        # select_layout.setAlignment(Qt.AlignLeft)

        self.font.setPointSize(30)
        self.result_label = QLabel('???')
        self.result_label.setFont(self.font)
        self.result_label.setFixedWidth(400)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.font.setPointSize(15)
        self.run_ballot_btn = QPushButton('开始\n抽签')
        self.run_ballot_btn.setFixedSize(80, 80)
        self.run_ballot_btn.setFont(self.font)
        self.run_ballot_btn.clicked.connect(self.switch_ballot)

        ballot_layout = QHBoxLayout()
        ballot_layout.addWidget(self.result_label)
        ballot_layout.addWidget(self.run_ballot_btn)
        ballot_layout.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(select_layout)
        main_layout.addLayout(ballot_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(main_layout)
        self.setCentralWidget(self.main_widget)

        # self.setLayout(ballot_layout)
        self.setWindowTitle('抽签工具 v0.1 by lzwang')
        self.setFixedSize(600, 400)

    def refresh_select_box(self):
        self.select_box.clear()
        self.select_box.addItems(self.get_txt_files())

    def get_txt_files(self):
        files = os.listdir(self.root_path)
        return [file for file in files if file.endswith('.txt')]

    def _init_ballot_thread(self):
        self.ballot_thread = QThread()
        self.ballot_worker = BallotWorker()
        self.ballot_worker.moveToThread(self.ballot_thread)
        reconnect(self.ballot_worker.result, self.show_result)

    def show_result(self, result: str):
        self.result_label.setText(f'{result}')

    def switch_ballot(self):
        if self.ballot_worker.stop_ballot:
            self.ballot_worker.data_path = os.path.join(self.root_path, self.select_box.currentText())
            self.ballot_worker.stop_ballot = False
            self.run_ballot_btn.setText('停止\n抽签')
            reconnect(self.ballot_thread.started, self.ballot_worker.start_ballot)
            reconnect(self.ballot_worker.finished, self.ballot_thread.quit)
            self.ballot_thread.start()
        else:
            self.ballot_worker.stop_ballot = True
            self.run_ballot_btn.setText('开始\n抽签')

    def closeEvent(self, event: QCloseEvent) -> None:
        if not self.ballot_worker.stop_ballot:
            self.switch_ballot()
        reply = QMessageBox.question(self, '退出?', "确认要退出抽签软件吗?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BallotWindow()
    window.show()
    sys.exit(app.exec())
