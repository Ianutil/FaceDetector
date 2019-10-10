#!/usr/bin/python
# -*- coding: UTF-8 
# author: Ian
# Please,you must believe yourself who can do it beautifully !
"""
Are you OK?
"""

import sys
import cv2
import base64
import requests
import json
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import Runthread

# 一次最大上传图像数
UPDATE_FACE_COUNT = 5
# 上传时间间隔
UPDATE_FACE_INTERVAL = 10


class FaceDetector(QtWidgets.QMainWindow):
    encode_faces = []

    # 开始检测上传图像时间和间隔
    start_time = time.time()
    isStartUploadFace = False # 是否开启上传图片资源
    isUploadFace = False  # 是否正在上传图片资源

    isStop = False  # 是否停止检测图像
    isRecognizable = False # 是否识别成功

    def __init__(self):
        super().__init__()
        self.initView()
        self.initCamera()

        # 更新天气
        file = "./resource/sunshine.gif"
        self.weatherText = "晴转多云"
        self.updateWeather(file=file, weather=self.weatherText)

    def initView(self):
        self.setWindowTitle('人脸识别门禁系统')
        self.setWindowIcon(QtGui.QIcon('camera.png'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # 设置背景透明
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # self.resize(960, 700)
        self.resize(988, 680)

        # 创建窗口主部件
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QGridLayout()
        self.main_widget.setLayout(self.main_layout)

        self.createWeather()
        # self.createLeftLayout1()
        self.createLeftLayout()
        self.createCameraLayout()
        self.createRegisterOfPhone()

        # 行号，列号，行宽，列宽
        self.main_layout.addWidget(self.weather_widget, 1, 0, 2, 5)
        self.main_layout.addWidget(self.left_widget, 3, 0, 3, 1)
        self.main_layout.addWidget(self.camera_widget, 3, 1, 3, 4)

        self.setCentralWidget(self.main_widget)

    def createWeather(self):
        self.weather_widget = QtWidgets.QWidget()
        self.weather_layout = QtWidgets.QGridLayout()
        self.weather_widget.setLayout(self.weather_layout)

        style = "QWidget{background-color:transparent;border-radius:15px;padding:0px;}"
        # 设置背景色  #FFE1FF
        self.weather_widget.setStyleSheet(style)

        self.label_movie = QtWidgets.QLabel()
        self.label_movie.setStyleSheet(style)
        self.weather_layout.addWidget(self.label_movie, 0, 2, 12, 3)
        # self.label_movie.setPixmap(QtGui.QPixmap("./resource/background.jpg"))
        self.movie_weather = QtGui.QMovie("./resource/rainy.gif")
        self.movie_weather.setScaledSize(QtCore.QSize(self.width(), 210))
        self.label_movie.setMovie(self.movie_weather)
        self.label_movie.setAutoFillBackground(True)
        self.movie_weather.start()

        self.label_weather = QtWidgets.QLabel()
        self.weather_layout.addWidget(self.label_weather, 0, 2, 12, 3)
        self.label_weather.setText(u"2019年02月14日 上午11：19 天气：睛")
        self.label_weather.setFont(QtGui.QFont('SansSerif', 36))
        self.label_weather.setAlignment(QtCore.Qt.AlignCenter)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor(255, 255, 255))  # 设置字体颜色
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.black)  # 设置字体颜色
        self.label_weather.setAutoFillBackground(False)  # 设置背景充满，为设置背景颜色的必要条件
        self.label_weather.setPalette(palette)

    def createLeftLayout1(self):
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        # 设置背景色  浅蓝#FFF0F5  浅黄#FFFFE0 橙色#FFC125  #FFE4C4
        self.left_widget.setStyleSheet('''
            QWidget{
            background-color:#FFA54F;
            border-radius:15px;
            margin-left:15px;
            margin-right:8px;
            padding-left:8px;
            padding-right:8px;
            }
        ''')
        # self.left_widget.setStyleSheet("QWidget{background-color:gray;border-top-left-radius:15px;border-top-right-radius:5px;}”)

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)  # 设置字体颜色
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.red)  # 设置背景颜色
        # palette.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样

        self.label_user = QtWidgets.QLabel()
        self.left_layout.addWidget(self.label_user, 0, 1, 2, 2)
        self.label_user.setText(u"识别结果")
        self.label_user.setFont(QtGui.QFont('SansSerif', 20))
        self.label_user.setPalette(palette)

        self.label_name = QtWidgets.QLabel()
        self.left_layout.addWidget(self.label_name, 3, 1, 1, 2)
        self.label_name.setText(u"姓名：xxxx")
        self.label_name.setFont(QtGui.QFont('SansSerif', 14))
        self.label_name.setPalette(palette)

        self.label_phone = QtWidgets.QLabel()
        self.left_layout.addWidget(self.label_phone, 4, 1, 1, 2)
        self.label_phone.setText(u"电话：132 6290 4190")
        self.label_phone.setFont(QtGui.QFont('SansSerif', 14))
        self.label_phone.setPalette(palette)

        self.label_date = QtWidgets.QLabel()
        self.left_layout.addWidget(self.label_date, 5, 1, 1, 2)
        self.label_date.setText(u"日期：2019-02-14 19：15：00")
        self.label_date.setFont(QtGui.QFont('SansSerif', 14))
        self.label_date.setPalette(palette)

        self.label_barcode = QtWidgets.QLabel()
        self.left_layout.addWidget(self.label_barcode, 7, 1, 10, 2)
        self.label_barcode.setAutoFillBackground(False)
        self.label_barcode.setAlignment(QtCore.Qt.AlignCenter)
        image = QtGui.QPixmap('resource/barcode.png').scaled(200, 200)
        self.label_barcode.setPixmap(image)


        # self.movie_ads = QtGui.QMovie("./resource/movie.gif")
        # scaled = 530.0/200.0
        # self.movie_ads.setScaledSize(QtCore.QSize(200, 160))
        # # self.movie_ads.setScaledSize(QtCore.QSize(530 * scaled, 331*scaled))
        # self.label_ads.setMovie(self.movie_ads)
        # self.movie_ads.start()

        self.register_button = QtWidgets.QPushButton("手机注册")
        self.register_button.setMinimumHeight(40)
        self.register_button.setStyleSheet("QWidget{background-color:red;border-radius:15px;color:white;}")
        self.left_layout.addWidget(self.register_button, 18, 1, 2, 2)
        self.register_button.setFont(QtGui.QFont("SansSerif", 14))
        self.register_button.clicked.connect(self.showRegisterDialog)

        self.exit_button = QtWidgets.QPushButton("退出")
        self.exit_button.setMinimumHeight(40)
        self.exit_button.setStyleSheet("QWidget{background-color:red;border-radius:15px;color:white;}")
        self.left_layout.addWidget(self.exit_button, 22, 1, 2, 2)
        self.exit_button.setFont(QtGui.QFont("SansSerif", 14))
        self.exit_button.clicked.connect(self.close)

    def createLeftLayout(self):
        self.left_widget = QtWidgets.QWidget()
        self.left_layout = QtWidgets.QGridLayout()
        self.left_widget.setLayout(self.left_layout)

        # 设置背景色  浅蓝#FFF0F5  浅黄#FFFFE0 橙色#FFC125  #FFE4C4
        self.left_widget.setStyleSheet('''
            QWidget{
            margin-left:6px;
            margin-right:2px;
            }
        ''')
        # self.left_widget.setStyleSheet("QWidget{background-color:gray;border-top-left-radius:15px;border-top-right-radius:5px;}”)


        self.left_top_widget = QtWidgets.QWidget()
        self.left_top_layout = QtWidgets.QGridLayout()
        self.left_top_widget.setLayout(self.left_top_layout)
        self.left_layout.addWidget(self.left_top_widget, 0, 1, 1, 1)

        self.left_top_widget.setStyleSheet('''
                    QWidget{
                    background-color:#FFA54F;
                    border-radius:15px;
                    padding-left:8px;
                    padding-right:8px;
                    }
                ''')

        self.left_bottom_widget = QtWidgets.QWidget()
        self.left_bottom_layout = QtWidgets.QGridLayout()
        self.left_bottom_widget.setLayout(self.left_bottom_layout)
        self.left_layout.addWidget(self.left_bottom_widget, 1, 1, 2, 1)
        self.left_bottom_widget.setStyleSheet('''
                            QWidget{
                            background-color:#FFA54F;
                            border-radius:15px;
                            margin-top:2px;
                            padding-left:8px;
                            padding-right:8px;
                            }
                        ''')

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)  # 设置字体颜色
        palette.setColor(QtGui.QPalette.Window, QtCore.Qt.red)  # 设置背景颜色
        # palette.setColor(QPalette.Background,Qt.blue)<span style="font-family: Arial, Helvetica, sans-serif;">#设置背景颜色，和上面一行的效果一样

        self.label_user = QtWidgets.QLabel()
        self.left_top_layout.addWidget(self.label_user, 0, 1, 1, 2)
        self.label_user.setText(u"识别结果")
        self.label_user.setFont(QtGui.QFont('SansSerif', 20))
        self.label_user.setPalette(palette)

        self.label_name = QtWidgets.QLabel()
        self.left_top_layout.addWidget(self.label_name, 2, 1, 1, 2)
        self.label_name.setText(u"姓名：xxxx")
        self.label_name.setFont(QtGui.QFont('SansSerif', 14))
        self.label_name.setPalette(palette)

        self.label_phone = QtWidgets.QLabel()
        self.left_top_layout.addWidget(self.label_phone, 3, 1, 1, 2)
        self.label_phone.setText(u"电话：xxx xxxx xxxx")
        self.label_phone.setFont(QtGui.QFont('SansSerif', 14))
        self.label_phone.setPalette(palette)

        self.label_date = QtWidgets.QLabel()
        self.left_top_layout.addWidget(self.label_date, 4, 1, 1, 2)
        self.label_date.setText(u"日期：xxxx                  ")
        self.label_date.setFont(QtGui.QFont('SansSerif', 14))
        self.label_date.setPalette(palette)

        # self.label_move = QtWidgets.QLabel()
        # self.left_top_layout.addWidget(self.label_move, 5, 1, 1, 2)


        self.label_ads = QtWidgets.QLabel()
        self.left_bottom_layout.addWidget(self.label_ads, 0, 1, 1, 2)
        self.label_ads.setAutoFillBackground(False)
        self.label_ads.setText("欢迎来到百联科创中心")
        self.label_ads.setAlignment(QtCore.Qt.AlignCenter)
        self.label_ads.setFont(QtGui.QFont('SansSerif', 14))
        self.label_ads.setStyleSheet('''
                    QWidget{
                    padding-top:6px;
                    padding-bottom:6px;
                    font-size:16px;
                    color:white;
                    font-family:Microsoft YaHei;
                    }
                ''')

        self.label_barcode = QtWidgets.QLabel()
        self.left_bottom_layout.addWidget(self.label_barcode, 1, 1, 10, 2)
        self.label_barcode.setAutoFillBackground(False)
        self.label_barcode.setAlignment(QtCore.Qt.AlignCenter)
        # image = QtGui.QPixmap('resource/icon.png').scaled(200, 200)
        image = QtGui.QPixmap('resource/default.png').scaled(250, 250)
        self.label_barcode.setPixmap(image)


        self.label_number = QtWidgets.QLabel()
        self.label_number.setAlignment(QtCore.Qt.AlignCenter)
        self.label_number.setStyleSheet('''
                        QWidget{
                        background-color:#00FFA54F;
                        padding-top:6px;
                        padding-bottom:6px;
                        font-size:128px;
                        color:white;
                        font-family:Microsoft YaHei;
                        }
                    ''')
        self.left_bottom_layout.addWidget(self.label_number, 1, 1, 10, 2)


    def createCameraLayout(self):
        self.camera_widget = QtWidgets.QWidget()
        self.camera_layout = QtWidgets.QGridLayout()
        self.camera_widget.setLayout(self.camera_layout)
        self.camera_widget.setStyleSheet('''
                   QWidget{
                   background-color:#EEEEEE;
                   margin-bottom:17px;
                   }
               ''')

        self.label_camera = QtWidgets.QLabel()
        self.camera_layout.addWidget(self.label_camera, 0, 0, 12, 12)
        image = QtGui.QPixmap('resource/face.jpg').scaled(self.label_camera.width(), self.label_camera.height())
        self.label_camera.setPixmap(image)

        # 显示检测状态
        # self.detect_status_label = QtWidgets.QLabel()
        # self.camera_layout.addWidget(self.detect_status_label, 0, 0, 12, 1)
        # self.detect_status_label.setText("")
        # self.detect_status_label.setFont(QtGui.QFont('SansSerif', 14))
        # self.detect_status_label.setAlignment(QtCore.Qt.AlignTop|QtCore.Qt.AlignHCenter)


    def initCamera(self):
        # 摄像机
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH,640)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT,480)

        # 确保此xml文件与该py文件在一个文件夹下，否则将这里改为绝对路径
        file = r"resource/haarcascade_frontalface_default.xml"
        self.classifier = cv2.CascadeClassifier(file)

        # 实时刷新
        self.cameraTimer = QtCore.QTimer()
        self.cameraTimer.timeout.connect(self.startCamera)

        # 设置5s后自动开启
        QtCore.QTimer.singleShot(3000, self.startUpCamera)

    def startUpCamera(self):

        print("开始人脸识别")
        # 1000/32ms开始打开相机
        self.cameraTimer.start(1000 / 32)

    # 读摄像头
    def startCamera(self):

        # 更新时间
        self.updateTimer()

        if self.cameraTimer == None or self.cameraTimer.isActive() == False: return
        if self.isStop == True: return

        ret, frame = self.camera.read()

        if ret == False: return

        # 变换彩色空间顺序
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        size = frame.shape[:2]

        divisor = 4
        h, w = size
        minSize = (w // divisor, h // divisor)

        faceRects = self.classifier.detectMultiScale(gray, 1.2, 2, cv2.CASCADE_SCALE_IMAGE, minSize)

        # 目前只支持单人识别
        if len(faceRects) > 0 and len(faceRects) < 2:

            for faceRect in faceRects:
                x, y, w, h = faceRect
                # 上传的服务器
                face_array = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                # face_array = rgb_image[y - 10: y + h + 10, x - 10: x + w + 10]

                current_time = time.time()
                # 注册状态时，不需要上传图像
                # if self.register_phone_widget.isVisible() == False :

                # 增加5张待上传的采集图像
                if self.isStartUploadFace and len(self.encode_faces) < UPDATE_FACE_COUNT:
                    # 只有不在上传图像状态下，才判断是否到了该上传图像的时刻
                    self.start_time = current_time
                    text = "开始上传：{0} 图像：{1} ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                     len(self.encode_faces))
                    print(text)
                    self.label_ads.setText("正采集中{0}，请保持动作...".format(UPDATE_FACE_COUNT - len(self.encode_faces)))
                    self.label_number.setText("{0}".format(UPDATE_FACE_COUNT - len(self.encode_faces)))
                    self.label_barcode.setPixmap(QtGui.QPixmap(""))

                    byte_image = face_array.tobytes()
                    byte_image = base64.b64encode(byte_image)
                    byte_image = str(byte_image, 'utf-8')
                    shape = str(face_array.shape[0]) + ',' + str(face_array.shape[1]) + ',' + str(
                        face_array.shape[2])

                    self.encode_faces.append({"data": byte_image, "shape": shape})
                    cv2.imwrite("./frame.jpg", face_array)

                    # 每隔6秒上传一次图片
                elif current_time - self.start_time > UPDATE_FACE_INTERVAL:
                    # 只有不在上传图像状态下，才判断是否到了该上传图像的时刻了
                    self.start_time = current_time
                    # 开始采集图像标志
                    self.isStartUploadFace = True
                    self.label_number.setText("")

                    text = "开始上传时间：{0} ".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                    print(text)

                # 收集到5张人脸后，上传到服务器，进行识别
                if len(self.encode_faces) >= UPDATE_FACE_COUNT and self.isUploadFace == False:
                    # 关闭采集图像标志
                    self.isStartUploadFace = False
                    self.isUploadFace = True

                    image = QtGui.QPixmap('resource/default.png').scaled(250, 250)
                    self.label_barcode.setPixmap(image)

                    self.label_number.setText("")
                    self.label_ads.setText("正在识别中，请等待开门...")

                    req = {"store_id": "s6001", "device_id": "b001", "faces": self.encode_faces}

                    # 开始上传到服务器
                    self.thread = Runthread.Runthread()
                    self.thread.setRequest(req)
                    self.thread._signal.connect(self.updateFace)
                    self.thread.start()

            # cv2.rectangle(frame, (x, y), (x + h, y + w), (0, 255, 0), 2)
            cv2.rectangle(rgb_image, (x, y), (x + h, y + w), (0, 255, 0), 2)

        # image = QtGui.QImage(frame.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        image = QtGui.QImage(rgb_image.data, frame.shape[1], frame.shape[0], QtGui.QImage.Format_RGB888)
        self.label_camera.setPixmap(QtGui.QPixmap.fromImage(image))

    def updateWeather(self, file, weather):
        self.weatherText = weather
        self.updateTimer()

        self.movie_weather.stop()
        # rainy sunshine
        self.movie_weather.setFileName(file)
        self.movie_weather.start()


    def updateTimer(self):
        # 获取当前系统时间
        currentTime = QtCore.QDateTime.currentDateTime()
        # 时间显示格式
        currentDate = currentTime.toString("yyyy-MM-dd hh:mm:ss");

        weather_text = currentDate + " 天气："+ self.weatherText
        self.label_weather.setText(weather_text)

    def updateFace(self, data):

        # 获取当前系统时间
        currentTime = QtCore.QDateTime.currentDateTime()

        # 时间显示格式
        currentDate = currentTime.toString("yyyy-MM-dd hh:mm:ss");

        try:
            self.encode_faces.clear()
            self.isUploadFace = False

            # 识别结果默认为 False
            self.isRecognizable = False

            code = data["identified"]
            if code == 1:
                name = "姓名： %s" % data["emp"]["name"]

                self.label_name.setText(name)

                self.label_date.setText("日期：" + currentDate)

                self.label_phone.setText("电话：%s" % data["emp"]["phone"])
                self.label_ads.setText("识别成功，开门已开...")

                image = QtGui.QPixmap('resource/default.png').scaled(250, 250)
                self.label_barcode.setPixmap(image)

                # 识别成功
                self.isRecognizable = True
            else:
                self.label_name.setText("姓名： xxx")
                self.label_date.setText("日期： xxxx-xx-xx xx:xx:xx")
                self.label_phone.setText("电话： xxx xxxx xxxx")


                # 识别失败后，显示二维码来注册
                self.face_id = data["face_id"]
                req = requests.get(data["qrcode"])
                image = QtGui.QPixmap()
                image.loadFromData(req.content)
                # image = image.scaled(320, 260, QtCore.Qt.KeepAspectRatio)
                image = image.scaled(350, 280, QtCore.Qt.KeepAspectRatio)
                self.label_barcode.setPixmap(image)

                self.label_ads.setText(u"识别失败，请微信扫描注册")
                print("识别失败: {0} {1}".format(currentDate, data["msg"]))
                # 显示注册手机号提示框
                # self.showRegisterDialog()
        except Exception as e:
            print("网络异常")
            print(e)



    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()

        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, u"提示", u"是否真的需要退出？")

        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')

        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:

            if self.camera.isOpened():
                self.camera.release()
            if self.cameraTimer.isActive():
                self.cameraTimer.stop()
                self.cameraTimer = None
                self.isStop = True
            event.accept()

    # 创建注册框
    def createRegisterOfPhone(self):

        self.register_phone_widget = QtWidgets.QWidget()
        self.register_phone_widget.setObjectName("register_phone")
        self.register_phone_layout = QtWidgets.QGridLayout()
        self.register_phone_widget.setLayout(self.register_phone_layout)

        # self.setStyleSheet("QWidget{background-color:#FFA54F;border-radius:15px;}")
        self.register_phone_widget.setAutoFillBackground(True)

        self.register_phone_widget.setFixedSize(340, 280)

        # 浅蓝色#FFF0F5  橙色#FFA54F
        self.register_phone_widget.setStyleSheet('''
        QWidget#register_phone{
            background:white;
            border:none;
            font-size:16px;
            font-weight:700;
            font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
            border-radius:15px;
        }
        ''')
        self.camera_layout.addWidget(self.register_phone_widget, 1, 1,)
        # self.register_phone_widget.setGeometry(self.width()/2-380/2, self.height()/2 - 250/2, 380, 250)
        self.register_phone_widget.setVisible(False)

        self.label_register_phone = QtWidgets.QLabel("注册手机号")
        self.label_register_phone.setObjectName("register_phone")
        self.label_register_phone.setFont(QtGui.QFont("sans-serif", 18))
        self.register_phone_layout.addWidget(self.label_register_phone, 0, 1, 3, 8)

        self.register_phone_input = QtWidgets.QLineEdit()
        # 只能输入整数
        self.register_phone_input.setValidator(QtGui.QDoubleValidator());
        self.register_phone_input.setObjectName("register_phone")
        self.register_phone_input.setMaxLength(11)
        self.register_phone_input.setFixedHeight(45)
        self.register_phone_input.setPlaceholderText("请输入已登记的手机号码")
        self.register_phone_layout.addWidget(self.register_phone_input, 1, 2, 6, 12)

        self.register_phone_input.setStyleSheet('''
                QWidget{
                    background:#EEEEEE;
                    border:none;
                    border-color:transparent;
                    color:#666666;
                    padding:12px;
                    font-size:16px;
                    font-weight:700;
                    font-family:"Helvetica Neue", Helvetica, Arial, sans-serif;
                    border-radius:15px;
                }
                ''')

        # 右边的手机icon
        self.register_phone_icon = QtWidgets.QLabel()
        self.register_phone_layout.addWidget(self.register_phone_icon, 1, 14, 6, 3)
        image = QtGui.QPixmap("./resource/timg.jpeg").scaled(32, 32)

        self.register_phone_icon.setPixmap(image)

        self.button_register = QtWidgets.QPushButton("注册")
        self.button_register.setObjectName("register_phone")
        self.button_register.setFont(QtGui.QFont("sans-serif", 16))
        self.register_phone_layout.addWidget(self.button_register, 6, 2, 2, 4)

        self.button_cancel = QtWidgets.QPushButton("取消")
        self.button_cancel.setObjectName("register_phone")
        self.button_cancel.setFont(QtGui.QFont("sans-serif", 16))
        self.register_phone_layout.addWidget(self.button_cancel, 6, 6, 2, 4)

        self.button_cancel.clicked.connect(self.hideRegister)
        self.button_register.clicked.connect(self.registerPhone)

    # 隐藏手机注册对话话框
    def hideRegister(self):
        self.register_phone_widget.setVisible(False)
        self.label_camera.setVisible(True)

    # 显示注册手机对话框
    def showRegisterDialog(self):
        self.register_phone_widget.setVisible(True)


    # 手机号码注册
    def registerPhone(self):

        phoneNumber = self.register_phone_input.text()

        print("注册手机号码#",phoneNumber)

        msg = ""
        if len(phoneNumber) == 11:
            req = {"store_id": "s6001", "device_id": "b001", "face_id": self.face_id, "phone_num": phoneNumber}
            print("开始注册#", req)
            res = requests.post(Runthread.SERVICE_URL+"/mem_reg", json=req)
            data = json.loads(res.content)
            print("---------->", data)

            if data["identified"] == 1:
                self.register_phone_widget.setVisible(False)
                msg = u"注册成功！！！"
            else:
                msg = u"注册失败，请重新尝试！！！"
        else:
            msg = u"手机号码输入不正确，请重新输入！！！"

        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()

        dialog = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, u"提示", msg)

        dialog.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        dialog.addButton(cancel, QtWidgets.QMessageBox.ActionRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')

        dialog.exec_()

def main():
    app = QtWidgets.QApplication(sys.argv)

    window = FaceDetector()
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
