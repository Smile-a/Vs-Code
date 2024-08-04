import pyautogui

from pywinauto.application import Application
from time import sleep,time

#启动！
if __name__=='__main__':
    print("开始操作winscp")
    app = Application(backend='win32').connect(class_name='TScpCommanderForm') #通过类名
    window = app.window(class_name='TScpCommanderForm') #通过类名
    window_TitleText = window.window_text()
    print("WinSCP窗口标题：", window_TitleText)
    #获取焦点
    window.set_focus()
    #打印这个窗口里面所有的结构
    #window.print_control_identifiers()
    #窗口最大化
    #window.maximize()
    #获取当前窗口显示的坐标
    windowXY = window.rectangle()
    print('WinSCP窗口坐标:',windowXY)
    #先拿到最大的面板窗体,拿第一个就行了，他有多个TPanel
    bdTPanel_window = window.child_window(class_name="TPanel",found_index=0)
    #然后在TPanel里面拿文件目录控件
    TDirView = bdTPanel_window.child_window(class_name="TDirView")
    #查看文件目录的坐标
    rect = TDirView.rectangle()  
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
    pyautogui.click(rect.left + 10,rect.top + 10)
    pyautogui.hotkey('ctrl', 'o')