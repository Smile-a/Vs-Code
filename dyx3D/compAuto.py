import os
import sys
import json
import socket
import paramiko
#import compAutoConfig

# 打包成exe基础命令就够了，默认会打包成文件夹
# pyinstaller -D -c -i naotou.ico compAuto.py 文件夹
# pyinstaller -F -c -i naotou.ico compAuto.py 单个文件
# -D 默认文件夹  -F 单个文件 -c 默认黑框框  -w 隐藏黑框框

#3d可视化到开发环境打包
if(__name__=="__main__"):
    #多此一举的操作
    #pyFilePath = sys.path[0] #py脚本用这个
    pyFilePath = os.getcwd()  #打包成exe要用这个
    print("程序路径:",pyFilePath)
    
    print("【淡雅香3D可视化项目公司环境自动打包脚本】")
    print("可能会较慢，因为是从本地上传的奥~")
    
    # 读取文件内容  
    with open('compAutoConfig.json', 'r' ,encoding="utf-8") as file:
        jsonFileData = json.load(file)
        print(jsonFileData)
    
    #如果有想法的话可以自己改造，通过命令行输入的参数来启动对应的模块
    # @echo off  
    # python "C:\\MyProject\\Vs-Code\\dyx3D\\compAuto.py" %* kanabn
    # ::pause
    #param = sys.argv[1]
    #print("跟随命令传入的参数为:",param)
    
    #判断是否打包前端
    if jsonFileData['isFrontend']:
        #切换目录,打包前台项目
        print("开始更新前台项目...")
        os.chdir(jsonFileData['frontendDirPath'])
        os.system("svn update")
        print("前台项目svn更新完毕...")
        
        print("开始打包前台项目...")
        os.chdir(jsonFileData['frontendBuildPath'])
        os.system(jsonFileData['frontendBatName'])
        print("前台项目打包完成！")
    
    #判断是否打包后台
    if jsonFileData['isSystem'] or jsonFileData['isKanban']:
        #切换目录,打包后台项目
        print("开始打包后台项目...")
        os.chdir(jsonFileData['jarPackBuildPath'])
        os.system(jsonFileData['jarBatCompName'])
        print("后台项目打包完成!")
    
    #切换回来--py文件没问题，exe打包成单独文件就不可以看了，因为是zip
    os.chdir(pyFilePath)
    print("自动化开始!")
    
    # 创建一个套接字对象，连接到远程服务器  
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    sock.connect((jsonFileData['ipAddr'], 22))  
    
    # 创建SSHClient对象，并设置连接参数  
    ssh = paramiko.SSHClient()  
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  
    
    # 连接服务器  
    ssh.connect(hostname=jsonFileData['ipAddr'], username=jsonFileData['userName'], password=jsonFileData['password'], sock=sock) 
    
    # 创建SFTPClient对象，并传入SSH连接  
    sftp = paramiko.SFTPClient.from_transport(ssh.get_transport())  
    
    if jsonFileData['isFrontend']:
        #上传文件
        print("链接服务器成功，开始上传dist-pc.zip,请等待...")
        result = sftp.put(jsonFileData['frontendPath'], jsonFileData['FrontendlinuxPath'])
        if result:
            print("前端zip上传成功!")
            #执行命令
            stdin, stdout, stderr = ssh.exec_command(jsonFileData['cdStr'] + ' unzip -o dist-pc.zip')
            print(stdout.read().decode())
        else:
            print("前端上传失败!")
    
    if jsonFileData['isSystem']:
        #上传文件
        print("链接服务器成功，开始上传system.jar,请等待...")
        result = sftp.put(jsonFileData['systemJarPath'], jsonFileData['SystemlinuxPath'])
        if result:
            print("system上传成功!")
            #执行命令
            pwdi,pwdo,pwde = ssh.exec_command(jsonFileData['cdStr'] + ' pwd')
            print(pwdo.read().decode())
            stdin, stdout, stderr = ssh.exec_command(jsonFileData['cdStr'] + ' sh deploy-dyxvisual.sh system_start')
            print(stdout.read().decode())
        else:
            print("system上传失败!")
    
    if jsonFileData['isKanban']:
        #上传文件
        print("链接服务器成功，开始上传kanban.jar,请等待...")
        result = sftp.put(jsonFileData['kanbanJarPath'], jsonFileData['KanbanlinuxPath'])
        if result:
            print("kanban上传成功!")
            #执行命令.好坑!就是execute_command() 他是a single session，每次执行完后都要回到缺省目录。所以可以 .execute_command('cd  /var; pwd')
            pwdi,pwdo,pwde = ssh.exec_command(jsonFileData['cdStr'] + ' pwd')
            print(pwdo.read().decode())
            stdin, stdout, stderr = ssh.exec_command(jsonFileData['cdStr'] + ' sh deploy-dyxvisual.sh kanban_start')
            print(stdout.read().decode())
        else:
            print("kanban上传失败!")
    
    # 关闭连接  
    print("自动化结束，关闭连接")
    sftp.close()
    ssh.close()
    
    os.system("pause")