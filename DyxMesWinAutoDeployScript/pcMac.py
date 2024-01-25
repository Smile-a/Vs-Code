import uuid
from psutil import net_if_addrs
from flask import Flask

app = Flask(__name__)

@app.route('/get_local_mac',methods=['GET'])
def hello():
    return "My MAC address:" + get_local_mac()
 
# 获取本机MAC地址--单网卡
def get_local_mac():
    mac_address = ':'.join(hex(uuid.getnode())[2:].zfill(12)[i:i + 2] for i in range(0, 12, 2))
    print("MAC address:", mac_address)
    return mac_address
 
 
# 获取所有MAC地址
def get_all_mac():
    for k, v in net_if_addrs().items():
        print("k:",k)
        print("v:",v)
        for item in v:
            address = item[1]
            if '-' in address and len(address)==17:
                print(address)
 

if __name__=='__main__':
    #get_all_mac()
    app.run(host='0.0.0.0', port=5000, debug=True)