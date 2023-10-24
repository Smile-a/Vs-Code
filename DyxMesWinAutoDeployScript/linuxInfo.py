import psutil
import socket
from time import sleep

#获取本机信息
def get_sys_info(): 
    print(psutil.disk_usage('/'))
    print("磁盘利用率:",psutil.disk_usage('/').percent,"%")
    print(psutil.virtual_memory())
    print("内存占用百分比:",psutil.virtual_memory().percent,"%")
    return psutil.virtual_memory().percent

#获取本机IP地址
def get_local_ip():
    return socket.gethostbyname(socket.gethostname())


if __name__=='__main__':
    while(True):
        sleep(1)
        free = get_sys_info()
        if(free > 95):
            #发送邮件通知
            print("不好辣，服务器内存不够了~",get_local_ip())
            break