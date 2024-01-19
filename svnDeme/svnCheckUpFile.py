import os

# 创建一个空的集合  
my_set = set()
# 添加一些字符串到集合中  
my_set.add("connection.properties")
my_set.add("application.properties")
my_set.add("wsdJedisConfig.properties")
my_set.add("server.properties")
my_set.add("logback-spring.xml")
my_set.add("Dockerfile")
my_set.add("gen.java")
my_set.add("GEN.java")
my_set.add("genQuality.java")
my_set.add("pom.xml")
my_set.add("Test.java")
my_set.add("hbtobacco-dyxmes-web")
my_set.add("build.bat")
my_set.add("dyxvisuali-nginx.conf")
my_set.add("output.txt")

#启动！
if __name__=='__main__': 
    path = 'C:\WisdomInfo\IdeaWorkspace\svn\ERD预销售库\ERD_PROJ\java_wh_2021\hbprojects\hbzy\dyxmesProject'
    os.chdir(path)
    print("当前路径",os.getcwd())
    print("开始检测当前目录下svn文件状态")
    os.system("svn status --show-updates > output.txt")
    #打开文件
    with open('output.txt', 'r') as file:
        # 逐行读取文件
        for line in file:
            # 打印每一行，去掉行尾的换行符
            strLine = line.strip()
            # 找到最后一个反斜杠的位置  
            index = strLine.rfind("\\")
            # 如果找到了反斜杠  
            if index != -1:
                # 截取反斜杠及其后面的内容  
                substring = strLine[index + 1:]
                #print(substring)
                if substring in my_set:
                    #print("字符串已存在于集合中")
                    continue
                else:
                    print(substring)
            #else:
                #print(strLine)
    print("检测完毕，以上是当前目录中可能需要提交的文件信息。")