import pandas as pd  
import uuid  
  
# 读取Excel文件  
df = pd.read_excel('C:\\Users\\wsd\\Desktop\\组织.xlsx', engine='openpyxl')  
  
# 假设你想要为'your_column'字段生成UUID  
#
df['ID'] = df['ID'].apply(lambda x: str(uuid.uuid4()))  

# 将 'BIRTHDATE' 列转换为日期时间类型
#df['BIRTHDATE'] = pd.to_datetime(df['BIRTHDATE'], format='%Y%m%d')

# 指定所有列为字符串格式
df = df.astype(str)

# 查看结果  
print(df)  
  
# 如果你想把结果保存回Excel文件  
df.to_excel('C:\\Users\\wsd\\Desktop\\组织test.xlsx', index=False, engine='openpyxl')