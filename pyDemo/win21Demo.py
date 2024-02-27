import os
import time
import win32gui
import win32api
import win32con
import win32clipboard
import pyautogui as pag

#企业微信地址
wxWorkPath = 'C:\Program Files (x86)\WXWork\WXWork.exe'
title = '企业微信'

#启动！
if __name__=='__main__':
    print("hellow win32Demo!")
    
    x,y = pag.position()
    print(x,y)
    
    win = win32gui.FindWindow(None, title)  # 获取标题名称为title的句柄
    #win2 = win32gui.GetForegroundWindow()  # 获取当前窗口句柄
    #win32gui.SetForegroundWindow(win)  # 前台显示
    #win32gui.ShowWindow(win, win32con.SW_MAXIMIZE)  # 最大化
    
    #获取窗口标题
    winTitle = win32gui.GetWindowText(win)
    print(winTitle)
    
    #获取窗口类名
    winClassName = win32gui.GetClassName(win)
    print(winClassName)
    
    #获取窗口大小
    left,top,right,bottom = win32gui.GetWindowRect(win)
    print(left,top,right,bottom)
    width = right - left
    print("窗口宽度：",width)
    height = bottom - top
    print("窗口高度：",height)
    
    #获取窗口位置
    placement = win32gui.GetWindowPlacement(win)
    pstotopn = placement[4][:2]
    print(pstotopn)
    
    #获取窗口状态
    state = placement[1]
    print(state)