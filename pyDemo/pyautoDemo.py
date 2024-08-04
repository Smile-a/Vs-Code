import sys

from time import sleep
from threading import Event, Thread
from selenium import webdriver

# 定义一个全局变量来保存浏览器实例  
chrome = None
# 添加一个新的事件来控制子线程的启动 
start_event = Event()
# 添加一个新的事件来控制子线程的停止
stop_event = Event()

def login():
    global chrome
    if not chrome:
        print("开始操作浏览器~")
        options = webdriver.ChromeOptions()
        #selenium默认是会执行完关闭浏览器的，这样设置一下先不关闭，最后执行手动quit即可。
        options.add_experimental_option('detach', True)
        #加载谷歌浏览器驱动
        chrome = webdriver.Chrome(options=options)
        chrome.get("https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%97%B6%E9%97%B4&fenlei=256&rsv_pq=0xb501d0ae008a76c3&rsv_t=16d2i%2BsAO9UkRRGLa4I59np2hqSfx2bOJTVi602nuyIsFd4cCVC9bAK7P7n0&rqlang=en&rsv_dl=tb&rsv_enter=1&rsv_sug3=9&rsv_sug1=6&rsv_sug7=100&rsv_sug2=0&rsv_btype=i&inputT=2503&rsv_sug4=2503")
        # 用户登录后启动刷新线程
        start_event.set()
    else:
        print("已经登录，无需再次登录")

def refresh_browser():
    global chrome, start_event, stop_event
    #不是关闭状态
    while not stop_event.is_set():
        # 等待start_event被设置
        start_event.wait()
        #循环刷新页面
        while True:
            if chrome:
                #刷新页面
                print("刷新页面~~保持连接状态~~")
                chrome.refresh()
            # 等待10分钟
            #sleep(600)
            sleep(6)

def quitChrome():  
    global chrome, stop_event
    # 关闭浏览器
    if chrome:
        chrome.quit()  
        chrome = None  
        print("浏览器已关闭")
    # 设置停止事件
    stop_event.set()
 
#启动！
if __name__=='__main__':  
    # 创建并启动子线程
    thread = Thread(target=refresh_browser)
    # 设置子线程为守护线程;在主线程退出时，子线程也会立即终止。
    thread.daemon = True
    thread.start()
    login()
    #模拟主窗体一直不关闭的循环
    sleep(100)
    #关闭浏览器    
    #quitChrome()
    #sys.exit()