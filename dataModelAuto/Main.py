import os
import xlrd

from time import sleep,time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


xlsPath = 'C:\MyProject\Vs-Code\dataModelAuto\云MES系统实体清单-0326.xls'
dataMbUrl = 'file:///C:/Users/wsd/Desktop/%E6%95%B0%E6%8D%AE%E4%B8%AD%E5%8F%B0.html'

# 主函数
if(__name__=="__main__"):
    pyFilePath = os.getcwd()
    print("【云MES数据中台-数据模型维护脚本】" + "\t程序路径:" + pyFilePath)
    
    #谷歌浏览器驱动配置
    print("开始操作浏览器~")
    options = webdriver.ChromeOptions()
    #selenium默认是会执行完关闭浏览器的，这样设置一下先不关闭，最后执行手动quit即可。
    options.add_experimental_option('detach', True)
    #加载谷歌浏览器驱动
    chrome = webdriver.Chrome(options=options)
    #设置浏览器窗口最大化
    chrome.maximize_window()
    # 打开指定url
    chrome.get(dataMbUrl)
    # 使用显示等待确保元素已经加载完成
    wait = WebDriverWait(chrome, 10)
    
    # 1.选中左侧菜单 数据模型管理
    print("选中左侧菜单 数据模型管理")
    # 获取id 为 menu_scrollbar 的元素
    sjmxwh = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu_scrollbar"]')))
    # 直接获取【数据模型维护】的a标签 直接触发效果
    #submenu_item = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="https://szzt-sjzt.hbtobacco.cn/dmm/dam-imm-web/model/dataModel"]')))
    # 点击子菜单项
    #submenu_item.click()
    # 页面右侧数据更新等待
    sleep(3)
    print("成功进入数据模型维护页面")
    
    # 安全起见 直接输入关键字定位数据模型列表
    input_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='输入关键字进行过滤']")))
    # 输入文本值  云MES系统    回车触发搜索
    input_field.send_keys("云MES系统")
    input_field.send_keys(Keys.RETURN)
    sleep(3)
    
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
        # 遍历所有 button 元素，找到 span 为“查询”的按钮并点击
        for button in button_elements:
            span_elements = button.find_elements(By.CSS_SELECTOR, "span")
            if len(span_elements) > 0 and span_elements[0].text == "查询":
                button.click()
                print("点击了带有文本 '查询' 的按钮")
                break
        # 不出意外 一般是 成功了
        # 通过当前页面唯一class定位到数据表格grid el-table el-table--fit el-table--striped el-table--border el-table--scrollable-x el-table--scrollable-y el-table--enable-row-transition el-table--small
        grid_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".el-table.el-table--fit.el-table--striped.el-table--border.el-table--scrollable-x.el-table--scrollable-y.el-table--enable-row-transition.el-table--small")))
        # grid_element元素下的class定位到table el-table__body-wrapper is-scrolling-left
        table_element = grid_element.find_element(By.CSS_SELECTOR, ".el-table__body-wrapper.is-scrolling-left")
        # 准确的说是装table的div，继续获取里面的<tbody>元素，这才是存放<tr><td>的元素
        tbody_element = table_element.find_element(By.TAG_NAME, "tbody")
        print("表格元素定位成功,共有%d行数据" ,tbody_element.find_elements(By.TAG_NAME, "tr").__len__())
        # 按理就只有一条数据，因为就一个数据模板，所以默认取第一个吧
        tr_element = tbody_element.find_element(By.TAG_NAME, "tr")
        # 然后通过class=el-table_1_column_10 is-center  is-hidden el-table__cell 定位到 编辑按钮触发
        edit_button = tr_element.find_element(By.CSS_SELECTOR, ".el-table_1_column_10.is-center.is-hidden.el-table__cell")
        # 获取元素里面的第一个a标签，那就是编辑按钮,第二个a标签是删除按钮
        editAbtn = edit_button.find_element(By.TAG_NAME, "a")
        editAbtn.click()
       
        #这时候就要弹出模态框了，进行编辑，把excel的对应数据填写到表单中即可。
        
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
        
        # 打印分割线
        print("==================================================================================================================")
        # 循环一次就结束
        break


