from PyQt5.QtWidgets import QMessageBox
class MessageManager():

    def __init__(self, message):
        self.msg = QMessageBox()
        self.msg.setText(message)

    def warning(self):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setStandardButtons(QMessageBox.Close)
        self.msg.exec_()

    def error(self):
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setStandardButtons(QMessageBox.Close)
        self.msg.exec_()
