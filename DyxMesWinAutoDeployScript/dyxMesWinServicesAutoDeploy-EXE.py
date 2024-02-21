import os
import sys
import json
import ddddocr
import pyautogui
import pyperclip
import tkinter as tk
import requests

from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep,time
from pywinauto.application import Application
from pywinauto import mouse
from pyautogui import scroll
from PIL import Image
from urllib.request import urlopen

# 获取当前脚本所在的目录
script_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
print('script_dir:'+script_dir)
# 将dyxServerConfig.py所在的路径加入到sys.path中,而且是最前面，优先在这个目录下找
sys.path.insert(0,script_dir)
import dyxServerConfig

#获取企业微信消息通知里面的最新的登录验证码
def getYzmCode():
    sleep(2)
    #打开企业微信应用
    app = Application(backend='uia').start(wxWorkPath)
    sleep(1)
    #链接到企业微信
    app = Application(backend='uia').connect(title=title)
    sleep(1)
    #选中企业微信窗口
    wind_calc = app[title]
    sleep(1)
    #获取这个窗口的焦点？
    wind_calc.set_focus()
    #获取当前窗口显示的坐标
    coordinate = wind_calc.rectangle()
    print(coordinate)

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


def customer():
    # 输入提示框， 显示带有文本输入以及确定和取消按钮的消息框
    customer_name = pyautogui.prompt(text='', title='搜索', default='搜索')
    return customer_name


#持续获取当前鼠标坐标
def getPoint():
    for i in range(20):
        print("鼠标当前位置:",pyautogui.position())
        sleep(0.5)


#用tk做一个弹窗提示 自动关闭
def alterAuto(s):
    root = tk.Tk()  # 搞个tk
    root.withdraw() # 隐藏tk窗口 
    root.after(s, root.destroy) # 设置过时时间，单位为毫秒，超过s毫秒后运行root.destroy方法
    ss = int(s / 1000)
    messagebox.showinfo("提示", "该提示框在"+ str(ss) +"s后自动关闭,因为考虑到网络因素稍等一下~")
    #root.mainloop() # 加入主循环   如果注释掉这一行，程序将在创建窗口后立即结束,我做提示框要的就是这个


#获取登陆页面的验证码,可以单击更换
def getVcodeImg(vcodeImg):
    print('img:',vcodeImg)
    vcodeImg.screenshot(os.getcwd() + "/code.png")  # 下载图片
    sleep(2)
    with open(os.getcwd() + "/code.png", "rb") as fp:
        img = fp.read()
    #识别图片验证码
    ocr = ddddocr.DdddOcr()
    imgYzm = ocr.classification(img)
    print('识别图片验证码:',imgYzm)
    return imgYzm


#后来才发现，原来每天那个配置文件里面的登录参数是会变，对比了一下，感觉应该是时间戳加密那些玩意，但是无所谓
def getHtmlValue():
    #每次登录前获取一次，然后更新配置文件里面保存的就ok了
    # 读取文件内容  
    with open('dyxmesServiceJSON.json', 'r') as file:  
        config_data = json.load(file)
        node_count = len(config_data)  # 计算节点元素数量  
        print("JSON文件中节点元素数量为:", node_count)
    for i in range(node_count):
        server_name = list(config_data.keys())[i]  # 获取当前节点的服务器名称  
        jsonStr = config_data[server_name]  # 获取对应的json数据
        configTitleName = jsonStr['configTitleName']
        configTitleId = jsonStr['id']
        print("服务器:",configTitleName)
        print("dev_id:",configTitleId)
        devIdUrl = 'https://10.157.234.151/index.php/UserWork/operation/dgrp_id/0/dev_id/' + configTitleId
        chrome.get(devIdUrl)
        
        # 定位到shell表单元素
        shell_form = chrome.find_element(By.ID,"shell_1")
        # 定位到输入框元素  
        shell_form_input = shell_form.find_element(By.NAME,"data")  
        # 获取输入框的值  
        shell_value = shell_form_input.get_attribute("value")  
        # 打印输入框的值  
        #print(shell_value)
        
        # 定位到winscp表单元素  
        ssh_form = chrome.find_element(By.ID,"SSH")  
        # 定位到输入框元素  
        ssh_form_input = ssh_form.find_element(By.NAME,"data")  
        # 获取输入框的值  
        ssh_value = ssh_form_input.get_attribute("value")  
        # 打印输入框的值  
        #print(ssh_value)
        
        #把取到的值写入到config里面
        if(configTitleName == ''):
            print("更新密钥发生了点问题，程序退出!")
            sys.exit()
        else:
            # 更改xhell的值
            config_data[''+configTitleName+'']['Xshell'] = ''+shell_value+''
            config_data[''+configTitleName+'']['winscp'] = ''+ssh_value+''
            # 将更新后的内容写回到文件  
            with open('dyxmesServiceJSON.json', 'w') as file:  
                json.dump(config_data, file, indent=4)


#前台项目打包自动化
def frontendPackageAuto():
    print("前台自动化开始")
    #先切换到前台项目的根路径
    os.chdir(dyxServerConfig.frontendProPath)
    #然后更新一下前台代码
    os.system("svn update")
    
    #咋还非要切到那个路径才行呢 烦死了
    os.chdir(dyxServerConfig.frontendPath)
    #执行打包脚本
    os.system(dyxServerConfig.frontendBuildPath)

    #插个广告
    alterTk = tk.Tk()
    alterTk.withdraw()
    alterTk.after(3000, alterTk.destroy)
    messagebox.showinfo("提示", "稍等一下，前台打包脚本跑一下~")

    #然后还得把路径切换回来，这么不智能吗,还是我没找到方法?
    os.chdir(pyFilePath)
    print("打包成功，切换路径，当前路径",os.getcwd())

    print("准备打开Winscp")
    # 读取文件内容  
    with open('dyxmesServiceJSON.json', 'r') as file:
        jsonFileData = json.load(file)
    #构造请求winscp的参数
    winscp_form_data = requests.structures.CaseInsensitiveDict()
    winscp_form_data.update({'data': ''+jsonFileData[''+dyxServerConfig.frontendTitleKey+'']['winscp']+''})
    winscp_form_data.update({'username': ''})
    winscp_form_data.update({'password': ''})
    try:  
        sleep(2)
        #故意设置三秒的让他直接结束就ok了，不然后面的还要等待post响应吗
        requests.post('http://127.0.0.1:8888/RunWinScp', data=winscp_form_data,timeout=3.0)
    except requests.exceptions.RequestException as e:  
        # 当捕获到特定类型的异常时，打印出异常信息，然后继续执行  
        print(f'winscp捕获到值错误: {e}')
    sleep(1)
    #调用winscp脚本开始上传文件了~
    upFileStatus = winscpAuto(dyxServerConfig.frontendPath,dyxServerConfig.frontendZipName)
    if(upFileStatus == None):
        print("失败了？")
        #关闭浏览器
        chrome.quit()
        failTk = tk.Tk()
        failTk.withdraw()
        failTk.after(3000, failTk.destroy)
        messagebox.showerror("错误", "在上传文件时发生了问题？建议查看一下哦～")
        #程序结束
        sys.exit()
    else:
        print("成功了！")
        try:  
            #文件都上传成功了，切换xshell开始走指令启动程序了~
            sleep(2)
            #故意设置三秒的让他直接结束就ok了，不然后面的还要等待post响应吗
            requests.post('http://127.0.0.1:8888/RunTerm',{'data':''+jsonFileData[''+dyxServerConfig.frontendTitleKey+'']['Xshell']+''},timeout=3.0)
        except requests.exceptions.RequestException as e: 
            # 当捕获到特定类型的异常时，打印出异常信息，然后继续执行  
            print(f'xshell捕获到值错误: {e}')
        #调用xshell脚本开始处理上传的文件了~~ 改造一下，这里传入你要调用的脚本命令
        xshellAuto("sh deploy-frontend-Auto.sh")
        print("前台自动化正常结束了~")


#如果说前台打包替换都完活了的话，可以开始后台jar包的部署了
def javaJarPackageAuto():
    print("jar包自动化开始")
    #mvn打包
    mavenPack()
    #打包成功了，准备上传吧,原来还想着做个开关，指定替换，我都自动了，我直接全换了不就ok了吗  
    #60的
    #base
    if(dyxServerConfig.isBase):
        jarUp(dyxServerConfig.jar_base,dyxServerConfig.jar_base_Name,"base_start",dyxServerConfig.testTwoTitleKey)
    #quality
    if(dyxServerConfig.isQuality):
        jarUp(dyxServerConfig.jar_quality,dyxServerConfig.jar_quality_Name,"quality_start",dyxServerConfig.testTwoTitleKey)
    #warehouse
    if(dyxServerConfig.isWarehouse):
        jarUp(dyxServerConfig.jar_warehouse,dyxServerConfig.jar_warehouse_Name,"warehouse_start",dyxServerConfig.testTwoTitleKey)
    #59的
    #plan
    if(dyxServerConfig.isPlan):
        jarUp(dyxServerConfig.jar_plan,dyxServerConfig.jar_plan_Name,"plan_start",dyxServerConfig.testOneTitleKey)
    #system
    if(dyxServerConfig.isSystem):
        jarUp(dyxServerConfig.jar_system,dyxServerConfig.jar_system_Name,"system_start",dyxServerConfig.testOneTitleKey)
    
    print("jar包自动化结束")


#maven打包操作
def mavenPack():
    print("切换到目录，执行maven命令打包")
    mvn_package = "mvn clean package -P " + dyxServerConfig.maven_Profile
    mvn_install = "mvn clean install -P " + dyxServerConfig.maven_Profile
    #切换到父目录
    os.chdir(dyxServerConfig.jarFilesPath)
    #忘了一步，在这里svn更新一下最新的代码
    os.system("svn update")
    #这里会慢，更新一下所有的依赖，免得跑不起来==
    os.system("mvn clean -U")
    #还是先切换到commapi和mobile俩install一下再说吧，不然有时候他们更新了接口的
    os.chdir(dyxServerConfig.jar_commonapi)
    #执行install
    os.system(mvn_install)
    sleep(2)
    #切换到mobile继续
    os.chdir(dyxServerConfig.jar_mobile)
    #执行install
    os.system(mvn_install)
    sleep(2)
    #可以了，切回父目录，直接全部打包!
    os.chdir(dyxServerConfig.jarFilesPath)
    os.system(mvn_package)


#拆分复用---就是把前台那边的代码拆分一下过来复用,懒得把他俩封装了
def jarUp(jarPath,jarName,jarStart,titleKey):
    print("准备打开Winscp")
    # 读取文件内容 emm 这时候路径已经切到jar包这边了，懒得切回去就直接读取吧，问题不大C:\Users\wsd\eclipse-workspace\dyxmesProject\hbtobacco-dyxmes-parent\hbtobacco-dyxmes-base\target\hbtobacco-dyxmes-base.jar
    
    with open(pyFilePath+'\\dyxmesServiceJSON.json', 'r') as file:
        jsonFileData = json.load(file)
    #构造请求winscp的参数
    winscp_form_data = requests.structures.CaseInsensitiveDict()
    winscp_form_data.update({'data': ''+jsonFileData[''+titleKey+'']['winscp']+''})
    winscp_form_data.update({'username': ''})
    winscp_form_data.update({'password': ''})
    try:  
        sleep(2)
        #故意设置三秒的让他直接结束就ok了，不然后面的还要等待post响应吗
        requests.post('http://127.0.0.1:8888/RunWinScp', data=winscp_form_data,timeout=3.0)
    except requests.exceptions.RequestException as e:  
        # 当捕获到特定类型的异常时，打印出异常信息，然后继续执行  
        print(f'winscp捕获到值错误: {e}')
    sleep(1)
    #调用winscp脚本开始上传文件了~
    upFileStatus = winscpAuto(jarPath,jarName)
    if(upFileStatus == None):
        print("失败了？")
        #关闭浏览器
        chrome.quit()
        failTk = tk.Tk()
        failTk.withdraw()
        failTk.after(3000, failTk.destroy)
        messagebox.showerror("错误", "在上传jar包时发生了问题？建议查看一下哦～")
        #程序结束
        sys.exit()
    else:
        print("成功了！")
        try:  
            #文件都上传成功了，切换xshell开始走指令启动程序了~
            sleep(2)
            #故意设置三秒的让他直接结束就ok了，不然后面的还要等待post响应吗
            requests.post('http://127.0.0.1:8888/RunTerm',{'data':''+jsonFileData[''+titleKey+'']['Xshell']+''},timeout=3.0)
        except requests.exceptions.RequestException as e: 
            # 当捕获到特定类型的异常时，打印出异常信息，然后继续执行  
            print(f'xshell捕获到值错误: {e}')
        #调用xshell脚本开始处理上传的文件了~~ 改造一下，这里传入你要调用的脚本命令
        xshellStr = "nohup sh deploy_dyxmes.sh " + jarStart + " > /dev/null 2>&1 &"
        xshellAuto(xshellStr)
        print("后台自动化正常结束了~")


#调启winscp的方法;;filePath=文件全路径;fileName=文件单独名称
def winscpAuto(filePath,fileName):
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
    #记录一下，好像是这样，默认打开文件/目录快捷键，但是你不要手欠自己点过远程目录的那个奥，不然好像会打开远程目录，就会找不到文件，不理会这条即可
    pyautogui.hotkey('ctrl', 'o')
    #打开就会自己选中，把路径直接放进去
    #把变量值复制到剪贴板
    #jarpath = dyxServerConfig.jarFilesPath
    #jarpath = dyxServerConfig.frontendPath
    pyperclip.copy(filePath)
    #这个时候光标还是在路径栏，直接粘贴就ok了
    sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    #模拟回车，确认
    pyautogui.hotkey('enter')
    #最好先去判断一下文件是否存在
    #upFile = dyxServerConfig.frontendPath + dyxServerConfig.frontendZipName
    upFile = filePath + fileName
    print("上传文件路径:",upFile)
    if(os.path.exists(upFile)):
        print("文件存在")
    else:
        print("文件不存在，程序终止!")
        fileNullErrTk = tk.Tk()
        fileNullErrTk.withdraw()
        fileNullErrTk.after(3000, fileNullErrTk.destroy)
        messagebox.showerror("错误", "打包上传文件不存在，请检查!")
        return
    #获取焦点
    window.set_focus()
    #选择文件
    pyautogui.hotkey('alt','m')
    pyautogui.hotkey('down')
    pyautogui.hotkey('enter')
    #fronZip = dyxServerConfig.frontendZipName
    #复制一下要打包的文件名称，因为要定位它
    pyperclip.copy(fileName)
    sleep(1)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    #f5上传，f6上传并且删除
    pyautogui.hotkey('f6')
    #最后一个发送enter,然后就开始了上传,好像有些框是可以选中以后都不弹窗，这个可以自己调整是否要回车
    pyautogui.hotkey('enter')
    
    #最新的问题，我好像没有办法在这个窗口等待他是不是上传完毕了，有一个进度条但是我无法获取到~
    sleep(5)
    #但是可以曲线救国，走到这里确定了文件存在，进度条在上传了对吧，我执行的是上传成功后删除文件，那？
    for n in range(100):
        #我直接堵塞住你，不往下走，就给我读那个文件，你只要不存在了 那不就是删除成功了吗
        sleep(6)
        #最多给你十分钟时间，还没成功那。。。。。。。
        if(os.path.exists(upFile)):
            print("文件存在,上传还未完成，请等待！")
        else:
            print("文件不存在了，上传成功了！!!")
            window.set_focus()
            #上传成功后关闭窗口 用window.close()会有问题，很怪
            pyautogui.hotkey('alt', 'f4')
            #确认关闭 你要是打勾了应该没问题了
            pyautogui.hotkey('enter')
            print("winscp自动化结束")
            #结束？break? sys.exit()?
            return True
    #你要是还能到这说明？10分钟了还没上传成功？你认真的？
    #emmmm


#调启xshell的方法;;shellStr输入的cmd指令,一般都是调用sh那句
def xshellAuto(shellStr):
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
    #做个判断，前台脚本我改了的不用切路径
    if('deploy_dyxmes.sh' in shellStr):
        pyautogui.typewrite('cd',0.2)
        pyautogui.hotkey('shift')
        pyautogui.typewrite(' /home/mes',0.2)
        pyautogui.hotkey('shift')
        pyautogui.hotkey('enter')
        #那就要先cd去/home/mes里面了在执行脚本
    #自己加的脚本--这样自动化前面出了问题的化，这个脚本问题不大
    #pyautogui.typewrite('nohup sh deploy-frontend-Auto.sh > /dev/null 2>&1 &',0.2) #这个直接关闭窗口都行
    #pyautogui.typewrite('sh deploy-frontend-Auto.sh',0.2) #这个就要硬等xshell的窗口命令跑完才可以奥
    pyautogui.typewrite(shellStr,0.2)
    pyautogui.hotkey('shift')
    pyautogui.hotkey('enter')
    #等脚本慢慢跑就行了,前台包，15s应该解压无压力吧~  后台jar包还是直接后台跑就行了其余不管
    sleep(10)
    window.set_focus()
    #自带的close居然会有异常?
    pyautogui.hotkey('alt','f4')
    #确认关闭
    pyautogui.hotkey('y')
    print("xshell自动化结束")



#启动！
if __name__=='__main__':
    #要登陆堡垒机的账号和密码
    qwAccount=dyxServerConfig.loginUserName
    qwPassword=dyxServerConfig.qwPassword
    #企业微信地址
    wxWorkPath = dyxServerConfig.wxWorkPath
    title = '企业微信'
    # 设置自动化操作时间间隔
    pyautogui.PAUSE = 0.5

    # 先把路径切进来
    print("我要开始浏览器登录自动化了~")
    print("当前路径",os.getcwd())
    ##pyFilePath = sys.path[0] #py脚本用这个
    pyFilePath = os.getcwd()  #打包成exe要用这个
    print("文件所在路径",pyFilePath)
    #进入到文件夹所在路径
    os.chdir(pyFilePath)
    print("切换路径，当前路径",os.getcwd())
    print("鼠标当前位置:",pyautogui.position())

    #检查一下能不能ping的通10.157.234.151再继续，后面可以自己加启动vpn
    pingHostname  = dyxServerConfig.pingHostname
    pingResponse = os.system("ping -n 1 " + pingHostname)
    if pingResponse == 0:
        print('Ping successful')
    else:
        print('Ping failed.')
        sys.exit()

    #谷歌浏览器驱动配置
    print("开始操作浏览器~")
    options = webdriver.ChromeOptions()
    #selenium默认是会执行完关闭浏览器的，这样设置一下先不关闭，最后执行手动quit即可。
    options.add_experimental_option('detach', True)
    #加载谷歌浏览器驱动
    chrome = webdriver.Chrome(options=options)
    #设置浏览器窗口最大化
    #chrome.maximize_window()
    try:  
        #登陆堡垒机
        chrome.get(dyxServerConfig.bljLoginPathUrl)
    except Exception as e:  
        print("登录堡垒机失败！")
        chrome.close()
        sys.exit()
    #弹窗等待一下
    alterAuto(3000)
    #这个地址一打开就说不安全，点击高级按钮然后访问真实地址就可以正常登录了
    gaojiButton = chrome.find_element(By.ID,'details-button')
    gaojiButton.click()
    sleep(1)
    #选择继续访问，点击
    jixuButton = chrome.find_element(By.ID,'proceed-link')
    jixuButton.click()
    sleep(1)
    #不出意外的话都打开了
    #输入账号
    account = chrome.find_element(By.NAME,'account')
    account.send_keys(qwAccount)
    sleep(1)
    #本地密码
    local = chrome.find_element(By.NAME,'local')
    local.send_keys(qwPassword)
    sleep(1)
    #单击按钮-发送验证码
    send_mobile_codeButton = chrome.find_element(By.ID,'send_mobile_code')
    send_mobile_codeButton.click()
    #这时候会有一个系统弹窗，说发送成功,把它关掉
    sleep(1)
    chrome.switch_to.alert.accept()
    #怕有时候网络不行，所以才等一会
    #弹窗等待一下.有的时候验证码没有那么及时~
    alterAuto(5000)
    #获取企业微信收到的验证码
    yzm = getYzmCode()
    print('获得企微验证码:',yzm)

    #短信密码填入
    sms = chrome.find_element(By.NAME,'sms')
    sms.send_keys(yzm)
    #调用图像识别，取到图片验证码
    vcodeImg = chrome.find_element(By.ID,'vcode')
    imgYzm = getVcodeImg(vcodeImg)
    #最多10下吧，就不信10次还有这样的验证码
    for i in range(10):
        #判断验证码有没有o，O，0 这些，目前这个识别会失败，那就直接换一个新的就好了
        if len(imgYzm) < 4:
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        elif 'o' in imgYzm:
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        elif 'O' in imgYzm:
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        elif '0' in imgYzm :
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        elif '1' in imgYzm :
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        elif '工' in imgYzm :
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        elif '5' in imgYzm :
            vcodeImg.click()
            imgYzm = getVcodeImg(vcodeImg)
        else :
            print(imgYzm)
            break
    #验证码输入框
    verify = chrome.find_element(By.NAME,'verify')
    verify.send_keys(imgYzm)
    sleep(1)
    #登陆按钮触发
    submit = chrome.find_element(By.ID,'submit')
    submit.click()
    print("执行操作,不出意外登陆成功!")
    #是否登陆成功
    errBox = chrome.find_element(By.ID,'errBox')
    errBoxSpan = errBox.get_attribute('innerHTML')
    print(errBoxSpan)
    #一般登陆成功就啥也没有，如果登陆失败才会有字，而且账号密码验证码基本都不会有问题，只有可能是验证码也就是"*验证码不正确！"
    if errBoxSpan != '':
        #以后可以改成重新来一遍登陆流程，现在就先结束
        #关闭浏览器
        chrome.quit()
        #搞个提示框告诉一下失败了
        closeTk = tk.Tk()  # 搞个tk
        closeTk.withdraw() # 隐藏tk窗口 
        closeTk.after(3000, closeTk.destroy) # 设置过时时间，单位为毫秒，超过s毫秒后运行root.destroy方法
        messagebox.showerror("错误", "本次登录遇到了一点点问题，请重新启动试试~~")
        #程序结束
        sys.exit()
    #等一下加载
    sleep(5)
    #刷新浏览器
    #chrome.refresh()
    #全局搜索页面
    allList = dyxServerConfig.bljAllListPathUrl
    chrome.get(allList)
    sleep(1)
    #更新登录密钥--目前写的是直接把测试的三台服务器都更新了，以后有需要或者别的自己加就行
    getHtmlValue()
    #然后我在切回去~装作无事发生
    chrome.get(allList)
    sleep(1)

    #判断前台打包开关
    print(dyxServerConfig.isFrontend)
    if(dyxServerConfig.isFrontend):
        #调用前台打包方法
        frontendPackageAuto()
    sleep(1)
    #判断后台打包开关 如果全都是false的话就不进去了，有时候会自己选择部署哪个模块
    if(dyxServerConfig.isSystem or dyxServerConfig.isPlan or dyxServerConfig.isBase or dyxServerConfig.isQuality or dyxServerConfig.isWarehouse):
        #调用后台打包方法
        javaJarPackageAuto()
    sleep(1)
    #关闭浏览器
    chrome.quit()