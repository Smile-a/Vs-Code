import time
from tqdm import tqdm
 
# 假设你要迭代的是一个范围
for i in tqdm(range(100)):
    # 在这里执行你的任务
    time.sleep(0.5)
    pass
 
# 如果你正在使用列表
items = [1, 2, 3, 4, 5]
for item in tqdm(items):
    # 处理每个item
    time.sleep(1)
    pass