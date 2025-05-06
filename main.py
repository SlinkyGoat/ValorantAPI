from PyQt5.QtWidgets import (
  QApplication, QWidget, QLabel, QListWidget, QVBoxLayout
)
from PyQt5.QtCore import Qt
import sys
import os

class FileDropWidget(QWidget):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Drag and Drop File/Folder Processor")
    self.setAcceptDrops(True)
    self.resize(400, 300)

    self.label = QLabel("Drop files or folders here", self)
    self.label.setAlignment(Qt.AlignCenter)

    self.list_widget = QListWidget()

    layout = QVBoxLayout()
    layout.addWidget(self.label)
    layout.addWidget(self.list_widget)
    self.setLayout(layout)

  def dragEnterEvent(self, event):
    if event.mimeData().hasUrls():
      event.acceptProposedAction()

  def dropEvent(self, event):
    urls = event.mimeData().urls()
    for url in urls:
      path = url.toLocalFile()
      if os.path.exists(path):
        self.list_widget.addItem(path)

def main():
  app = QApplication(sys.argv)
  window = FileDropWidget()
  window.show()
  sys.exit(app.exec_())

if __name__ == "__main__":
  main()