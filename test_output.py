# 测试脚本，将输出写入文件
import os
import time
import json
import http.client

# 主函数
def main():
    # 打开输出文件
    with open('test_output.txt', 'w', encoding='utf-8') as f:
        f.write("=== AI智能体开发测试 ===\n")
        
        # 获取脚本和项目目录
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(script_dir)
        env_path = os.path.join(project_dir, '.env')
        
        f.write(f"脚本目录: {script_dir}\n")
        f.write(f"项目目录: {project_dir}\n")
        f.write(f".env文件路径: {env_path}\n")
        
        # 加载.env文件
        f.write("\n1. 加载配置文件\n")
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r', encoding='utf-8') as env_file:
                    for line in env_file:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
                f.write(".env文件加载成功\n")
            except Exception as e:
                f.write(f".env文件加载错误: {str(e)}\n")
        else:
            f.write(".env文件不存在\n")
        
        # 从环境变量获取配置
        BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:1234/v1')
        MODEL = os.getenv('MODEL', 'qwen/qwen3.5-4b')
        API_KEY = os.getenv('API_KEY', 'sk-lm-cH81w7ac:xfAZOrS9dQKaTyY7qf1V')
        TEMPERATURE = float(os.getenv('TEMPERATURE', 1))
        MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4096))
        
        f.write(f"BASE_URL: {BASE_URL}\n")
        f.write(f"MODEL: {MODEL}\n")
        f.write(f"API_KEY: {API_KEY[:10]}...\n")
        f.write(f"TEMPERATURE: {TEMPERATURE}\n")
        f.write(f"MAX_TOKENS: {MAX_TOKENS}\n")
        
        # 解析URL
        f.write("\n2. 解析连接参数\n")
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
        
        f.write(f"协议: {protocol}\n")
        f.write(f"主机: {host}\n")
        f.write(f"端口: {port}\n")
        f.write(f"路径: {path}\n")
        f.write(f"完整URL: {protocol}://{host}:{port}{path}\n")
        
        # 构建请求数据
        request_data = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": "Hello"}
            ],
            "temperature": 0.7,
            "max_tokens": 50
        }
        
        f.write(f"请求数据: {request_data}\n")
        
        # 开始计时
        start_time = time.time()
        
        try:
            f.write("\n3. 发送请求到LLM服务\n")
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
            f.write(f"请求数据: {request_json}\n")
            f.write(f"请求头: {headers}\n")
            f.write(f"发送请求到: {protocol}://{host}:{port}{path}\n")
            
            # 尝试发送请求
            try:
                conn.request('POST', path, request_json, headers)
                f.write("请求发送成功\n")
            except Exception as e:
                f.write(f"请求发送错误: {str(e)}\n")
                import traceback
                traceback.print_exc(file=f)
                raise
            
            # 获取响应
            f.write("等待响应...\n")
            response = conn.getresponse()
            f.write(f"响应状态码: {response.status}\n")
            
            # 读取响应数据
            response_data = response.read().decode('utf-8')
            f.write(f"响应数据: {response_data}\n")
            
            # 结束计时
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # 尝试解析JSON
            try:
                response_json = json.loads(response_data)
                f.write("\n4. 解析响应结果\n")
                
                # 提取token使用情况
                usage = response_json.get('usage', {})
                prompt_tokens = usage.get('prompt_tokens', 0)
                completion_tokens = usage.get('completion_tokens', 0)
                total_tokens = usage.get('total_tokens', 0)
                
                # 计算token速度
                token_speed = total_tokens / elapsed_time if elapsed_time > 0 else 0
                
                # 打印结果
                f.write("\n=== LLM调用结果 ===\n")
                f.write(f"请求内容: Hello\n")
                f.write(f"模型: {MODEL}\n")
                
                # 尝试提取响应内容
                if 'choices' in response_json and len(response_json['choices']) > 0:
                    if 'message' in response_json['choices'][0] and 'content' in response_json['choices'][0]['message']:
                        content = response_json['choices'][0]['message']['content']
                        f.write(f"响应内容: {content}\n")
                    elif 'text' in response_json['choices'][0]:
                        content = response_json['choices'][0]['text']
                        f.write(f"响应内容: {content}\n")
                    else:
                        f.write("响应内容: 无法提取\n")
                else:
                    f.write("响应内容: 无法提取\n")
                
                # 打印统计信息
                f.write("\n=== 统计信息 ===\n")
                f.write(f"提示词tokens: {prompt_tokens}\n")
                f.write(f"完成tokens: {completion_tokens}\n")
                f.write(f"总tokens: {total_tokens}\n")
                f.write(f"耗时: {elapsed_time:.2f}秒\n")
                f.write(f"Token速度: {token_speed:.2f} tokens/秒\n")
                
            except json.JSONDecodeError as e:
                f.write(f"JSON解析错误: {str(e)}\n")
            
            # 关闭连接
            conn.close()
            f.write("\n连接已关闭\n")
            
        except Exception as e:
            f.write(f"错误: {str(e)}\n")
            import traceback
            traceback.print_exc(file=f)
        finally:
            f.write("\n=== 测试完成 ===\n")

if __name__ == "__main__":
    main()
