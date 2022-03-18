import random
import time
import traceback

from PySide6.QtCore import Signal, QObject
from loguru import logger as log


class BallotWorker(QObject):
    result = Signal(str)
    finished = Signal()

    def __init__(self, data_path: str = None):
        super().__init__()
        self.data_path = data_path
        self.stop_ballot = True
        self.data: list = []

    def load_data_from_file(self):
        with open(self.data_path, 'r') as f:
            self.data = f.readlines()

    def start_ballot(self):
        self.load_data_from_file()
        data_length = len(self.data)
        log.info(f'User number: {data_length}')
        try:
            while not self.stop_ballot:
                this_index = random.randint(0, data_length - 1)
                user = self.data[this_index].strip()
                log.debug(f'Index: {this_index}, user: {user}')
                self.result.emit(user)
                time.sleep(0.01)
        except Exception as e:
            log.error(e)
            log.error(traceback.format_exc())
        finally:
            self.finished.emit()
