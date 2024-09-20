import os
import xlrd

from time import sleep,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


xlsPath = 'C:\MyProject\Vs-Code\dataModelAuto\云MES系统实体清单-0326.xls'
checkXmlPath = 'C:\MyProject\Vs-Code\dataModelAuto\数据模型补充分工表.xls'
dataMbUrl = 'https://szzt-sjzt.hbtobacco.cn/dmm/dam-imm-web/model/dataModel'

# 主函数
if(__name__=="__main__"):
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
    wait = WebDriverWait(chrome, 10)
    
    print("成功进入数据模型维护页面")
    # 等会
    sleep(5)
    
    # 到这里初始工作就结束了，后面就是循环里面处理各个表的数据了

    # 打开excel文件
    workbook = xlrd.open_workbook(xlsPath)
    # 获取所有的sheet页
    sheet_names = workbook.sheet_names()
    #print(len(sheet_names))
    for sheet_name in sheet_names:    
        # 跳过 '表关系图' 页
        if sheet_name == '表关系图':
            continue
        # 获取sheet页
        sheet = workbook.sheet_by_name(sheet_name)
        # 获取sheet页名 (行数，列数)
        print(sheet.name, sheet.nrows, sheet.ncols)
        # 截取sheet页名 - 分割 前面是模型英文名称 后面是模型中文名称
        sheetName = sheet.name.split('-')
        print(sheetName)
        # 模型英文名称
        mxCode = sheetName[0]
        # 模型中文名称
        modelChineseName = sheetName[1]
        
        #拿到了数据模型表名和模型中文名称 直接操作浏览器搜索模型
        input_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='请输入内容']")))
        # 分两次查询 有时候code可以匹配，有的时候 中文可以匹配
        input_fields[0].send_keys(mxCode)
        #后面code查不到的时候在用名称查一遍
        #input_fields[1].send_keys(modelChineseName)
        
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
        # 不出意外一般是成功了,直接定位页面 el-table-body 元素 他们好像是把一个table切成了四个
        table_body = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-table__body")))
        # 最后一个就是编辑和删除的按钮框
        table_element = table_body[3]
        #之后获取这个表格元素里的 tbody
        tbody_element = table_element.find_element(By.TAG_NAME, "tbody")
        trRows = tbody_element.find_elements(By.TAG_NAME, "tr")
        print("表格元素定位成功,共有%d行数据" % len(trRows))
        # 判断列表是否为空 为空就停止程序
        if len(trRows) == 0:
            # 那就说明没有找到 mxCode的模型，切换用模型中文名称试一次
            backBtnClean.click() # 重置页面查询条件
            input_fields[1].send_keys(modelChineseName) # 输入中文名称
            query_button.click()
            # 然后再看看有没有数据模板
            query_body = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-table__body")))
            query_element = query_body[3]
            queryBody_element = query_element.find_element(By.TAG_NAME, "tbody")
            queryTrRows = queryBody_element.find_elements(By.TAG_NAME, "tr")
            print("表格元素重新定位成功,共有%d行数据" % len(queryTrRows))
            if len(queryTrRows) > 0:
                trRows = queryTrRows
            else:
                print("没有找到表名为\t"+mxCode+"\t 模型中文名称为\t"+modelChineseName+"\t的数据，请检查数据模型名称是否正确！")
                print("程序退出！")
                exit()
        # 按理就只有一条数据，因为就一个数据模板，所以默认取第一个吧
        tr_element = trRows[0]
        # 然后通过class=el-table_1_column_10 is-center  is-hidden el-table__cell 定位到 编辑按钮触发
        # 查看tr_element所有子元素  10个td
        #print(tr_element.find_elements(By.TAG_NAME, "td").__len__())
        # 获取最后的td
        td_element = tr_element.find_elements(By.TAG_NAME, "td")[9]
        # 查看td里面的所有子元素
        #print(td_element.find_elements(By.TAG_NAME, "a").__len__())
        # 按理就俩a标签，第一个是编辑，第二个是删除，获取第一个编辑按钮，然后触发
        edit_button = td_element.find_elements(By.TAG_NAME, "a")[0]
        edit_button.click()
       
        #这时候就要弹出模态框了，进行编辑，把excel的对应数据填写到表单中即可。
        # 获取父级中的 section 元素
        section_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'section')))
        # 从section中获取各个对应的输入框即可。
        # 先获取 class="dam_imm-info_model_edit"的div 这是大编辑form
        edit_div = section_element.find_element(By.CLASS_NAME, "dam_imm-info_model_edit")
        # 然后获取它下面的 class="mt-8" div 这是主从表的容器
        main_div = edit_div.find_element(By.CLASS_NAME, "mt-8")
        # 直接获取main_div里面所有包括子元素里面的 class="el-input__inner"
        input_elements = main_div.find_elements(By.CLASS_NAME, "el-input__inner")
        print("一共有%d个输入框" % input_elements.__len__())
        # 输出所有输入框的name和value
        for input_element in input_elements:
            print(input_element.get_attribute("name"), input_element.get_attribute("value"))
        #数据模型标准名称
        input_elements[2].clear()
        input_elements[2].send_keys(mxCode)
        
        #数据模型源表名
        input_elements[3].clear()
        input_elements[3].send_keys(mxCode)
        
        #数据模型中文名
        input_elements[4].clear()
        input_elements[4].send_keys(modelChineseName)
        
        #数据库英文名称 - 要去checkXmlPath里面匹配一下，然后刷新进去
        input_elements[8].clear()
        input_elements[8].send_keys(4)
        
        
        
        
        # 数据库表名
        tableName = ""
        # 数据库名
        tableEnglishName = ""
        # 遍历所有的行  目前已知 每页8列 行数未知
        # 字段名	字段类型	字段长度	数字长度	小数位数	能否为NULL	字段说明	代码类别
        for row in range(sheet.nrows):
            # 跳过 第一行
            if row == 0:
                continue
            row_values = sheet.row_values(row)
            print(row_values)
            # 字段名 统一转为大写
            zdm = row_values[0]
            zdm = zdm.upper()
            # 字段类型
            zdlx = row_values[1]
            # 字段长度
            zdcd = row_values[2]
            # 数字长度
            szcd = row_values[3]
            # 小数位数
            xsws = row_values[4]
            # 能否为NULL
            nfwn = row_values[5]
            isNull = nfwn
            # 字段说明
            zdsm = row_values[6]
            # 代码类别
            dylb = row_values[7]
        
        # 定位id=el-drawer__title的headle里面有一个button 触发
        #headleClose_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#el-drawer__title > button")))
        #headleClose_button.click()
        
        #定位 aria-label="close 数据模型管理" 的button 按钮 点击执行关闭
        close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='close 数据模型管理']")))
        close_button.click()
        # 打印分割线
        print("==================================================================================================================")
        # 循环一次就结束
        break


