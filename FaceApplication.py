#!/usr/bin/python
# -*- coding: UTF-8 
# author: Ian
# Please,you must believe yourself who can do it beautifully !
"""
Are you OK?
"""

import sys
from PyQt5 import QtWidgets
import FaceDetector
import threading
import LockDevice

def startApp():

    # UI展示
    app = QtWidgets.QApplication(sys.argv)
    window = FaceDetector.FaceDetector()

    # 串口设备
    thread = threading.Thread(target=LockDevice.lockDevice, args=(window,))
    thread.start()

    window.show()

    sys.exit(app.exec_())





if __name__ == "__main__":
    print("****************** 人脸门禁开始启动 ******************")

    startApp()