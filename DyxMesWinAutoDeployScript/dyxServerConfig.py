#页面登录用户名称
loginUserName = "anwei"
#页面本地密码
qwPassword='An123456'
#你电脑里企业微信地址
wxWorkPath = 'C:\Program Files (x86)\WXWork\WXWork.exe'
#ping堡垒机的地址
pingHostname = "10.157.234.151"
#堡垒机登录页面url
bljLoginPathUrl = "https://10.157.234.151/index.php/Public/index/stra_name/sms_local"
bljAllListPathUrl = "https://10.157.234.151/index.php/UserWork/index/type/all/cpu/64"
#winscp软件窗口标题
winsctTitle = "@10.157.234.151 – WinSCP"
#Xshell软件窗口标题
xshellTitle = 'root@kjymessjzjjtest:~ - Xshell'
#前台页面项目总路径
frontendProPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxmes-frontend\\"
#前台页面打包脚本
frontendBuildPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxmes-frontend\\build\\build.bat"
#前台页面打包好的存放路径
frontendPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxmes-frontend\\build\\"
#前台打包好的zip
frontendZipName = "dist-pc.zip"
#jar包存放的路径
jarFilesPath = "C:\\Users\\wsd\\eclipse-workspace\\dyxmesProject\\hbtobacco-dyxmes-parent\\"
#目前测试服务器这几个是在59的
jar_system = jarFilesPath + "hbtobacco-dyxmes-system\\target\\"
jar_system_Name = "hbtobacco-dyxmes-system.jar"
#===
jar_plan = jarFilesPath + "hbtobacco-dyxmes-plan\\target\\"
jar_plan_Name = "hbtobacco-dyxmes-plan.jar"
#目前测试服务器这几个是在60的
jar_base = jarFilesPath + "hbtobacco-dyxmes-base\\target\\"
jar_base_Name = "hbtobacco-dyxmes-base.jar"
#===
jar_quality = jarFilesPath + "hbtobacco-dyxmes-quality\\target\\"
jar_quality_Name = "hbtobacco-dyxmes-quality.jar"
#===
jar_warehouse = jarFilesPath + "hbtobacco-dyxmes-warehouse\\target\\"
jar_warehouse_Name = "hbtobacco-dyxmes-warehouse.jar"
#这俩是install的
jar_commonapi = jarFilesPath + "hbtobacco-dyxmes-commonapi"
jar_mobile = jarFilesPath + "hbtobacco-dyxmes-mobile"
#maven打包环境 test pro
maven_Profile = "test"
#那个json文件是存储登录信息的，各个服务器的登录参数，有多少个节点他就会去获取对应的参数信息
#加个有点多余的参数吧，免得去改脚本里面的参数，在这里加对应json文件里面的前台服务器标题，你要部署哪一台机器，就填哪一个json的key，一定要对应奥不然找不到就尴尬了
frontendTitleKey = "test_10_156_53_58"
testOneTitleKey = "test_10_156_53_59"
testTwoTitleKey = "test_10_156_53_60"
#做个发布开关吧
isFrontend=False
isSystem=False
isPlan=False
isBase=False
isQuality=False
isWarehouse=False
#鼠标移动需要使用到的坐标参数，每个电脑第一次配置好就可以了,使用文件夹里的移动坐标工具就可以直接得到需要的坐标
#企业微信窗口左上角到消息图标的x,y坐标偏移值，不是他们的坐标，是需要移动多少到达这个位置
msgLogo_X=28
msgLogo_Y=88
#从消息菜单到消息通知的x,y坐标偏移值
NotifyLogo_X=90
NotifyLogo_Y=129
#双击消息通知联系人，会把聊天窗口弹出来，作为一个独立的窗口，这个窗口的的左上角到他的聊天记录log的x,y坐标偏移值，不是他们的坐标，是需要移动多少到达这个位置
MessageLogo_X=230
MessageLogo_Y=391
#最后一个，定位验证码的位置，就是消息记录按钮log的坐标，到最新一条验证码的坐标偏移量，y轴上移,不用带-，直接填值。
yzmCode_X=14
yzmCode_Y=65