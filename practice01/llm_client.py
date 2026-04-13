import os
import time
import json
import http.client

# 加载.env文件
def load_dotenv(file_path):
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print(".env文件加载成功")
        except Exception as e:
            print(f".env文件加载错误: {str(e)}")
    else:
        print(".env文件不存在")

# 主函数
def main():
    print("=== AI智能体开发测试 ===")
    
    # 获取脚本和项目目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 确保project_dir指向AI课程目录
    project_dir = script_dir
    # 检查是否在practice01目录中
    if os.path.basename(project_dir) == 'practice01':
        project_dir = os.path.dirname(project_dir)
    env_path = os.path.join(project_dir, '.env')
    
    # 调试路径构建
    print(f"脚本目录: {script_dir}")
    print(f"项目目录: {project_dir}")
    print(f".env文件路径: {env_path}")
    print(f".env文件是否存在: {os.path.exists(env_path)}")
    
    # 加载.env文件
    print("\n1. 加载配置文件")
    load_dotenv(env_path)
    
    # 从环境变量获取配置
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:1234/v1')
    MODEL = os.getenv('MODEL', 'qwen/qwen3.5-4b')
    API_KEY = os.getenv('API_KEY', 'sk-lm-cH81w7ac:xfAZOrS9dQKaTyY7qf1V')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 1))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4096))
    
    print(f"BASE_URL: {BASE_URL}")
    print(f"MODEL: {MODEL}")
    print(f"API_KEY: {API_KEY[:10]}...")
    print(f"TEMPERATURE: {TEMPERATURE}")
    print(f"MAX_TOKENS: {MAX_TOKENS}")
    
    # 解析URL
    print("\n2. 解析连接参数")
    if BASE_URL.startswith('https://'):
        protocol = 'https'
        url = BASE_URL[8:]
    elif BASE_URL.startswith('http://'):
        protocol = 'http'
        url = BASE_URL[7:]
    else:
        protocol = 'http'
        url = BASE_URL
    
    # 提取主机和端口
    parts = url.split('/')[0].split(':')
    host = parts[0]
    port = int(parts[1]) if len(parts) > 1 else (443 if protocol == 'https' else 80)
    
    # 简化路径构建
    path = '/v1/chat/completions'
    
    print(f"协议: {protocol}")
    print(f"主机: {host}")
    print(f"端口: {port}")
    print(f"路径: {path}")
    print(f"完整URL: {protocol}://{host}:{port}{path}")
    
    # 示例请求
    prompt = "请简要介绍人工智能的发展历程"
    
    # 构建请求数据
    request_data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": "请简要介绍人工智能的发展历程"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    # 调试请求数据
    print(f"请求数据简化后: {request_data}")
    
    # 开始计时
    start_time = time.time()
    
    try:
        print("\n3. 发送请求到LLM服务")
        # 创建连接
        if protocol == 'https':
            conn = http.client.HTTPSConnection(host, port, timeout=60)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=60)
        
        # 设置请求头
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}'
        }
        
        # 发送请求
        request_json = json.dumps(request_data)
        print(f"请求数据: {request_json}")
        print(f"请求头: {headers}")
        print(f"发送请求到: {protocol}://{host}:{port}{path}")
        
        # 尝试发送请求
        try:
            conn.request('POST', path, request_json, headers)
            print("请求发送成功")
        except Exception as e:
            print(f"请求发送错误: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
        # 获取响应
        print("等待响应...")
        # 尝试获取响应，添加超时处理
        try:
            response = conn.getresponse()
            print(f"响应状态码: {response.status}")
            
            # 读取响应数据
            response_data = response.read().decode('utf-8')
            print(f"响应数据长度: {len(response_data)}")
            print(f"响应数据: {response_data}")
        except Exception as e:
            print(f"获取响应错误: {str(e)}")
            import traceback
            traceback.print_exc()
            raise
        
        # 结束计时
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        # 尝试解析JSON
        try:
            response_json = json.loads(response_data)
            print("\n4. 解析响应结果")
            
            # 提取token使用情况
            usage = response_json.get('usage', {})
            prompt_tokens = usage.get('prompt_tokens', 0)
            completion_tokens = usage.get('completion_tokens', 0)
            total_tokens = usage.get('total_tokens', 0)
            
            # 计算token速度
            token_speed = total_tokens / elapsed_time if elapsed_time > 0 else 0
            
            # 打印结果
            print("\n=== LLM调用结果 ===")
            print(f"请求内容: {prompt}")
            print(f"模型: {MODEL}")
            
            # 尝试提取响应内容
            if 'choices' in response_json and len(response_json['choices']) > 0:
                if 'message' in response_json['choices'][0]:
                    message = response_json['choices'][0]['message']
                    if 'content' in message and message['content']:
                        content = message['content']
                        print(f"响应内容: {content}")
                    elif 'reasoning_content' in message and message['reasoning_content']:
                        content = message['reasoning_content']
                        print(f"响应内容(推理): {content}")
                    else:
                        print("响应内容: 空")
                elif 'text' in response_json['choices'][0]:
                    content = response_json['choices'][0]['text']
                    print(f"响应内容: {content}")
                else:
                    print("响应内容: 无法提取")
            else:
                print("响应内容: 无法提取")
            
            # 打印统计信息
            print("\n=== 统计信息 ===")
            print(f"提示词tokens: {prompt_tokens}")
            print(f"完成tokens: {completion_tokens}")
            print(f"总tokens: {total_tokens}")
            print(f"耗时: {elapsed_time:.2f}秒")
            print(f"Token速度: {token_speed:.2f} tokens/秒")
            
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {str(e)}")
        
        # 关闭连接
        conn.close()
        print("\n连接已关闭")
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()
