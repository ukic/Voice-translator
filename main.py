from MyApp import MyApp
import sys
from PyQt5.QtWidgets import QApplication


app = QApplication(sys.argv)
window = MyApp()
window.show()
sys.exit(app.exec())

