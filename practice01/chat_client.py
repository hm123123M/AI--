#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
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
            return True
        except Exception as e:
            print(f"加载.env文件错误: {str(e)}")
            return False
    else:
        print(".env文件不存在")
        return False

# 解析URL
def parse_url(base_url):
    if base_url.startswith('https://'):
        protocol = 'https'
        url = base_url[8:]
    elif base_url.startswith('http://'):
        protocol = 'http'
        url = base_url[7:]
    else:
        protocol = 'http'
        url = base_url
    
    parts = url.split('/')[0].split(':')
    host = parts[0]
    port = int(parts[1]) if len(parts) > 1 else (443 if protocol == 'https' else 80)
    
    path_parts = url.split('/')[1:]
    if path_parts:
        path = '/' + '/'.join(path_parts)
        if not path.endswith('/chat/completions'):
            if path.endswith('/'):
                path += 'chat/completions'
            else:
                path += '/chat/completions'
    else:
        path = '/v1/chat/completions'
    
    return protocol, host, port, path

# 发送请求并处理流式响应
def send_request(protocol, host, port, path, api_key, messages, temperature=0.7, max_tokens=4096):
    request_data = {
        "model": os.getenv('MODEL', 'qwen/qwen3.5-4b'),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": True
    }
    
    try:
        if protocol == 'https':
            conn = http.client.HTTPSConnection(host, port, timeout=120)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=120)
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
        
        request_json = json.dumps(request_data)
        conn.request('POST', path, request_json, headers)
        
        response = conn.getresponse()
        if response.status != 200:
            response_data = response.read().decode('utf-8')
            print(f"请求失败，状态码: {response.status}")
            print(f"错误信息: {response_data}")
            conn.close()
            return None, 0, 0
        
        return response, conn, response.status
        
    except Exception as e:
        print(f"请求错误: {str(e)}")
        return None, None, None

# 处理流式响应
def process_stream(response, conn):
    full_content = ""
    buffer = bytearray()
    
    try:
        while True:
            chunk = response.read(1024)
            if not chunk:
                break
            
            buffer.extend(chunk)
            
            while True:
                try:
                    buffer_str = buffer.decode('utf-8')
                except UnicodeDecodeError:
                    break
                
                if '\n\n' not in buffer_str:
                    break
                
                line_end = buffer_str.find('\n\n')
                line = buffer_str[:line_end].strip()
                buffer = buffer[(line_end + 2):]
                
                if not line:
                    continue
                
                if line.startswith('data: '):
                    data_str = line[6:]
                    if data_str == '[DONE]':
                        conn.close()
                        return full_content
                    
                    try:
                        data = json.loads(data_str)
                        
                        if 'choices' in data and len(data['choices']) > 0:
                            choice = data['choices'][0]
                            
                            if 'delta' in choice and 'content' in choice['delta']:
                                content = choice['delta']['content']
                                full_content += content
                                print(content, end='', flush=True)
                                
                            elif 'message' in choice and 'content' in choice['message']:
                                content = choice['message']['content']
                                full_content += content
                                print(content, end='', flush=True)
                                
                    except json.JSONDecodeError:
                        continue
        
        conn.close()
        return full_content
        
    except Exception as e:
        print(f"\n流式响应处理错误: {str(e)}")
        if conn:
            conn.close()
        return full_content

# 主函数
def main():
    print("=== AI智能体聊天客户端 ===")
    print("欢迎使用AI聊天客户端！")
    print("输入消息开始聊天，按Ctrl+C退出\n")
    
    # 获取项目目录并加载配置
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)
    env_path = os.path.join(project_dir, '.env')
    
    if not load_dotenv(env_path):
        print("无法加载配置文件，使用默认配置")
    
    # 获取配置
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:1234/v1')
    API_KEY = os.getenv('API_KEY', '')
    MODEL = os.getenv('MODEL', 'qwen/qwen3.5-4b')
    TEMPERATURE = float(os.getenv('TEMPERATURE', 0.7))
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', 4096))
    
    # 解析URL
    protocol, host, port, path = parse_url(BASE_URL)
    
    # 初始化历史记录
    history = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_time = 0
    
    print(f"已连接到: {protocol}://{host}:{port}")
    print(f"使用模型: {MODEL}\n")
    
    try:
        while True:
            # 获取用户输入
            try:
                print("你: ", end='', flush=True)
                user_input = input()
            except KeyboardInterrupt:
                print("\n\n感谢使用AI聊天客户端！")
                break
            
            if not user_input.strip():
                print("请输入有效消息")
                continue
            
            # 添加用户消息到历史
            history.append({"role": "user", "content": user_input})
            
            # 限制历史记录长度（最多保留10轮对话）
            if len(history) > 20:
                history = history[-20:]
            
            # 记录开始时间
            start_time = time.time()
            
            print(f"AI: ", end='', flush=True)
            
            # 发送请求
            response, conn, status = send_request(protocol, host, port, path, API_KEY, history, TEMPERATURE, MAX_TOKENS)
            
            if response is None:
                print("请求失败，请检查配置和网络连接")
                # 移除刚才添加的用户消息
                history.pop()
                continue
            
            # 处理流式响应
            ai_response = process_stream(response, conn)
            
            # 记录结束时间
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # 添加AI响应到历史
            history.append({"role": "assistant", "content": ai_response})
            
            # 简单统计（实际应用中应该从响应中获取准确的token数）
            prompt_tokens = len(user_input) // 4  # 粗略估算
            completion_tokens = len(ai_response) // 4  # 粗略估算
            
            total_prompt_tokens += prompt_tokens
            total_completion_tokens += completion_tokens
            total_time += elapsed_time
            
            print(f"\n\n[统计] 本次耗时: {elapsed_time:.2f}秒 | "
                  f"提示词: ~{prompt_tokens} tokens | "
                  f"响应: ~{completion_tokens} tokens")
            
            if total_time > 0:
                avg_speed = (total_prompt_tokens + total_completion_tokens) / total_time
                print(f"[总计] 提示词: ~{total_prompt_tokens} | "
                      f"响应: ~{total_completion_tokens} | "
                      f"平均速度: {avg_speed:.2f} tokens/秒\n")
    
    except KeyboardInterrupt:
        print("\n\n感谢使用AI聊天客户端！")
    
    except Exception as e:
        print(f"\n发生错误: {str(e)}")

if __name__ == "__main__":
    main()
