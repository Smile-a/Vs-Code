import socket
import paramiko
  

ipAddr = "192.168.42.127"
userName = "root"
password = "root"
isFont = True
isSystem = True
isKanban = True

if(__name__=="__main__"):
    # 创建一个套接字对象，连接到远程服务器  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((ipAddr, 22))
    
    # 创建SSHClient对象，并设置连接参数  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    
    # 连接服务器  
    ssh.connect(hostname=ipAddr, username=userName, password=password, sock=sock)  
    
    # 创建SFTPClient对象，并传入SSH连接  
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())  
    
    # 上传文件  
    result = sftp.put('/Users/anwei/Documents/我的项目/Vs-Code/demo.txt', '/root/demo.txt')  
    if result:
        print("上传成功!")
    else:
        print("上传失败!")

    #执行命令
    stdin, stdout, stderr = ssh.exec_command('pwd')
    print(stdout.read().decode())

    # 关闭连接  
    sftp.close()  
    ssh.close()