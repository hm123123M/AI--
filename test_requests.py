# 使用requests库测试LLM服务
import requests
import json

# 主函数
def main():
    print("=== 使用requests库测试LLM服务 ===")
    
    # 配置
    url = "http://127.0.0.1:1234/v1/chat/completions"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer sk-lm-cH81w7ac:xfAZOrS9dQKaTyY7qf1V'
    }
    
    # 构建请求数据
    data = {
        "model": "qwen/qwen3.5-4b",
        "messages": [
            {"role": "user", "content": "Hello"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    print(f"请求URL: {url}")
    print(f"请求头: {headers}")
    print(f"请求数据: {data}")
    
    try:
        # 发送请求
        print("\n发送请求...")
        response = requests.post(url, json=data, headers=headers, timeout=60)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n测试完成")

if __name__ == "__main__":
    main()
