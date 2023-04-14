import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer, QObject, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QFileDialog
import os
import shutil
from datetime import datetime

import win32file


class Communicate(QObject):
    signal = pyqtSignal()


class App:
    def __init__(self):
        self.tray_icon = None
        self.menu_items = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.periodic_task)
        self.last_drive_list = []
        self.current_drive_list = []
        self.signal = Communicate()
        self.signal.signal.connect(self.update_menu)

    def periodic_task(self):
        self.current_drive_list.clear()
        drivebits = win32file.GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                # here if the drive is at least there
                drname = '%c:\\' % chr(ord('A') + d)
                t = win32file.GetDriveType(drname)
                if t == win32file.DRIVE_REMOVABLE:
                    self.current_drive_list.append(drname)
        if self.last_drive_list != self.current_drive_list:
            self.last_drive_list = self.current_drive_list.copy()
            self.signal.signal.emit()

    def run(self):
        app = QApplication(sys.argv)

        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(QIcon('good-icon.png'), app)
        self.tray_icon.setToolTip('My App')

        # Create the menu
        menu = QMenu()

        action1 = QAction('Set Path', self.tray_icon)
        action1.triggered.connect(self.set_path)
        menu.addAction(action1)
        action2 = QAction('Exit', self.tray_icon)
        action2.triggered.connect(self.exit)
        menu.addAction(action2)

        self.tray_icon.setContextMenu(menu)

        # Start the timer to execute a function every 5 seconds
        self.timer.start(5000)

        # Show the tray icon
        self.tray_icon.show()

        # Run the event loop
        sys.exit(app.exec_())

    def update_menu(self):
        # Modify the menu
        menu = self.tray_icon.contextMenu()
        menu.clear()
        for disk in self.current_drive_list:
            action1 = QAction(disk, menu)
            action1.triggered.connect(lambda: self.open(disk))
            menu.addAction(action1)
        action1 = QAction('Set Path', self.tray_icon)
        action1.triggered.connect(self.set_path)
        menu.addAction(action1)
        action2 = QAction('Exit', menu)
        action2.triggered.connect(self.exit)
        menu.addAction(action2)

    def set_path(self):

        self.config.setWindowTitle('Configuration')
        self.config.setGeometry(300, 300, 640, 480)

        self.config.show()
        print("opened!")

    def open(self, path):
        outfolder = os.path.join('D:\capture one sesions')

        def copy_files_to_dated_folders(src_dir, dest_dir):
            """
            Copy files from source directory to a dated folder in the destination directory.
            If the dated folder does not exist, it will be created.
            """
            foldername = ["Output",
                          "Capture",
                          "Selects",
                          "Trash"]
            for file in os.listdir(src_dir):
                src_file_path = os.path.join(src_dir, file)
                if os.path.isfile(src_file_path):
                    creation_time = os.path.getctime(src_file_path)
                    creation_date = datetime.fromtimestamp(creation_time).strftime('%Y\\%m\\%d\\')
                    creation_date_for_session = datetime.fromtimestamp(creation_time).strftime('%Y_%m_%d')
                    origin_folder_path = os.path.join(dest_dir, creation_date)
                    if not os.path.exists(origin_folder_path):
                        for folder in foldername:
                            os.makedirs(os.path.join(origin_folder_path,folder ))
                    dest_folder_path = os.path.join(origin_folder_path,"Capture")
                    dest_file_path = os.path.join(dest_folder_path, file)
                    if not os.path.exists(dest_file_path):
                        shutil.copy2(src_file_path, dest_folder_path)
                    new_session_file_name = os.path.join(origin_folder_path,creation_date_for_session+".cosessiondb")
                    old_session_file_name = os.path.join(origin_folder_path,"cosessiondb.cosessiondb")
                    if not os.path.exists(new_session_file_name):
                        shutil.copy("cosessiondb.cosessiondb",origin_folder_path )
                        os.rename(old_session_file_name,new_session_file_name)

        folder_list = set()
        for root, dirs, files in os.walk(path):
            if any(file.lower().endswith(('.jpg', '.jpeg', '.raf')) for file in files):
                folder_list.add(root)
                continue

        for folder in folder_list:
            # in_folder = os.path.join(path, file)
            copy_files_to_dated_folders(folder, outfolder)
        print("opened!")

    def empty(self):
        # self.tray_icon.
        print("empty!")

    def exit(self):
        # Do something when the "Exit" menu item is clicked
        self.tray_icon.hide()
        sys.exit()


if __name__ == '__main__':
    app = App()
    app.run()
