import pyautogui

from pywinauto.application import Application
from time import sleep,time

#启动！
if __name__=='__main__':
    app = Application(backend='win32').connect(class_name='Xshell::MainFrame_0')
    window = app.window(class_name='Xshell::MainFrame_0')
    print("Xshell窗口标题：", window.window_text())
    #获取焦点
    window.set_focus()
    #打印这个窗口里面所有的结构
    #window.print_control_identifiers()
    #窗口最大化
    #window.maximize()
    #获取当前窗口显示的坐标
    windowXY = window.rectangle()
    print('窗口坐标:',windowXY)\
    #锁定xshell光标
    cursor = window.child_window(class_name="Afx:00400000:0")
    #查看文件目录的坐标
    rect = cursor.rectangle()  
    print(rect)
    # 打印控件的坐标  
    print("Left:", rect.left)  
    print("Top:", rect.top)  
    print("Right:", rect.right)  
    print("Bottom:", rect.bottom) 
    # 如果需要获取控件的宽度和高度  
    width = rect.width()
    height = rect.height()
    print("Width:", width)  
    print("Height:", height)
    #点击一下本地目录，这样后面的快捷键打开文件; emm鼠标偏移一下,因为这个位置摸不到框框里面
    pyautogui.click(rect.left,rect.top)
    pyautogui.click(button='right')
    # 触发xshell的快捷键右键粘贴，这样就都通用了
    pyautogui.hotkey('shift', 'p')
    #多余了
    pyautogui.hotkey('shift')
    pyautogui.hotkey('enter')