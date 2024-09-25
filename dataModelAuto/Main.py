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


xlsPath = 'C:\MyProject\Vs-Code\dataModelAuto\云MES系统实体清单-0326.xls'
checkXmlPath = 'C:\MyProject\Vs-Code\dataModelAuto\数据模型补充分工表.xls'
dataMbUrl = 'https://szzt-sjzt.hbtobacco.cn/dmm/dam-imm-web/model/dataModel'

#用来存储成功修改了的数据模型
r = redis.Redis(host='localhost', port=6379, db=5) 

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
        # 如果sheetName 只有一个元素，说明缺少了中文名称 跳过
        if len(sheetName) < 2:
            print("Execl中sheet名缺少模型中文名称，跳过")
            #当有问题的模型，跳过不出来，但是需要把模板的code存到er里面，方便后面手动处理
            r.sadd('excelErrList', sheet.name)
            continue
        # 模型英文名称
        mxCode = sheetName[0]
        # 判断这个sheet页模型Code是否已经在redis中
        if r.sismember('successList', mxCode):
            print("模型"+mxCode+"已经存在，跳过")
            continue
        # 模型中文名称
        modelChineseName = sheetName[1]
        # 如果中文名称是空的，跳过
        if modelChineseName == "":
            print("Execl中sheet名缺少模型中文名称，跳过")
            #当有问题的模型，跳过不出来，但是需要把模板的code存到er里面，方便后面手动处理
            r.sadd('excelErrList', sheet.name)
            continue
        # 刷新页面
        #chrome.refresh()
        # 再次等待页面加载完毕
        #wait = WebDriverWait(chrome, 10)
        #拿到了数据模型表名和模型中文名称 直接操作浏览器搜索模型
        alertMesBox(wait) #弹窗
        input_fields = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//input[@placeholder='请输入内容']")))
        # 忘记了 循环的时候，之前的值没有干掉奥，手动清空
        input_fields[0].clear()
        input_fields[1].clear()
        alertMesBox(wait) #弹窗
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
            # if len(trRows) == 0:
            #     # 那就说明没有找到 mxCode的模型，切换用模型中文名称试一次
            #     backBtnClean.click() # 重置页面查询条件
            #     # 等两秒，重置后会默认查询一次所有数据
            #     sleep(2)
            #     input_fields[1].send_keys(modelChineseName) # 输入中文名称
            #     query_button.click()
            #     sleep(2)
            #     # 然后再看看有没有数据模板
            #     query_body = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".el-table__body")))
            #     query_element = query_body[3]
            #     queryBody_element = query_element.find_element(By.TAG_NAME, "tbody")
            #     queryTrRows = queryBody_element.find_elements(By.TAG_NAME, "tr")
            #     print("表格元素重新定位成功,共有%d行数据" % len(queryTrRows))
            #     if len(queryTrRows) > 0:
            #         trRows = queryTrRows
            #     else:
            #         print("没有找到表名为\t"+mxCode+"\t 模型中文名称为\t"+modelChineseName+"\t的数据，请检查数据模型名称是否正确！")
            #         # 跳过
            #         continue
        #在这里等待一下吧，有数据，但是页面没有加载出来导致的？
        sleep(2)
        # 按理就只有一条数据，因为就一个数据模板，所以默认取第一个吧
        #tr_element = trRows[0]
        tr_element = None
        
        #还是获取结果进行匹配吧，哪怕用code和name一起，它搜索结果还是多个
        headTable = table_body[2]
        # 打印headTable所有元素
        for tr in headTable.find_elements(By.TAG_NAME, "tr"):
            tds = tr.find_elements(By.TAG_NAME, "td")
            sjmxybmL = tds[3]
            if sjmxybmL.text == mxCode:
                print(sjmxybmL.text)
                # 记录一个下标
                tr_element_num = tds[1].text
                # 就是要编辑这一行 这样就能定位到code搜索结果返回多个数据里最符合的那行数据了
                tr_element = trRows[int(tr_element_num) - 1] #trRows里面是下标 num存的是序号，所以要减一
                break
        # 这里有一种情况，有模糊匹配的结果，但是T_P开头，匹配不到 那不还是NONe
        if tr_element == None:
            print(f"******没有完全匹配CODE的模板，跳过该项数据,模板code:{mxCode},模型名称:{modelChineseName}******")
            # 这种情况是通过code可以模糊匹配到数据，但是对应的数据表名有可能是T_P开头这种，就需要手动处理了
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
        edit_button.click()
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
        #print("一共有%d个输入框" % input_elements.__len__())
        # 输出所有输入框的name和value
        # for input_element in input_elements:
        #     print(input_element.get_attribute("name"), input_element.get_attribute("value"))
        #数据模型标准名称
        try:
            input_elements[2].clear()
            input_elements[2].send_keys(mxCode)
        except Exception as e:
            print("数据模板标准名称不可编辑~")
        
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
        for row in tqdm(range(sheet.nrows)):
            # 跳过 第一行
            if row == 0:
                continue
            # 暂停1秒
            sleep(1)
            row_values = sheet.row_values(row)
            print("当前处理第%d条数据,共%d条数据!" % (row,sheet.nrows))
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
            # 字段说明
            zdsm = row_values[6]
            # 代码类别
            dylb = row_values[7]
            
            # 这时候已经获取到了当前行里的所有元素，然后依次进行填充
            # 先获取当前模态窗里面 id="pane-column" 的元素 这里面会有手动添加按钮和数据列表
            tabpanel = edit_div.find_element(By.ID, "pane-column")
            
            # 获取tabpanel里面的button 一共有五个，获取第四个"手动添加"按钮
            sleep(1)
            try:
                add_button = tabpanel.find_elements(By.TAG_NAME, "button")[3]
                add_button.click()
            except Exception as e:
                print("重新调用手动添加")
                # 检测提醒    
                alertMesBox(wait)
                sleep(1)
                # 一般都是因为上一个手动编辑的页面框关闭失败导致的，再关闭一次
                sdxgzdCloseBtn = drawerAddForm.find_element(By.TAG_NAME, "i")
                sleep(1)
                #sdxgzdCloseBtn.click()
                # 使用 JavaScript 执行点击
                chrome.execute_script("arguments[0].click();", sdxgzdCloseBtn)
                #然后再次调用 手动新增 按钮
                add_button = tabpanel.find_elements(By.TAG_NAME, "button")[3]
                sleep(2)
                #这里也会弹窗接口超时
                # 检测提醒    
                alertMesBox(wait)
                # 一切正常 点击手动新增按钮
                add_button.click()
            
            #定位弹窗的class="el-drawer__wrapper" 有很多个
            sleep(2)
            drawers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'el-drawer__wrapper')))
            # 获取最后一个元素 也就是 手动添加的弹窗
            drawerAddForm = drawers[-1]
            
            # 开始输入值 获取所有input标签
            input_elements = drawerAddForm.find_elements(By.TAG_NAME, "input")
            # 一共是有11个
            print("一共有%d个input元素" % len(input_elements))
            
            # 检测提醒    
            alertMesBox(wait)
            
            # 开始给对应的输入框赋值 第一个输入框是 源字段名
            input_elements[0].send_keys(zdm)
            # 第二个输入框是 字段中文名
            if zdsm == "":
                zdsm = zdm
                if "DOMAINCOL" == zdm:
                    zdsm = "域"
            input_elements[1].send_keys(zdsm)
            # 第四个输入框是 字段类型 比如是varchar int date datetime decimal 全部改成首字母大写
            zdlx = zdlx.capitalize()
            # 重新拼接zdlx 带中文组装
            if zdlx == "Decimal":
                zdlx = "高精小数(Decimal)"
            elif zdlx == "Date":
                zdlx = "时间(Time)"
            elif zdlx == "Decimal":
                zdlx = "高精小数(Decimal)"
            elif zdlx == "Int" or zdlx == "Tinyint":
                zdlx = "整数(Integer)"
            elif zdlx == "Varchar":
                zdlx = "变长字符(Varchar)"
            # 不太对，字段类型 input是一个下拉框，直接输入值好像不能成功，要如何操作?
            input_elements[3].send_keys(zdlx)
            # 直接这样是不行的，鼠标移动就丢失值，需要 键盘下然后加上回车 就可以了
            input_elements[3].send_keys(Keys.DOWN, Keys.ENTER)
            # 第五个输入框是 字段长度
            if zdcd != 'null':
                input_elements[4].send_keys(zdcd)
            # 第六个输入框是 小数位 如果zdlx是decimal 才需要设置
            if zdlx == "高精小数(Decimal)":
                # 字段长度一般只有在字段类型是varchar的时候才有用  数字类型一般就是null，那么就改获取数字长度
                input_elements[4].send_keys(szcd)
                # xsws 并且不能=0
                if int(xsws) != 0:
                    input_elements[5].send_keys(xsws)
            elif zdlx == "整数(Integer)":
                input_elements[4].send_keys(szcd)
            # 第九个是 能否为NULL 默认是不限制非空的 
            if nfwn == "NO":
                # excel中为NO 表示不允许为空，单击非空约束控件即可 启用
                fkysInput = input_elements[8]
                sleep(1)
                print(fkysInput.is_enabled())
                # 使用 JavaScript 执行点击
                chrome.execute_script("arguments[0].click();", fkysInput)
            
            #获取里面 class="drawerBtn" 元素里面的 button  这是保存按钮
            drawerBtnDiv = drawerAddForm.find_element(By.CLASS_NAME, "drawerBtn")
            saveBtn = drawerBtnDiv.find_element(By.TAG_NAME, "button")
            saveBtn.click()
            
            # 检测页面是否有弹出提示 role="alert" 的元素
            try:
                alert_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='alert']")))
                # 提示框里面的p标签 class=el-message__content 的text
                alert_P = alert_element.find_element(By.CLASS_NAME, "el-message__content")
                alert_text = alert_P.text
                #判断不为空的话 就打印出来
                if alert_text != "":
                    print(alert_text)
                    #print("源字段名已存在，跳过该字段!!!")
                    chrome.execute_script("arguments[0].click();", sdxgzdCloseBtn)
                    continue
            except Exception as e:
                print("没有捕获到顶部弹窗~")
                # 判断当前关闭按钮还是不是存在 get_attribute 是否none 状态
                if sdxgzdCloseBtn.aria_role != 'none':
                    chrome.execute_script("arguments[0].click();", sdxgzdCloseBtn)
        
        # 数据模型的字段都修改好了 可以直接点击暂存按钮了
        try:
            zcSave_button.click()
        except Exception as e:
            print("获取调用暂存按钮失败,重新调用")
            # 一般都是因为上一个手动编辑的页面框关闭失败导致的，再关闭一次
            sdxgzdCloseBtn = drawerAddForm.find_element(By.TAG_NAME, "i")
            sleep(1)
            sdxgzdCloseBtn.click()
            #然后再次调用 暂存 按钮
            zcSave_button.click()
        print("数据模型修改完毕，暂存成功！！！")
        #之后就可以关闭弹窗了，定位 aria-label="close 数据模型管理" 的button 按钮 点击执行关闭数据模型修改模态框
        close_button = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='close 数据模型管理']")))
        sleep(2)
        close_button.click()
        
        # 这一个sheet页的数据就都处理完毕了，把sheet页的code存储到redis的successList里面，下次循环就可以跳过这个sheet页了
        r.sadd("successList", mxCode)
        # 打印分割线
        print("==================================================================================================================")


# 主函数
if(__name__=="__main__"):
    # 启动次数
    num = 1
    # 最大重试次数
    max_attempts = 1000
    # 循环执行
    while True:
        if num < max_attempts:
            try:
                print(f"自动流程启动第{num}次")
                automationBegins()
                print("所有任务正常走完了？  程序结束!")
                break
            except Exception as e:
                print("自动化发生了异常，准备重新启动~")
            finally:
                num += 1
        else:
            print("达到最大启动次数，停止尝试。")
            break
