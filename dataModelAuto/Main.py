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

# 通过excel文件匹配数据模型的数据库英文名称
def checkExcel():
    # 创建一个字典来存储数据
    data_map = {}
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
        # 将第一列作为值，第二列作为key
        value = row_values[0]
        key = row_values[1]
        # 存储到字典中
        data_map[key] = value
        # 打印每行的内容
        #print(sheet.row_values(row)[1] + "\t" + sheet.row_values(row)[0])
    return data_map

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
    dataMap = checkExcel()
    # 打印字典大小
    print(f"dataMap_size: {len(dataMap)}")

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
        # 获取和mt-8同级的div class="drawerBtn" 这是暂存按钮的div容器，里面有个button才是真的暂存按钮
        drawerBtn_div = edit_div.find_element(By.CLASS_NAME, "drawerBtn")
        # 获取它下面的 button 元素 这是暂存按钮
        zcSave_button = drawerBtn_div.find_element(By.TAG_NAME, "button")
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
        key_to_check = mxCode
        if key_to_check in dataMap:
            print(f"{key_to_check} 存在于字典中，对应的值为：{dataMap[key_to_check]}")
            input_elements[8].clear()
            input_elements[8].send_keys(dataMap[key_to_check])
        else:
            print(f"{key_to_check} 不存在于字典中")
        
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
            # 能否为NULL   YES NO
            nfwn = row_values[5]
            # 修改yes no  为 true false
            if nfwn == "YES":
                # 允许为空 改为 false 页面控件就不点亮
                nfwn = "false"
            else:
                # 不允许为空 改为 true 页面控件就点亮
                nfwn = "true"
            isNull = nfwn
            # 字段说明
            zdsm = row_values[6]
            # 代码类别
            dylb = row_values[7]
            
            # 这时候已经获取到了当前行里的所有元素，然后依次进行填充
            # 先获取当前模态窗里面 id="pane-column" 的元素 这里面会有手动添加按钮和数据列表
            tabpanel = edit_div.find_element(By.ID, "pane-column")
            
            # 获取tabpanel里面的button 一共有五个，获取第四个"手动添加"按钮
            add_button = tabpanel.find_elements(By.TAG_NAME, "button")[3]
            add_button.click()
            
            #定位弹窗的class="el-drawer__wrapper" 有很多个
            drawers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'el-drawer__wrapper')))
            # 获取最后一个元素 也就是 手动添加的弹窗
            drawerAddForm = drawers[-1]
            
            # 开始输入值 获取所有input标签
            input_elements = drawerAddForm.find_elements(By.TAG_NAME, "input")
            # 一共是有11个
            print("一共有%d个input元素" % len(input_elements))
            # 开始给对应的输入框赋值 第一个输入框是 源字段名
            input_elements[0].send_keys(zdm)
            # 第二个输入框是 字段中文名
            input_elements[1].send_keys(zdsm)
            # 第四个输入框是 字段类型 比如是varchar int date datetime decimal 全部改成首字母大写
            zdlx = zdlx.capitalize()
            input_elements[3].send_keys(zdlx)
            # 第五个输入框是 字段长度
            input_elements[4].send_keys(zdcd)
            # 第六个输入框是 小数位 如果zdlx是decimal 才需要设置
            if zdlx == "Decimal":
                input_elements[5].send_keys(xsws)
            # 第九个是 能否为NULL
            input_elements[8].send_keys(isNull)
            
            #获取里面 class="drawerBtn" 元素里面的 button  这是保存按钮
            drawerBtnDiv = drawerAddForm.find_element(By.CLASS_NAME, "drawerBtn")
            saveBtn = drawerBtnDiv.find_element(By.TAG_NAME, "button")
            saveBtn.click()
            
            # 检测页面是否有弹出提示 role="alert" 的元素
            alert_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='alert']")))
            alert_text = alert_element.text
            #判断是不是 源字段名已存在，请修改！
            if "源字段名已存在，请修改！" in alert_text:
                # 获取关闭按钮
                sdxgzdCloseBtn = drawerAddForm.find_element(By.TAG_NAME, "i")
                sdxgzdCloseBtn.click()
                #可以换下一个字段了
                continue
            
        # 数据模型的字段都修改好了 可以直接点击暂存按钮了
        zcSave_button.click()
        #之后就可以关闭弹窗了，定位 aria-label="close 数据模型管理" 的button 按钮 点击执行关闭数据模型修改模态框
        close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='close 数据模型管理']")))
        close_button.click()
        
        # 打印分割线
        print("==================================================================================================================")
        # 循环一次就结束
        break


