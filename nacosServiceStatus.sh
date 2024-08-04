#!/bin/zsh

# 定义函数，用于获取服务实例列表
getServiceInstances() {
  local serviceName="$1"
  local url="http://127.0.0.1:8848/nacos/v1/auth/login"

  # 调用 POST 接口获取 token
  local tokenResponse=$(curl -s -X POST \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=aw&password=aw" \
    "$url")

  # 解析 token
  local token=$(echo $tokenResponse | jq -r '.accessToken')

  # 检查 token 是否获取成功
  if [[ -z "$token" ]]; then
    echo "Error: Failed to retrieve token."
    return 1
  fi

  # 构造 GET 请求 URL
  local getUrl="http://127.0.0.1:8848/nacos/v2/ns/instance/list?serviceName=$serviceName&accessToken=$token&healthyOnly=true&ip=127.0.0.1&port=8088"

  # 发起 GET 请求
  curl -s -X GET "$getUrl"
}

# 使用函数
getServiceInstances "service-gateway"