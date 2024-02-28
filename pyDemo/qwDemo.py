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
    #链接到企业微信
    app = Application(backend='uia').connect(title=title)
    #选中企业微信窗口
    wind_calc = app[title]
    #获取这个窗口的焦点？
    wind_calc.set_focus()
    #获取当前窗口显示的坐标
    coordinate = wind_calc.rectangle()
    print("企业微信窗口显示的坐标:",coordinate)

    # 程序左边缘距离显示器左边缘的像素
    l_coordinate = coordinate.left
    # 程序右边缘距离显示器左边缘的像素
    r_coordinate = coordinate.right
    # 程序上边缘距离显示器上边缘的像素
    t_coordinate = coordinate.top
    # 程序下边缘距离显示器上边缘的像素
    b_coordinate = coordinate.bottom

    #这里可以还有一步，先选择左下角 我的企业，然后选中烟的不然有时候公司的消息，你就找不到验证码了,但是，，提醒一下就ok

    #选中消息 偶然发现的，如果直接单击会有问题，你要是来了一条消息，你单机，他就是第一条，置顶的消息通知都会被顶走
    pyautogui.moveTo((l_coordinate + 28), (t_coordinate + 88))
    #当前鼠标在消息图标上，挪动到消息通知上面，暂时简单做法就是制定消息通知，让鼠标点过去，高级点就先点搜索框就有点麻烦了
    #直接挪动到消息通知聊天栏然后双击打开,有时候会出问题，你说不定在最后一行 还没回到顶上呢
    #先移动
    pyautogui.moveTo((l_coordinate + 90), (t_coordinate + 129))
    #先轻轻单击一下，让他好翻页
    pyautogui.click()
    #要等一下，免得双击了，必须这样才能触发pageup
    sleep(1)
    pyautogui.click()
    for i in range(10):
        # 模拟按下 Page Up 键
        pyautogui.press('pageup')  
    print("鼠标当前位置:",pyautogui.position())
    #这样基本可以确保鼠标在消息通知log上了,双击打开
    pyautogui.doubleClick()
    #偶然发现了 要等一会
    sleep(1)
    #选中企业微信窗口
    wind_msg = app['消息通知']
    #获取当前窗口显示的坐标,被双击出来的窗口默认就是居中的，很赞
    print('消息通知窗口位置:',wind_msg.rectangle())
    wind_msg_left = wind_msg.rectangle().left
    wind_msg_top = wind_msg.rectangle().top
    wind_msg_right = wind_msg.rectangle().right
    wind_msg_bottom = wind_msg.rectangle().bottom
     # 屏幕的宽度和高度
    width, height = pyautogui.size()
    print("当前屏幕尺寸:",width, height)
    #把鼠标定位到消息通知弹窗的那个聊天记录的log上面，那个是定位点，很赞
    #先移动
    pyautogui.moveTo((wind_msg_left + 230), (wind_msg_top + 391))
    #不出意外的话，现在鼠标就在聊天记录按钮上了，这就是他的坐标
    log_x,log_y = pyautogui.position()
    #然后从这个坐标，挪动到最新一条的验证码的那个位置，是可以双击自动选中6位数验证码的那个位置才行
    pyautogui.moveTo((log_x + 14), (log_y - 65))
    #这里一个双击不是为了拿验证码，有可能不是最新的消息，为了让他可以翻页而已
    pyautogui.doubleClick()
    #这时候双击就可以直接复制验证码了， 但是为了以防万一，滚动一下这个框最安全
    for j in range(10):
        # 模拟按下 Page Down 键，就是最新的验证码,虽然一进来默认就是最新
        pyautogui.press('pagedown')
    #双击获取验证码
    mouse.double_click(coords=((log_x + 14), (log_y - 65)))
    #到这，就获取到了企业微信聊天框里面验证码了
    pyautogui.hotkey('ctrl', 'c')
    print("获取到最新的验证码为:",pyperclip.paste())
    #然后关闭这个窗口，不然下次打开找不到会出问题，其实可以在上面获取消息通知的时候做判断，如果已经打开了就直接找过去辅助就行，但是先这样吧
    #以防万一，先获取这个消息通知窗口的焦点
    print("关闭消息通知独立窗口")
    wind_msg.set_focus()
    pyautogui.hotkey('alt', 'f4')
    #最小化企业微信的窗口
    wind_calc.minimize()
    #拿到剪贴板的数据,就是验证码
    yzm = pyperclip.paste()
    return yzm


#企业微信地址
wxWorkPath = 'C:\Program Files (x86)\WXWork\WXWork.exe'
title = '企业微信'
# 设置自动化操作时间间隔
pyautogui.PAUSE = 0.5



#启动！
if __name__=='__main__':
    yzm = getYzmCode()
    print(yzm)
