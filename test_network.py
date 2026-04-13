# 测试网络连接
import http.client
import time

# 主函数
def main():
    print("=== 测试网络连接 ===")
    
    # 测试连接到本地LLM服务
    host = '127.0.0.1'
    port = 1234
    path = '/v1/chat/completions'
    
    print(f"尝试连接到: http://{host}:{port}{path}")
    
    start_time = time.time()
    
    try:
        # 创建连接
        conn = http.client.HTTPConnection(host, port, timeout=10)
        print("连接创建成功")
        
        # 构建请求数据
        request_data = {
            "model": "qwen/qwen3.5-4b",
            "messages": [
                {"role": "user", "content": "请介绍一下你自己"}
            ],
            "temperature": 1,
            "max_tokens": 4096
        }
        
        import json
        request_json = json.dumps(request_data)
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer sk-lm-cH81w7ac:xfAZOrS9dQKaTyY7qf1V'
        }
        
        # 发送请求
        print("发送请求...")
        conn.request('POST', path, request_json, headers)
        print("请求发送成功")
        
        # 获取响应
        print("等待响应...")
        response = conn.getresponse()
        print(f"响应状态码: {response.status}")
        
        # 读取响应数据
        response_data = response.read().decode('utf-8')
        print(f"响应数据: {response_data}")
        
        # 关闭连接
        conn.close()
        print("连接已关闭")
        
        end_time = time.time()
        print(f"耗时: {end_time - start_time:.2f}秒")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n测试完成")

if __name__ == "__main__":
    main()
