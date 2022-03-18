import sys

import qdarktheme
from PySide6.QtWidgets import QApplication

from window import BallotWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BallotWindow()
    app.setStyleSheet(qdarktheme.load_stylesheet('dark'))
    window.show()
    sys.exit(app.exec())
