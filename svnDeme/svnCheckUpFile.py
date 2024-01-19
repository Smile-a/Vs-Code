import os
import json

#启动！
if __name__=='__main__':
    #程序根路径
    rootPath = os.getcwd()
    print(rootPath)
    # 读取 JSON 文件  
    with open(rootPath+'\\verificationRejection.json', 'r',encoding="utf-8") as file:
        jsonData = json.load(file)
    #我要检测的项目svn目录
    path = jsonData['svnProjectPath']
    os.chdir(path)
    print("路径已切换，当前路径",os.getcwd())
    print("开始检测当前目录下svn文件状态,输出至output.txt")
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
                if substring in jsonData:
                    #print("字符串已存在于集合中")
                    continue
                else:
                    print(substring)
            #else:
                #print(strLine)
    print("检测完毕，以上是当前目录中可能需要提交或更新的文件信息。")