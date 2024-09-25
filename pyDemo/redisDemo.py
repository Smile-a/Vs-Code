import redis

# 连接redis 设置存储的数据库为14 将从Redis服务器接收到的值默认为字符串类型
r = redis.Redis(host='localhost', port=6379, db=5 , decode_responses=True)

# 清空list数据
# r.delete('list')

# 设置list值，字符串类型
# r.rpush('list', '1')
# r.rpush('list', '2')

#获取list总条数
# print(r.llen('list'))

# 获取list值
# print(r.lrange('list', 0, -1))

#获取当前redis数据库所有的元素列表
#print(r.keys())
#把所有元素的key写入到successList集合中
# for i in r.keys():
#     r.sadd('successList', i)

# 删除集合中的所有元素，除了successList
# for i in r.keys():
#     if i != 'successList':
#         r.delete(i)

r.delete('excelErrList')
r.delete('webDataNullList')
r.delete('TpList')