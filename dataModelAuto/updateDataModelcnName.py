import os
import xlrd
import redis

from tqdm import tqdm
from time import sleep,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

checkXmlPath = 'C:\MyProject\Vs-Code\dataModelAuto\数据模型补充分工表.xls'
dataMbUrl = 'https://szzt-sjzt.hbtobacco.cn/dmm/dam-imm-web/model/dataModel'

#用来存储成功修改了的数据模型
r = redis.Redis(host='localhost', port=6379, db=6) 

# 防止网络掉线定时调用接口刷新浏览器页面
def refreshChrome():
    options = webdriver.ChromeOptions()
    # 配置调试端口
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #加载谷歌浏览器驱动
    chrome = webdriver.Chrome(options=options)
    # 打开指定url
    chrome.get(dataMbUrl)
    #刷新页面
    chrome.refresh()
    print("刷新页面成功")

def alertMesBox(wait):
    try:
        # 检测一下，当前页面有没有弹窗 一个class="el-message-box__btns" 的消息提醒框，如果有，就获取里面的button元素确定
        messBoxBtn = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'el-message-box__btns')))
        #判断是否存在 并且文本不为空
        if messBoxBtn and messBoxBtn.text != "":
            print("检测到弹窗")
            # 获取里面的button元素确定
            messBoxBtn.find_element(By.TAG_NAME, "button").click()
        else:
            #print("没有检测到弹窗")
            pass
    except Exception as e:
        print("没有找到弹窗，不予理会~")


#开始执行自动化功能
def automationBegins():
    pyFilePath = os.getcwd()
    print("【云MES数据中台-数据模型维护脚本】" + "\t程序路径:" + pyFilePath)
    
    #谷歌浏览器驱动配置
    print("开始操作浏览器~")
    options = webdriver.ChromeOptions()
    # 配置调试端口
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #加载谷歌浏览器驱动
    chrome = webdriver.Chrome(options=options)
    # 打开指定url
    chrome.get(dataMbUrl)
    print(chrome.title)
    # 使用显示等待确保元素已经加载完成
    wait = WebDriverWait(chrome, 2)
    
    print("成功进入数据模型维护页面")
    # 等会
    sleep(5)

    # 打开excel文件
    workbook = xlrd.open_workbook(checkXmlPath)
    # 获取第一页的sheet页
    sheet = workbook.sheet_by_index(0)
    # 打印所有行信息
    for row in range(sheet.nrows):
        # 跳过第一行
        if row == 0:
            continue
        # 获取每行的内容
        row_values = sheet.row_values(row)
        # 将第2列作为code，第3列作为name
        mxCode = row_values[1]
        # 如果mxCode在redis中，就跳过
        if r.sismember('successList', mxCode):
            print("模型"+mxCode+"已经存在Redis中，跳过该项")
            continue
        mxName = row_values[2]
        #检测弹窗
        alertMesBox(wait)
        # 输入框
        input_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='请输入内容']")))
        # 忘记了 循环的时候，之前的值没有干掉奥，手动清空
        input_fields[0].clear()
        input_fields[1].clear()
        alertMesBox(wait) #弹窗
        # 分两次查询 有时候code可以匹配，有的时候 中文可以匹配
        input_fields[0].send_keys(mxCode)
        # 直接点击查询按钮
        col_elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-col.el-col-24")))
        # 获取第四个 .el-col el-col-24 元素   就是重置 查询那个div
        fourth_col_element = col_elements[3]
        # 找到该元素中的所有 button 元素
        button_elements = fourth_col_element.find_elements(By.CSS_SELECTOR, "button")
        # 提前设置一下页面重置按钮，说不定后面会用到
        backBtnClean = None
        query_button = None
        # 遍历所有 button 元素，找到 span 为“查询”的按钮并点击
        for button in button_elements:
            span_elements = button.find_elements(By.CSS_SELECTOR, "span")
            if len(span_elements) > 0 and span_elements[0].text == "重置":
                # 设置重置按钮
                backBtnClean = button
            if len(span_elements) > 0 and span_elements[0].text == "查询":
                query_button = button
                button.click()
                print("点击了'查询'按钮")
                break
        sleep(3)
        # 不出意外一般是成功了,直接定位页面 el-table-body 元素 他们好像是把一个table切成了四个
        table_body = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-table__body")))
        # 最后一个就是编辑和删除的按钮框
        table_element = table_body[3]
        #之后获取这个表格元素里的 tbody
        tbody_element = table_element.find_element(By.TAG_NAME, "tbody")
        trRows = tbody_element.find_elements(By.TAG_NAME, "tr")
        print("表格元素定位成功,共有%d行数据" % len(trRows))
        # 判断列表是否为空  先只用code匹配一轮，后面再用名称看看，光用名称好像有点问题.
        if len(trRows) == 0:
            print("没有找到模型："+mxCode)
            #execl表中有模型信息，但是通过code在浏览器查询没有数据，保存到webDataNullList下后面手动处理
            r.sadd('webDataNullList', sheet.name)
            continue
        tr_element = None
        #还是获取结果进行匹配吧，哪怕用code和name一起，它搜索结果还是多个
        headTable = table_body[2]
        # 打印headTable所有元素
        for tr in headTable.find_elements(By.TAG_NAME, "tr"):
            tds = tr.find_elements(By.TAG_NAME, "td")
            sjmxybmL = tds[3]
            if sjmxybmL.text == mxCode:
                print("excel中的code和页面查询到的数据code完全匹配!!! "+sjmxybmL.text)
                # 记录一个下标
                tr_element_num = tds[1].text
                # 就是要编辑这一行 这样就能定位到code搜索结果返回多个数据里最符合的那行数据了
                tr_element = trRows[int(tr_element_num) - 1] #trRows里面是下标 num存的是序号，所以要减一
                break
        # 这里有一种情况，有模糊匹配的结果，但是T_P开头，匹配不到 那不还是NONe
        if tr_element == None:
            print(f"******没有完全匹配CODE的模板，跳过该项数据,模板code:{mxCode}******")
            # 这种情况是通过code可以模糊匹配到数据，但是对应的数据表名有可能是T_P开头这种,以及code模糊相似名称不同的，就需要手动处理了
            r.sadd('TpList', sheet.name)
            continue
        # 然后通过class=el-table_1_column_10 is-center  is-hidden el-table__cell 定位到 编辑按钮触发
        # 查看tr_element所有子元素  10个td
        #print(tr_element.find_elements(By.TAG_NAME, "td").__len__())
        # 获取最后的td
        td_element = tr_element.find_elements(By.TAG_NAME, "td")[9]
        # 查看td里面的所有子元素
        #print(td_element.find_elements(By.TAG_NAME, "a").__len__())
        # 按理就俩a标签，第一个是编辑，第二个是删除，获取第一个编辑按钮，然后触发
        edit_button = td_element.find_elements(By.TAG_NAME, "a")[0]
        alertMesBox(wait) # 检测弹出提示框
        try:
            edit_button.click()
        except Exception as e:
            r.sadd('stopUsingList', sheet.name)
            print("编辑按钮触发失败，跳过该项数据")
            continue
        #太快了没加载出来就会报错
        sleep(2)
        #这时候就要弹出模态框了，进行编辑，把excel的对应数据填写到表单中即可。
        # 获取父级中的 section 元素
        section_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'section')))
        # 从section中获取各个对应的输入框即可。
        # 先获取 class="dam_imm-info_model_edit"的div 这是大编辑form
        edit_div = section_element.find_element(By.CLASS_NAME, "dam_imm-info_model_edit")
        # 获取和mt-8同级的div class="drawerBtn" 这是暂存按钮的div容器，里面有个button才是真的暂存按钮
        drawerBtn_div = edit_div.find_element(By.CLASS_NAME, "drawerBtn")
        # 获取它下面的 button 元素 这是暂存按钮
        zcSave_button = drawerBtn_div.find_element(By.TAG_NAME, "button")
        # 然后获取它下面的 class="mt-8" div 这是主从表的容器
        main_div = edit_div.find_element(By.CLASS_NAME, "mt-8")
        # 直接获取main_div里面所有包括子元素里面的 class="el-input__inner"
        input_elements = main_div.find_elements(By.CLASS_NAME, "el-input__inner")
        print("一共有%d个输入框" % input_elements.__len__())
        
        #数据模型中文名 获取input里的内容
        #datamodleCname = input_elements[4].get_attribute("value")
        input_elements[4].clear()
        input_elements[4].send_keys(mxName)
        
        #只修改模型中文名称，然后暂存即可
        zcSave_button.click()
        print("数据模型修改完毕，暂存成功！！！")
    
        #之后就可以关闭弹窗了，定位 aria-label="close 数据模型管理" 的button 按钮 点击执行关闭数据模型修改模态框
        close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='close 数据模型管理']")))
        sleep(2)
        close_button.click()
         # 这一个sheet页的数据就都处理完毕了，把sheet页的code存储到redis的successList里面，下次循环就可以跳过这个sheet页了
        r.sadd("successList", mxCode)


# 主函数
if(__name__=="__main__"):
    # 启动次数
    num = 1
    # 最大重试次数
    max_attempts = 100
    # 循环执行
    while True:
        if num < max_attempts:
            try:
                print(f"自动流程启动第{num}次")
                # 正常执行脚本任务
                automationBegins()
                print("所有任务正常走完了？  程序结束!")
                break
                
                # 刷新浏览器
                # refreshChrome()
                # sleep(60)
            except Exception as e:
                print("自动化发生了异常，准备重新启动~")
            finally:
                num += 1
        else:
            print("达到最大启动次数，停止尝试。")
            break
