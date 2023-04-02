import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction

class App:
    def __init__(self):
        self.tray_icon = None

    def run(self):
        app = QApplication(sys.argv)

        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(QIcon('icon.png'), parent=None)
        self.tray_icon.setToolTip('My App')

        # Create the menu
        menu = QMenu()
        action1 = QAction('Open', self.tray_icon)
        action1.triggered.connect(self.open)
        menu.addAction(action1)
        action2 = QAction('Exit', self.tray_icon)
        action2.triggered.connect(self.exit)
        menu.addAction(action2)

        self.tray_icon.setContextMenu(menu)

        # Show the tray icon
        self.tray_icon.show()

        # Run the event loop
        sys.exit(app.exec_())

    def open(self):
        # Do something when the "Open" menu item is clicked
        pass

    def exit(self):
        # Do something when the "Exit" menu item is clicked
        self.tray_icon.hide()
        sys.exit()

if __name__ == '__main__':
    app = App()
    app.run()
