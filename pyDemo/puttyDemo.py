import time
from pywinauto.application import Application

putty_class = "PuTTY"
putty_title = "root@"

def puttyAuto():
    puttyOK = False
    try:
        app = Application(backend='win32').connect(class_name=putty_class)
        window = app.window(class_name=putty_class)
        window_TitleText = window.window_text()
        print("窗口标题：", window_TitleText)
        if putty_title in window_TitleText:
            #获取焦点
            window.set_focus()
            #打印这个窗口里面所有的结构
            #window.print_control_identifiers()
            #窗口最大化
            #window.maximize()
            #获取当前窗口显示的坐标
            #windowXY = window.rectangle()
            #print('窗口坐标:',windowXY)
            time.sleep(1)  # 等待一秒以确保窗口已经获取焦点
            # 输入"ll"命令并按下回车
            window.type_keys("ll{ENTER}")
            # 等待一会以确保命令执行完毕
            time.sleep(2)
            puttyOK = True
    except Exception as e:
        print("执行putty自动化时发生异常,请检查: {}".format(e))
    return puttyOK

#启动！
if __name__=='__main__':  
    puttyok = puttyAuto()
    print(puttyok)