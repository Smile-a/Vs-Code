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
    #好坑，这个地方进来没有等待，winscp的窗口都没加载好，自然找不到。。。
    sleep(5)
    # 设置自动化操作时间间隔
    pyautogui.PAUSE = 0.5
    # 先把路径切进来
    print("我要开始WinSCP自动化了~")
    print("当前路径",os.getcwd())
    print("鼠标当前位置:",pyautogui.position())
    #winscp的完整title,因为这个title是动态的哦
    winscpTitle = dyxServerConfig.loginUserName + dyxServerConfig.winsctTitle
    print("WinSCP窗口标题：",winscpTitle)
    #找到这个app
    app = Application(backend='win32').connect(best_match=''+winscpTitle+'')
    #模糊匹配这个窗口
    window = app.window(best_match=''+winscpTitle+'')
    #获取焦点
    window.set_focus()
    #打印这个窗口里面所有的结构
    #window.print_control_identifiers()
    #获取当前窗口显示的坐标
    #windowXY = window.rectangle()
    #print('WinSCP窗口坐标:',windowXY)
    #窗口最大化
    #window.maximize()
    #快捷键打开本地目录，就是你的jar包文件夹，好上传文件到服务器
    sleep(0.5)
    pyautogui.hotkey('ctrl', 'o')
    #打开就会自己选中，把路径直接放进去
    #把变量值复制到剪贴板
    #jarpath = dyxServerConfig.jarFilesPath
    jarpath = dyxServerConfig.frontendPath
    pyperclip.copy(jarpath)
    #这个时候光标还是在路径栏，直接粘贴就ok了
    sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    #模拟回车，确认
    pyautogui.hotkey('enter')
    #最好先去判断一下文件是否存在
    upFile = dyxServerConfig.frontendPath + dyxServerConfig.frontendZipName
    print("上传文件路径:",upFile)
    if(os.path.exists(upFile)):
        print("文件存在")
    else:
        print("文件不存在，程序终止!")
        fileNullErrTk = tk.Tk()
        fileNullErrTk.withdraw()
        fileNullErrTk.after(3000, fileNullErrTk.destroy)
        messagebox.showerror("错误", "打包上传文件不存在，请检查!")
        sys.exit()
    #选择文件
    pyautogui.hotkey('alt','m')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    fronZip = dyxServerConfig.frontendZipName
    pyperclip.copy(fronZip)
    sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    pyautogui.hotkey('f5')
    #最后一个发送enter
    pyautogui.hotkey('enter')
    sleep(60)
    #上传成功后关闭窗口 用window.close()会有问题，很怪
    pyautogui.hotkey('alt', 'f4')
    #确认关闭 你要是打勾了应该没问题了
    pyautogui.hotkey('enter')
    print("winscp自动化结束")