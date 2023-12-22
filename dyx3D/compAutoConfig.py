#是否上传开关 True上传，但只是上传到服务器，并不会阻止他们拉代码和打包
#前台
isFrontend = False
#系统模块
isSystem = False
#看板模块
isKanban = False
#路径配置
ipAddr = "192.168.42.127"
userName = "root"
password = "whlinux"
#前台项目文件夹地址--懒得在脚本里面svn update
frontendDirPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-frontend\\"
#前台页面打包脚本路径
frontendBuildPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-frontend\\build\\"
#前台页面打包脚本文件--ps 把最后一行的pause干掉或者注释掉 不然会卡住 ::pause
frontendBatName = "build.bat"
#后台打包脚本路径
jarPackBuildPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-parent\\"
#在调用这个bat的时候先去把他最后一行的cmd /k注释掉，不然会卡住
jarBatCompName = "打包-公司环境.bat"
#具体上传到服务器的文件在本地的路径，防止奇怪的问题全放真实路径
frontendPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-frontend\\build\dist-pc.zip"
systemJarPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-parent\\hbtobacco-dyxvisualization-system\\target\\hbtobacco-dyxvisualization-system.jar"
kanbanJarPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxvisualization-parent\\hbtobacco-dyxvisualization-kanban\\target\\hbtobacco-dyxvisualization-kanban.jar"
#上传jar包和zip文件到服务器配置
FrontendlinuxPath = '/home/dyxvisual/dist-pc.zip'
SystemlinuxPath = '/root/hbtobacco-dyxvisualization-system.jar'
KanbanlinuxPath = '/root/hbtobacco-dyxvisualization-kanban.jar'
#ssh命令
cdStr = 'cd /home/dyxvisual/; '