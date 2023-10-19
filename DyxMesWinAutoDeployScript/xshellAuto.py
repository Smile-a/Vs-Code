import os
import sys
import ddddocr
import pyautogui
import pytesseract
import datetime as dt
import pyperclip
import tkinter as tk
import requests
import dyxServerConfig

from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep,time
from pywinauto.application import Application
from pywinauto import mouse
from pyautogui import scroll
from PIL import Image


def main():
    #好坑，这个地方进来没有等待，窗口都没加载好，自然找不到。。。
    sleep(5)
    # 设置自动化操作时间间隔
    pyautogui.PAUSE = 0.5
    # 先把路径切进来
    print("我要开始xshell自动化了~")
    print("当前路径",os.getcwd())
    print("鼠标当前位置:",pyautogui.position())
    xshellTitle = dyxServerConfig.xshellTitle
    print("xshell窗口标题：",xshellTitle)
    #找到这个app
    app = Application(backend='win32').connect(best_match=''+xshellTitle+'')
    sleep(2)
    #模糊匹配这个窗口
    window = app.window(best_match=''+xshellTitle+'')    
    sleep(2)
    #获取焦点
    window.set_focus()
    #窗口最大化
    #window.maximize()
    #获取当前窗口显示的坐标
    windowXY = window.rectangle()
    print('Xshell窗口坐标:',windowXY)
    #打印这个窗口里面所有的结构
    #window.print_control_identifiers()
    
    #获取焦点，默认就可以输入命令了，光标拿到了
    sleep(0.5)
    window.set_focus()
    #强迫症
    pyautogui.typewrite('ll',0.5)
    #很关键，每次输入了字之后shift一下 避免回车变成中文，懒得写强制修改输入法中文的方法了
    pyautogui.hotkey('shift')
    pyautogui.hotkey('enter')
    #自己加的脚本--这样自动化前面出了问题的化，这个脚本问题不大
    #pyautogui.typewrite('nohup sh deploy-frontend-Auto.sh > /dev/null 2>&1 &',0.2) #这个直接关闭窗口都行
    pyautogui.typewrite('sh deploy-frontend-Auto.sh',0.2) #这个就要硬等xshell的窗口命令跑完才可以奥
    pyautogui.hotkey('shift')
    pyautogui.hotkey('enter')
    #等脚本慢慢跑就行了,前台包，15s应该解压无压力吧~  后台jar包还是直接后台跑就行了其余不管
    sleep(15)
    #自带的close居然会有异常?
    pyautogui.hotkey('alt','f4')
    #确认关闭
    pyautogui.hotkey('y')
    print("xshell自动化结束")
