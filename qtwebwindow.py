"""
1. use qt5 to create a fullscreen web browser
2. allow specifying url from command line
this sort of works, but does not have a way to exit in fullscreen mode.
"""
import sys
import logging
import pathlib
import argparse
from urllib.parse import urlparse
# use QWebEngineView instead of from pyside2
# https://stackoverflow.com/questions/52709871/how-to-use-qwebengineview-in-pyqt5
import signal
from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtCore import QUrl, QEventLoop, QTimer, Qt, SIGNAL, SLOT, Slot
from PySide2.QtWidgets import QApplication, QMainWindow
from PySide2.QtWebEngineWidgets import QWebEngineView
print("using PySide2")
# except ImportError:
#     from PyQt5 import Qt
#     from PyQt5.QtWidgets import QApplication
#     from PyQt5.QtCore import QUrl, pyqtSignal as SIGNAL
#     from PyQt5.QtWebEngineWidgets import QWebEngineView
#     print("using PyQt5")

class MyQtKiosk(QMainWindow):
    def __init__(self) -> None:
        super(MyQtKiosk, self).__init__()
        # self.showFullScreen()
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)
        self.connect(SIGNAL("closeEvent(QCloseEvent)"), self.close)
        # not sure why this does not work
        # self.connect(SIGNAL("keyPressEvent(QKeyEvent)"), self.key_press_handler)
        self.connect(SIGNAL("loadFinished(bool)"), self.on_load_finished)
        # close if close key is pressed
        # self.connect(SIGNAL("keyPressEvent(QKeyEvent)"), self.key_press_handler)
        signal.signal(signal.SIGINT, self.close)
        self.show()


    def keyPressEvent(self, event):
        """ override keyPressEvent to handle key events"""
        logging.info(f"keyPressEvent{event.key()}")
        if event.key() == Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    def on_load_finished(self, ok):
        logging.info("on_load_finished")
    
    def load(self, url):
        self.webview.load(QUrl(url))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help='url to open', required=False)
    parser.add_argument('--debug', action='store_true', help='enable debug logging')
    args = parser.parse_args()


    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    logging.info("starting")
    if not args.url:
        logging.info("no url specified, opening default")
    args.url = 'kiosk.html'

    if not urlparse(args.url).scheme:
        # check if url is a file and it exists
        path = pathlib.Path(args.url)
        if path.is_file():
            # make file into a url
            args.url = f"file://{path.absolute()}"
            logging.info(f"url: {args.url}")
        else:
            logging.info("no scheme present, prepending http://")
            args.url = "http://" + args.url

    app = QApplication(sys.argv)
    # close app when browser window is closed
    app.setQuitOnLastWindowClosed(True)
    view = MyQtKiosk()
    view.load(QUrl(args.url))
    # view.showFullScreen()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()