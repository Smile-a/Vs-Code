# import requests
# from requests.exceptions import RequestException, ConnectionError, Timeout, HTTPError

# def is_url_reachable(url):
#     try:
#         response = requests.get(url, timeout=60, verify=False)  # 发送GET请求，设置超时时间为5秒
#         response.raise_for_status()  # 如果响应的状态码不是200，则抛出HTTPError异常
#         return True  # 如果没有异常发生，则认为网址可达
#     except ConnectionError as conn_err:
#         print(f"连接错误: {conn_err}")
#     except Timeout as time_err:
#         print(f"请求超时: {time_err}")
#     except HTTPError as http_err:
#         print(f"HTTP错误: {http_err}")
#     except RequestException as req_err:
#         print(f"请求异常: {req_err}")
#     except Exception as err:
#         print(f"发生未知错误: {err}")
#     return False  # 如果发生任何异常，则认为网址不可达

# # 测试示例
# url = "https://10.157.234.151/index.php/Public/index/stra_name/sms_local"
# if is_url_reachable(url):
#     print(f"{url} 是可达的")
# else:
#     print(f"{url} 是不可达的")
    
    
    
    
    
    
#简单测试连接是否可用
import requests
def is_url_reachable(url):
    try:
        response = requests.get(url, timeout=60, verify=False)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False
    
# 示例使用
url = "https://10.157.234.151/index.php/Public/index/stra_name/sms_local"
print(is_url_reachable(url))  