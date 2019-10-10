#!/usr/bin/python
# -*- coding: UTF-8 
# author: Ian
# Please,you must believe yourself who can do it beautifully !
"""
Are you OK?
"""

import serial.tools.list_ports
import time

# DEVICE_NAME = "/dev/cu.wchusbserial14610"
DEVICE_NAME = "/dev/cu.usbserial"
DEVICE_PORT = 9600
# DEVICE_PORT = 115200

def openDevice():
    portList = list(serial.tools.list_ports.comports())

    for i in range(0, len(portList)):
        print(portList[i])

    try:
        device = serial.Serial(DEVICE_NAME, DEVICE_PORT)
    except Exception as e:
        print(e)
        print("打开串失败，再重新尝试打开")
        device = serial.Serial(DEVICE_NAME, DEVICE_PORT)

    return device

def openDoor(device):
    print("识别成功，正在开门...")
    device.write([0x63, 0x31])
    # device.write(serial.to_bytes(b"c0\n"))
    # device.write(serial.to_bytes(b"12\n"))


def closeDoor(device):
    print("开门成功，正在关门...")
    device.write([0x63, 0x30])
    # device.write(serial.to_bytes(b"c1\n"))
    # device.write(serial.to_bytes(b"13\n"))


def lockDevice(faceDetector):
    portList = list(serial.tools.list_ports.comports())

    for i in range(0, len(portList)):
        print(portList[i])

    device = openDevice()

    start_time = time.time()
    delay_time = start_time
    isOpenDoor = False

    # 循环监听数据和状态消息
    while True:
        current_time = time.time()

        # 每10秒钟，请求一次锁的状态
        if current_time - start_time > 2:
            start_time = current_time
            continue

        try:
            text = str(device.read(32), "utf-8")
            text = text.replace("\n", "", 1)
            print(text)

            if faceDetector and faceDetector.isVisible():
                # 识别成功，就打开门
                if faceDetector.isRecognizable and isOpenDoor == False:
                    faceDetector.isRecognizable = False
                    isOpenDoor = True
                    openDoor(device)
                    closeDoor(device)

                # 延时关门
                if current_time - delay_time > 20:
                    delay_time = current_time
                    isOpenDoor = False
                    # closeDoor(device)

            else:
                print("结束设备监听...")
                break
        except Exception as e:
            print(e)





def testSwitch():

    device = openDevice()

    delay_time = time.time()
    start_time = time.time()

    isClosed = True
    # 循环监听数据和状态消息
    while True:
        current_time = time.time()

        # 每10秒钟，请求一次锁的状态
        if current_time - start_time > 5:
            start_time = current_time
            continue

        try:

            if device.isOpen() == False:
                device.close()
                device = openDevice()

            text = device.read(64)
            # text = device.readline()
            print(text)

            if current_time - delay_time > 10:
                delay_time = current_time
                if isClosed:
                    isClosed = False
                    openDoor(device)
                else:
                    isClosed = True
                    closeDoor(device)

        except Exception as e:
            try:
                print(e)
                print("连接断开，正在重新连接设备...")
                device.close()
                device = None
                device = openDevice()
            except Exception as e:
                print(e)
                print("连接断开，正在重新连接设备又失败了...")

                device = openDevice()



if __name__ == "__main__":
    print("Hello World")

    testSwitch()
