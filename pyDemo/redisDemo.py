import redis

# 连接redis 设置存储的数据库为14 将从Redis服务器接收到的值默认为字符串类型
r = redis.Redis(host='localhost', port=6379, db=14 , decode_responses=True)

# 清空list数据
r.delete('list')

# 设置list值，字符串类型
r.rpush('list', '1')
r.rpush('list', '2')

#获取list总条数
print(r.llen('list'))

# 获取list值
print(r.lrange('list', 0, -1))