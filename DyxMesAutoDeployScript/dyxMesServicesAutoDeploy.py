import sys
import atomac
import ddddocr
import datetime as dt
import dyxServerConfig
import requests

from atomac.AXKeyCodeConstants import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep,time
from PIL import Image

#企业微信应用名称id
bundle_id = 'com.tencent.WeWorkMac'
#要登陆堡垒机的账号和密码
qwAccount='anwei'
qwPassword='An123456'

#获取登陆验证码
def getYzmCode():
    #启动应用
    atomac.launchAppByBundleId(bundle_id)
    #获取应用信息
    ato = atomac.getAppRefByBundleId(bundle_id)
    #获取当前应用windows
    cur_win = ato.windows()[0]
    #窗口标题
    #print(cur_win.AXTitle)
    #分离组
    flz = cur_win.findFirstR(AXRole='AXSplitGroup')
    #滚动区
    gdq = flz.findFirstR(AXRole='AXScrollArea')
    #表格
    table = gdq.findFirstR(AXRole='AXTable')
    #表格里所有行；0就是那个状态，我的是疯狂打码中那个,因为我把消息提醒置顶了所以是第一个,后面迭代好点
    rowsAll = table.findAllR(AXRole='AXCell')
    #消息通知的row，预设一下，后面循环匹配，不然emmm如果没有把消息通知设置为置顶，[1]不就找不到了吗
    rows=[]
    #每一个单元格,迭代匹配
    for row in rowsAll:
        #获取每一个单元格里面的，就是聊天联系人左边的
        textArr = row.findFirstR(AXRole='AXStaticText')
        #具体的标题value值，比如'消息通知'栏目,'企业微信团队'之类
        textArrValue = textArr.AXValue
        #因为我们只需要消息通知就判断一下
        if textArrValue == '消息通知':
            #把消息通知栏对象传出去
            rows = row
            break
    #这个单元格下面所有文本框--消息通知里面有3个
    allTexts = rows.findAllR(AXRole='AXStaticText')
    #堡垒机帐号验证码--这里是左边的栏目，然后模拟按钮单击，在右边聊天框里面取验证码，左边栏目里面是没有值的
    xxtzlm = allTexts[1]
    #消息通知栏目的坐标
    xy = xxtzlm.AXPosition
    print('消息通知栏目的坐标:',xy)
    #模拟鼠标单击-消息通知栏
    xxtzlm.clickMouseButtonLeft(xy)
    #等一秒
    sleep(1)
    #不出意外右边的聊天框就是验证码具体信息了，想办法拿到;;从分离区里面拿
    area = flz.findAllR(AXRole='AXScrollArea')[1] #0就是左边的联系人列表，1是右边的聊天框的聊天记录表格
    #右边表格里面的第一个table，就是聊天框，里面都是单元格
    ltb = area.findFirstR(AXRole='AXTable')
    #获取每一个单元格，没个单元格里面都是四个文本框基本上
    lycellArr = ltb.findAllR(AXRole='AXCell')
    #找到最后的一个单元格，就是最新的验证码
    lycell = lycellArr[-1]
    #这个单元格里面所有的文本
    #lttxtDate = lycell.findFirstR(AXRole='AXStaticText') #这是消息标题日期，第一个
    lycelltext = lycell.findFirstR(AXRole='AXTextArea') #这个是堡垒机认证账号那个，是个文本框
    #一整句消息
    vlaue = lycelltext.AXValue
    print(vlaue)
    #截取只要验证码
    yzmCode = vlaue[29:35]
    print(yzmCode)
    #有效期
    yxqDatestr = vlaue[-16:] + ":00"
    print(type(yxqDatestr),yxqDatestr)
    #转成日期对象
    yxqDate = dt.datetime.strptime(yxqDatestr, '%Y-%m-%d %H:%M:%S')
    print(type(yxqDate),yxqDate)
    #比较验证码是否有效，对比时间即可
    now_time = dt.datetime.now()
    print(now_time)
    #判断有效期是否大于当前时间
    isEff = yxqDate > now_time
    print(isEff)
    if isEff:
        print("验证码有效!")
    else:
        print("验证码过期了!")
    #后期再加上是否有效的逻辑，目前先都放行
    #用在浏览器页面的登陆验证码
    dxyzm = ''
    dxyzm = yzmCode
    print(dxyzm)
    #关闭企业微信的窗口
    closeBtn = cur_win.AXCloseButton
    closeBtn.Press()
    return dxyzm

#获取登陆页面的验证码,可以单击更换
def getVcodeImg(vcodeImg):
    print('img:',vcodeImg)
    vcodeImg.screenshot("code.png")  # 下载图片
    sleep(2)
    with open("code.png", "rb") as fp:
        img = fp.read()
    #识别图片验证码
    ocr = ddddocr.DdddOcr(show_ad=False)
    imgYzm = ocr.classification(img)
    print('识别图片验证码:',imgYzm)
    return imgYzm

#谷歌浏览器驱动配置
options = webdriver.ChromeOptions()
#selenium默认是会执行完关闭浏览器的，这样设置一下先不关闭，最后执行手动quit即可。
options.add_experimental_option('detach', True)
#加载谷歌浏览器驱动
chrome = webdriver.Chrome(options=options)
#设置浏览器窗口最大化
chrome.maximize_window()
#登陆dyx
chrome.get("https://10.157.234.151/index.php/Public/index/stra_name/sms_local")
sleep(3)
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
sleep(1)
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
i = 1
while i <= 10:
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
    i += 1
#验证码输入框
verify = chrome.find_element(By.NAME,'verify')
verify.send_keys(imgYzm)
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
    #程序结束
    sys.exit()
#等一下加载
sleep(5)
#刷新浏览器
chrome.refresh()
sleep(1)
#print(chrome.page_source)#打印当前页面源码
#全局搜索页面
allList = 'https://10.157.234.151/index.php/UserWork/index/type/all/cpu/64'
chrome.get(allList)
#获取全局搜索按钮
#liId_all = chrome.find_element(By.ID,'liId_all')
#liId_all = chrome.find_element(By.LINK_TEXT,'全局搜索')
#liId_all.click()
#sleep(5)
#找到设备名称/IP的搜索框
keyword = chrome.find_element(By.NAME,'keyword')
#输入要部署的服务器ip
keyword.send_keys('10.156.53.58')#举例
#点击查询
search = chrome.find_element(By.NAME,'search')
search.click()
#也许可以emmm我直接好家伙
devIdUrl = 'https://10.157.234.151/index.php/UserWork/operation/dgrp_id/0/dev_id/' + '763'
print(devIdUrl)
chrome.get(devIdUrl)
#然后点击页面的那个按钮？打开
sleep(1)
requests.post('http://127.0.0.1:8888/RunTerm',{'data':''+dyxServerConfig.test_10_156_53_58['term']+''})
sleep(1)
#requests.post('http://127.0.0.1:8888/RunWinScp',{'data':''+dyxServerConfig.test_10_156_53_58['winscp']+''})
sleep(1)
#关闭浏览器
#chrome.quit()