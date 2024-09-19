import os
import xlrd

from time import sleep,time
from selenium import webdriver
from selenium.webdriver.common.by import By
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
    # sjmxwh = chrome.find_element(By.XPATH, '//*[@id="menu_scrollbar"]/li[4]/a')
    print("选中左侧菜单 数据模型管理")
    # 获取id 为 menu_scrollbar 的元素
    sjmxwh = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="menu_scrollbar"]')))
    sjmxwh.click()
    
    # 获取子菜单项
    # sub_elements = sjmxwh.find_elements(By.XPATH, './*')
    # # 打印子元素信息
    # for sub_element in sub_elements:
    #     print(f"Tag name: {sub_element.tag_name}")
    #     print(f"Text: {sub_element.text}")
    #     print(f"Attributes: {sub_element.get_attribute('outerHTML')}\n")

    # 直接获取【数据模型维护】的a标签 直接触发效果
    submenu_item = wait.until(EC.presence_of_element_located((By.XPATH, '//a[@href="https://szzt-sjzt.hbtobacco.cn/dmm/dam-imm-web/model/dataModel"]')))
    # 点击子菜单项
    submenu_item.click()
    # 等待页面加载完成
    wait.until(EC.title_contains('数据模型维护'))
    print("成功进入数据模型维护页面")

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


