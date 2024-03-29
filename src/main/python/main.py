from fbs_runtime.application_context.PySide6 import ApplicationContext
from PySide6.QtWidgets import QMainWindow
from packages.main_window import MainWindow

import sys

if __name__ == '__main__':
    appctxt = ApplicationContext()       # 1. Instantiate ApplicationContext
    window = MainWindow(ctx=appctxt)
    window.resize(650, 650)
    window.show()
    exit_code = appctxt.app.exec()      # 2. Invoke appctxt.app.exec()
    sys.exit(exit_code)