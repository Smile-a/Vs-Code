import xlrd

# 创建一个字典来存储数据
data_map = {}
# excel 文件路径
checkXmlPath = 'C:\MyProject\Vs-Code\dataModelAuto\数据模型补充分工表.xls'
# 打开excel文件
workbook = xlrd.open_workbook(checkXmlPath)
# 获取第一页的sheet页
sheet = workbook.sheet_by_index(0)
# 打印所有行信息
for row in range(sheet.nrows):
    if row == 0:
        continue
    # 获取每行的内容
    row_values = sheet.row_values(row)
    # 将第一列作为值，第二列作为key
    value = row_values[0]
    key = row_values[1]
    # 存储到字典中
    data_map[key] = value
    # 打印每行的内容 utf-8避免乱码
    #print(sheet.row_values(row)[1] + "\t" + sheet.row_values(row)[0])
    
# 示例：检查某个键是否存在
key_to_check = 'BAS_BOM'
if key_to_check in data_map:
    print(f"{key_to_check} 存在于字典中，对应的值为：{data_map[key_to_check]}")
else:
    print(f"{key_to_check} 不存在于字典中")

# 示例：获取某个键的值
value_for_key = data_map.get(key_to_check, "键不存在")
print(f"{key_to_check} 的值为：{value_for_key}")