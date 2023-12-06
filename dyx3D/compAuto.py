import os
import socket
import paramiko


#是否上传开关
isFrontend = True
isSystem = True
isKanban = True
#路径配置
ipAddr = "192.168.42.127"
userName = "root"
password = "***"
#前台页面打包脚本路径
frontendBuildPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-frontend\\build\\"
#后台打包脚本路径
jarPackBuildPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-parent\\"
jarBatCompName = "打包-公司环境.bat"
#具体上传到服务器的文件
frontendPath = 'C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-frontend\\build\dist-pc.zip'
systemJarPath = 'C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-parent\\hbtobacco-dyxvisualization-system\\tatger\\hbtobacco-dyxvisualization-system.jar'
kanbanJarPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-parent\\hbtobacco-dyxvisualization-kanban\\target\\hbtobacco-dyxvisualization-kanban.jar"
#上传jar包和zip文件到服务器配置
FrontendlinuxPath = '/home/dyxvisual/dist-pc.zip'
SystemlinuxPath = '/root/hbtobacco-dyxvisualization-system.jar'
KanbanlinuxPath = '/root/hbtobacco-dyxvisualization-kanban.jar'
#ssh命令
cdStr = 'cd /home/dyxvisual/; '

#3d可视化到开发环境打包
if(__name__=="__main__"):
    
    #切换目录,打包前台项目
    print("开始打包前台项目...")
    os.chdir(frontendBuildPath)
    os.system("build.bat")
    print("前台项目打包完成！")
    
    #切换目录,打包后台项目
    print("开始打包后台项目...")
    os.chdir(jarPackBuildPath)
    os.system(jarBatCompName)
    print("后台项目打包完成!")
    
    
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
    
    if isFrontend:
        #上传文件
        print("链接服务器成功，开始上传dist-pc.zip,请等待...")
        result = sftp.put(frontendPath, FrontendlinuxPath)
        if result:
            print("前端zip上传成功!")
            #执行命令
            stdin, stdout, stderr = ssh.exec_command(cdStr + ' unzip -o dist-pc.zip')
            print(stdout.read().decode())
        else:
            print("前端上传失败!")
    
    if isSystem:
        #上传文件
        print("链接服务器成功，开始上传system.jar,请等待...")
        result = sftp.put(systemJarPath, SystemlinuxPath)
        if result:
            print("system上传成功!")
            #执行命令
            pwdi,pwdo,pwde = ssh.exec_command(cdStr + ' pwd')
            print(pwdo.read().decode())
            stdin, stdout, stderr = ssh.exec_command(cdStr + ' sh deploy-dyxvisual.sh system_start')
            print(stdout.read().decode())
        else:
            print("system上传失败!")
    
    if isKanban:
        #上传文件
        print("链接服务器成功，开始上传kanban.jar,请等待...")
        result = sftp.put(kanbanJarPath, KanbanlinuxPath)  
        if result:
            print("kanban上传成功!")
            #执行命令.好坑!就是execute_command() 他是a single session，每次执行完后都要回到缺省目录。所以可以 .execute_command('cd  /var; pwd')
            pwdi,pwdo,pwde = ssh.exec_command(cdStr + ' pwd')
            print(pwdo.read().decode())
            stdin, stdout, stderr = ssh.exec_command(cdStr + ' sh deploy-dyxvisual.sh kanban_start')
            print(stdout.read().decode())
        else:
            print("kanban上传失败!")
            
    # 关闭连接  
    print("关闭连接")
    sftp.close()  
    ssh.close()