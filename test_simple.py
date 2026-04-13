# 简单测试脚本
print("=== 简单测试开始 ===")

# 测试1: 基本打印
print("测试1: 基本打印")
print("Hello World")

# 测试2: 模块导入
print("\n测试2: 模块导入")
try:
    import os
    import time
    import json
    import http.client
    print("所有模块导入成功")
except Exception as e:
    print(f"模块导入错误: {str(e)}")

# 测试3: 环境变量
print("\n测试3: 环境变量")
try:
    os.environ['TEST'] = 'test value'
    print(f"环境变量设置成功: {os.environ.get('TEST')}")
except Exception as e:
    print(f"环境变量错误: {str(e)}")

# 测试4: 网络连接
print("\n测试4: 网络连接")
try:
    # 测试连接到百度
    conn = http.client.HTTPConnection('www.baidu.com', 80, timeout=5)
    print("连接创建成功")
    conn.request('GET', '/')
    print("请求发送成功")
    response = conn.getresponse()
    print(f"响应状态码: {response.status}")
    conn.close()
    print("连接关闭成功")
except Exception as e:
    print(f"网络连接错误: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n=== 简单测试完成 ===")
