#!/usr/bin/python
# -*- coding: UTF-8 
# author: Ian
# Please,you must believe yourself who can do it beautifully !
"""
Are you OK?
"""

from PyQt5 import QtCore
import threading
import requests
import json

# SERVICE_URL = "http://10.10.10.4:5000"
SERVICE_URL = "https://sss.bailianic.com"

# 继承QThread
class Runthread(QtCore.QThread):
    # python3,pyqt5与之前的版本有些不一样
    #  通过类成员对象定义信号对象
    _signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Runthread, self).__init__()

    def __del__(self):
        self.wait()


    def setRequest(self, req):
        self.req = req

    def run(self):
        try:

            time = QtCore.QDateTime.currentDateTime()
            text = "开始时间：{0} 线程# {1}".format(time.toString("yyyy-MM-dd hh:mm:ss"), threading.current_thread().name)
            print(SERVICE_URL+"/mem_rec")
            print(text)
            text = "请求数据# deviceId = {0} 上传人脸个数：{1}".format(self.req["device_id"], len(self.req["faces"]))
            print(text)
            res = requests.post(SERVICE_URL+"/mem_rec", json=self.req)
            time = QtCore.QDateTime.currentDateTime()
            print("结束时间：", time.toString("yyyy-MM-dd hh:mm:ss"))

            print("---------->",res.content)

        #     1：表示成功；0：表示失败
        #     {"identified": false, "msg": "员工未能识别，请输入手机号码验证", "face_id": "0e3eb880-33fc-11e9-a986-88e9fe6fe202", "time_consuming": 180}
            data = json.loads(res.content)
            self.callback(data)
            self._signal.emit(data);  # 可以在这里写信号焕发

        except Exception as e:
            data = {}
            self.callback(data)
            self._signal.emit(data);  # 可以在这里写信号焕发

            print(e)

    def callback(self, data):
        # print(threading.current_thread().name)
        self._signal.emit(data);  # 可以在这里写信号焕发


if __name__ == "__main__":
    print("Hello World")