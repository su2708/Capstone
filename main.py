from PyQt5.QtWidgets import QApplication
from test_thread import MultiCamWindow
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MultiCamWindow()
    window.show()
    sys.exit(app.exec_())
