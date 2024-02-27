import pyautogui
import pyperclip

from time import sleep,time
from pywinauto.application import Application
from pywinauto import mouse
from pyautogui import scroll


#获取企业微信消息通知里面的最新的登录验证码
def getYzmCode():
    #打开企业微信应用
    app = Application(backend='uia').start(wxWorkPath)
    #sleep(1)
    #链接到企业微信
    app = Application(backend='uia').connect(title=title)
    #sleep(1)
    #选中企业微信窗口
    wind_calc = app[title]
    #sleep(1)
    #获取这个窗口的焦点？
    wind_calc.set_focus()
    #获取当前窗口显示的坐标
    coordinate = wind_calc.rectangle()
    print("当前窗口显示的坐标:",coordinate)

    # 程序左边缘距离显示器左边缘的像素
    l_coordinate = coordinate.left
    # 程序右边缘距离显示器左边缘的像素
    r_coordinate = coordinate.right
    # 程序上边缘距离显示器上边缘的像素
    t_coordinate = coordinate.top
    # 程序下边缘距离显示器上边缘的像素
    b_coordinate = coordinate.bottom

    #这里可以还有一步，先选择左下角 我的企业，然后选中烟的不然有时候公司的消息，你就找不到验证码了,但是，，提醒一下就ok
    
    #选中消息
    #mouse.click(coords=(l_coordinate + 25, b_coordinate - 550))
    #偶然发现的，如果直接单击会有问题，你要是来了一条消息，你单机，他就是第一条，置顶的消息通知都会被顶走
    pyautogui.moveTo((l_coordinate + 25), (b_coordinate - 550))
    #打开通讯录
    #mouse.click(coords=(l_coordinate + 25, b_coordinate - 220))
    #打开文档
    #mouse.click(coords=(l_coordinate + 25, b_coordinate - 440))
    #sleep(1)
    #当前鼠标在消息图标上，挪动到消息通知上面，暂时简单做法就是制定消息通知，让鼠标点过去，高级点就先点搜索框就有点麻烦了
    x,y = pyautogui.position()
    #挪动到消息通知聊天栏然后双击打开
    #mouse.double_click(coords=(x + 73, y + 28))
    #先移动
    pyautogui.moveTo((x + 73), (y + 28))
    for i in range(10):
        #然后滚轮上滑,不是很理解为啥直接10000就那么一点，所以循环弄下算了
        scroll(10000)
    print("鼠标当前位置:",pyautogui.position())
    #这样基本可以确保鼠标在消息通知log上了,双击打开
    pyautogui.doubleClick()
    #偶然发现了 要等一会
    sleep(1)
    #选中企业微信窗口
    wind_msg = app['消息通知']
    #获取当前窗口显示的坐标
    print('消息通知窗口位置:',wind_msg.rectangle())
    wind_msg_left = wind_msg.rectangle().left
    wind_msg_top = wind_msg.rectangle().top
    wind_msg_right = wind_msg.rectangle().right
    wind_msg_bottom = wind_msg.rectangle().bottom
    #获取消息通知的结构
    #print(wind_msg.print_control_identifiers())
    # 本来准备获取窗体内容的 也确实这么做了，奈何太菜了 只能换个路子了,截图或者定位  以后再看看能不能获取窗体在试试
    # 直接截图 这时候是双击的消息通知窗口直接通过消息通知定位
     # 屏幕的宽度和高度
    width, height = pyautogui.size()
    print("当前屏幕尺寸:",width, height)
    #pyautogui.alert(text='寻找定位中...', title='提示', button='OK')
    # 不这样傻傻移动可以用截图匹配 也可以
    # 移动鼠标到窗口聊天框中心 然后下滑动不滑也不是不行
    mouse.double_click(coords=(wind_msg_left + 500, wind_msg_top + 100))
    #这里是从聊天logo向上移动，你要是屏幕像素高自己看着调整就行
    scroll(-10)
    #截图 太妙了 他的聊天记录log刚好对应验证码!!
    qwGpslogo = pyautogui.locateOnScreen('qwGpslogo.png')
    print('聊天记录log位置:',qwGpslogo)
    qwGpslogoX = qwGpslogo.left + 10
    qwGpslogoY = qwGpslogo.top - 50
    #移动鼠标到聊天框那--定位的是图片log左上角，往上走双击直接获取验证码
    #pyautogui.moveTo(qwGpslogoX,qwGpslogoY)
    mouse.double_click(coords=(qwGpslogoX, qwGpslogoY))
    #到这，就获取到了企业微信聊天框里面验证码了
    pyautogui.hotkey('ctrl', 'c')
    #然后关闭这个窗口，不然下次打开找不到会出问题，其实可以在上面获取消息通知的时候做判断，如果已经打开了就直接找过去辅助就行，但是先这样吧
    print('聊天记录log关闭按钮位置:',wind_msg_right,wind_msg_top)
    qwGpslogoCloseX = wind_msg_right - 10
    qwGpslogoCloseY = wind_msg_top + 10
    #单击关闭按钮
    mouse.click(coords=(qwGpslogoCloseX, qwGpslogoCloseY))
    #最小化企业微信的窗口
    wind_calc.minimize()
    yzm = pyperclip.paste()
    return yzm


#企业微信地址
wxWorkPath = 'C:\Program Files (x86)\WXWork\WXWork.exe'
title = '企业微信'
# 设置自动化操作时间间隔
pyautogui.PAUSE = 0.5



#启动！
if __name__=='__main__':
    #yzm = getYzmCode()
    #print(yzm)
    
    #打开企业微信应用
    app = Application(backend='uia').start(wxWorkPath)
    #链接到企业微信
    app = Application(backend='uia').connect(title=title)
    #选中企业微信窗口
    wind_calc = app[title]
    #获取这个窗口的焦点？
    wind_calc.set_focus()
    #获取当前窗口显示的坐标
    coordinate = wind_calc.rectangle()
    print("当前窗口显示的坐标:",coordinate)
    
    # 输出企业微信主窗口的控件树
    wind_calc.print_control_identifiers()
    
    # 获取 Pane2 控件
    pane2 = wind_calc.child_window(title="", control_type="Pane", found_index=0)

    # 输出 Pane2 的控件信息
    print("控件文本:",pane2.window_text())  # 打印控件文本
    print("控件位置矩形信息:",pane2.rectangle())  # 打印控件位置矩形信息
    
    # 获取 Pane2 控件的坐标信息
    rect = pane2.rectangle()
    # 打印每个坐标的值
    print("Left:", rect.left)
    print("Top:", rect.top)
    print("Right:", rect.right)
    print("Bottom:", rect.bottom)
    pyautogui.moveTo((rect.left), (rect.top))
    
    print("s")
    pane2.print_control_identifiers()
    b = pane2.child_window(title="", control_type="Pane0", found_index=0)
    print("X")
    print(b)
    print(b.child_window())
    print("DIR")
    print(dir(b))
    print("VARS")
    print(vars(b))
