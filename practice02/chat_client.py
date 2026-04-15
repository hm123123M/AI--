#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import json
import http.client
from datetime import datetime

# ================ 工具函数定义 ================

def list_files(directory):
    """列出目录下的文件及其属性"""
    try:
        files = []
        for entry in os.listdir(directory):
            full_path = os.path.join(directory, entry)
            if os.path.isfile(full_path):
                file_stat = os.stat(full_path)
                files.append({
                    "name": entry,
                    "type": "file",
                    "size": file_stat.st_size,
                    "size_human": format_size(file_stat.st_size),
                    "created_time": datetime.fromtimestamp(file_stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
                    "modified_time": datetime.fromtimestamp(file_stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
                })
            elif os.path.isdir(full_path):
                files.append({
                    "name": entry,
                    "type": "directory",
                    "size": "-",
                    "size_human": "-",
                    "created_time": "-",
                    "modified_time": "-"
                })
        return json.dumps({"success": True, "data": files}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def rename_file(directory, old_name, new_name):
    """重命名文件"""
    try:
        old_path = os.path.join(directory, old_name)
        new_path = os.path.join(directory, new_name)
        if os.path.exists(old_path):
            os.rename(old_path, new_path)
            return json.dumps({"success": True, "message": f"文件已重命名: {old_name} -> {new_name}"}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "文件不存在"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def delete_file(directory, filename):
    """删除文件"""
    try:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            return json.dumps({"success": True, "message": f"文件已删除: {filename}"}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "文件不存在"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def create_file(directory, filename, content):
    """创建文件并写入内容"""
    try:
        file_path = os.path.join(directory, filename)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return json.dumps({"success": True, "message": f"文件已创建: {filename}"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def read_file(directory, filename):
    """读取文件内容"""
    try:
        file_path = os.path.join(directory, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return json.dumps({"success": True, "content": content}, ensure_ascii=False)
        else:
            return json.dumps({"success": False, "error": "文件不存在"}, ensure_ascii=False)
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def format_size(size_bytes):
    """格式化文件大小"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024
        i += 1
    return f"{size_bytes:.2f} {size_names[i]}"

def curl_request(url, method="GET", headers=None, body=None):
    """通过HTTP请求访问网页并返回内容"""
    try:
        # 解析URL
        if url.startswith('https://'):
            protocol = 'https'
            url = url[8:]
        elif url.startswith('http://'):
            protocol = 'http'
            url = url[7:]
        else:
            protocol = 'http'
        
        # 分离路径和主机
        if '/' in url:
            host = url.split('/')[0]
            path = '/' + '/'.join(url.split('/')[1:])
        else:
            host = url
            path = '/'
        
        # 分离端口
        port = 443 if protocol == 'https' else 80
        if ':' in host:
            host_parts = host.split(':')
            host = host_parts[0]
            port = int(host_parts[1])
        
        # 设置默认请求头
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
        
        # 建立连接
        if protocol == 'https':
            conn = http.client.HTTPSConnection(host, port, timeout=30)
        else:
            conn = http.client.HTTPConnection(host, port, timeout=30)
        
        # 发送请求
        conn.request(method, path, body, headers)
        
        # 获取响应
        response = conn.getresponse()
        status_code = response.status
        response_headers = dict(response.getheaders())
        content = response.read().decode('utf-8', errors='ignore')
        
        conn.close()
        
        return json.dumps({
            "success": True,
            "status_code": status_code,
            "headers": response_headers,
            "content": content[:5000]  # 限制返回内容长度
        }, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def get_datetime():
    """获取当前日期和时间"""
    try:
        now = datetime.now()
        weekday_map = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
        
        result = {
            "success": True,
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "weekday": weekday_map[now.weekday()],
            "weekday_number": now.weekday() + 1
        }
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

def get_weather(city, day=0):
    """获取指定城市的天气预报（使用wttr.in简洁格式）"""
    try:
        # day参数：0=今天，1=明天，2=后天
        import urllib.parse
        
        # 编码城市名称
        encoded_city = urllib.parse.quote(city)
        
        # 使用wttr.in的简洁格式API
        url = f"http://wttr.in/{encoded_city}?format=j1"
        
        # 解析URL
        protocol = 'http'
        host = 'wttr.in'
        path = f"/{encoded_city}?format=j1"
        
        conn = http.client.HTTPConnection(host, 80, timeout=30)
        conn.request('GET', path)
        
        response = conn.getresponse()
        status_code = response.status
        
        if status_code != 200:
            conn.close()
            return json.dumps({"success": False, "error": f"请求失败，状态码: {status_code}"}, ensure_ascii=False)
        
        content = response.read().decode('utf-8', errors='ignore')
        conn.close()
        
        # 解析JSON响应
        weather_data = json.loads(content)
        
        # 提取需要的数据
        result = {
            "success": True,
            "city": city,
            "forecasts": []
        }
        
        # 获取未来几天的预报
        if 'weather' in weather_data and len(weather_data['weather']) > day:
            forecast = weather_data['weather'][day]
            
            result["forecasts"].append({
                "date": forecast.get('date', ''),
                "day_of_week": forecast.get('day_of_week', ''),
                "maxtempC": forecast.get('maxtempC', ''),
                "mintempC": forecast.get('mintempC', ''),
                "maxtempF": forecast.get('maxtempF', ''),
                "mintempF": forecast.get('mintempF', ''),
                "weather_desc": forecast.get('hourly', [{}])[0].get('weatherDesc', [{}])[0].get('value', ''),
                "wind_speed": forecast.get('hourly', [{}])[0].get('windspeedKmph', '') + " km/h",
                "humidity": forecast.get('hourly', [{}])[0].get('humidity', '') + "%"
            })
        
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

# ================ 工具映射 ================
TOOL_MAP = {
    "list_files": list_files,
    "rename_file": rename_file,
    "delete_file": delete_file,
    "create_file": create_file,
    "read_file": read_file,
    "curl_request": curl_request,
    "get_datetime": get_datetime,
    "get_weather": get_weather
}

# ================ 系统提示词 ================
def get_system_prompt():
    """生成包含当前日期时间的系统提示词"""
    now = datetime.now()
    weekday_map = {0: '星期一', 1: '星期二', 2: '星期三', 3: '星期四', 4: '星期五', 5: '星期六', 6: '星期日'}
    current_date = now.strftime("%Y-%m-%d")
    current_time = now.strftime("%H:%M:%S")
    current_weekday = weekday_map[now.weekday()]
    
    # 使用字符串拼接避免f-string中花括号转义问题
    prompt = """【当前时间信息】
- 当前日期：{date}
- 当前时间：{time}
- 星期：{weekday}

你是一个具备文件操作、网络访问和时间查询能力的AI助手。你可以使用以下工具来帮助用户完成任务：

可用工具列表：

1. **list_files** - 列出目录下的文件
   - 描述：列出指定目录下的所有文件和文件夹，包含文件大小、创建时间、修改时间等信息
   - 参数：
     - directory: string, 要列出的目录路径
   - 使用示例：{{"tool_name": "list_files", "args": {{"directory": "/path/to/directory"}}}}

2. **rename_file** - 重命名文件
   - 描述：将指定目录下的文件重命名
   - 参数：
     - directory: string, 文件所在目录路径
     - old_name: string, 原文件名
     - new_name: string, 新文件名
   - 使用示例：{{"tool_name": "rename_file", "args": {{"directory": "/path/to/directory", "old_name": "old.txt", "new_name": "new.txt"}}}}

3. **delete_file** - 删除文件
   - 描述：删除指定目录下的文件
   - 参数：
     - directory: string, 文件所在目录路径
     - filename: string, 要删除的文件名
   - 使用示例：{{"tool_name": "delete_file", "args": {{"directory": "/path/to/directory", "filename": "file.txt"}}}}

4. **create_file** - 创建文件
   - 描述：在指定目录下创建新文件并写入内容
   - 参数：
     - directory: string, 要创建文件的目录路径
     - filename: string, 新文件名
     - content: string, 文件内容
   - 使用示例：{{"tool_name": "create_file", "args": {{"directory": "/path/to/directory", "filename": "new.txt", "content": "Hello World!"}}}}

5. **read_file** - 读取文件
   - 描述：读取指定目录下文件的内容
   - 参数：
     - directory: string, 文件所在目录路径
     - filename: string, 要读取的文件名
   - 使用示例：{{"tool_name": "read_file", "args": {{"directory": "/path/to/directory", "filename": "file.txt"}}}}

6. **curl_request** - 访问网页
   - 描述：通过HTTP请求访问指定URL并返回网页内容
   - 参数：
     - url: string, 要访问的网页URL（支持http和https）
     - method: string, 可选，HTTP方法，默认GET
     - headers: object, 可选，HTTP请求头
     - body: string, 可选，HTTP请求体（POST请求时使用）
   - 使用示例：{{"tool_name": "curl_request", "args": {{"url": "https://example.com"}}}}

7. **get_datetime** - 获取当前日期时间
   - 描述：获取当前系统日期和时间，包含年月日时分秒和星期几
   - 参数：无
   - 使用示例：{{"tool_name": "get_datetime", "args": {{}}}}

8. **get_weather** - 获取天气预报
   - 描述：获取指定城市的天气预报，包括最高气温、最低气温、天气状况等
   - 参数：
     - city: string, 城市名称（如：北京、上海、青城山）
     - day: int, 可选，0=今天，1=明天，2=后天，默认为0
   - 使用示例：{{"tool_name": "get_weather", "args": {{"city": "青城山", "day": 1}}}}

使用工具的格式要求：
- 当你需要调用工具时，请使用JSON格式输出，格式如下：
  <function_calls>[{{"name": "工具名称", "parameters": {{"参数名": "参数值"}}}}]</function_calls>
- 请确保JSON格式正确，参数完整
- 如果不需要调用工具，可以直接回答用户问题
- 如果已经收到工具执行结果，请基于结果进行总结回答

注意事项：
- 请确认文件路径正确
- 删除文件前请确认用户意图
- 创建文件时请确保内容符合用户要求
""".format(date=current_date, time=current_time, weekday=current_weekday)
    
    return prompt

# ================ 加载.env文件 ================
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

# ================ 解析URL ================
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

# ================ 发送请求 ================
def send_request(protocol, host, port, path, api_key, messages, temperature=0.7, max_tokens=4096, stream=True):
    request_data = {
        "model": os.getenv('MODEL', 'qwen/qwen3.5-4b'),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "stream": stream
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
            return None, None, None
        
        return response, conn, response.status
        
    except Exception as e:
        print(f"请求错误: {str(e)}")
        return None, None, None

# ================ 处理流式响应 ================
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

# ================ 处理非流式响应 ================
def process_response(response, conn):
    try:
        response_data = response.read().decode('utf-8')
        conn.close()
        return json.loads(response_data)
    except Exception as e:
        print(f"响应解析错误: {str(e)}")
        if conn:
            conn.close()
        return None

# ================ 解析工具调用 ================
def parse_tool_call(content):
    """解析LLM响应中的工具调用"""
    try:
        # 查找<function_calls>标签
        start_tag = "<function_calls>"
        end_tag = "</function_calls>"
        
        if start_tag in content and end_tag in content:
            start_idx = content.find(start_tag) + len(start_tag)
            end_idx = content.find(end_tag)
            json_str = content[start_idx:end_idx].strip()
            
            try:
                tool_calls = json.loads(json_str)
                if isinstance(tool_calls, list) and len(tool_calls) > 0:
                    return tool_calls
            except json.JSONDecodeError:
                pass
        
        # 如果没有标签，尝试直接解析JSON
        try:
            tool_calls = json.loads(content.strip())
            if isinstance(tool_calls, list) and len(tool_calls) > 0:
                return tool_calls
        except json.JSONDecodeError:
            pass
        
        return None
    except Exception as e:
        print(f"解析工具调用错误: {str(e)}")
        return None

# ================ 执行工具调用 ================
def execute_tool_call(tool_call):
    """执行工具调用"""
    try:
        tool_name = tool_call.get('name')
        parameters = tool_call.get('parameters', {})
        
        if tool_name not in TOOL_MAP:
            return json.dumps({"success": False, "error": f"未知工具: {tool_name}"}, ensure_ascii=False)
        
        tool_func = TOOL_MAP[tool_name]
        
        # 根据工具名称传递参数
        if tool_name == "list_files":
            return tool_func(parameters.get("directory", "."))
        elif tool_name == "rename_file":
            return tool_func(parameters.get("directory", "."), 
                           parameters.get("old_name", ""), 
                           parameters.get("new_name", ""))
        elif tool_name == "delete_file":
            return tool_func(parameters.get("directory", "."), 
                           parameters.get("filename", ""))
        elif tool_name == "create_file":
            return tool_func(parameters.get("directory", "."), 
                           parameters.get("filename", ""), 
                           parameters.get("content", ""))
        elif tool_name == "read_file":
            return tool_func(parameters.get("directory", "."), 
                           parameters.get("filename", ""))
        elif tool_name == "curl_request":
            return tool_func(parameters.get("url", ""),
                           parameters.get("method", "GET"),
                           parameters.get("headers", None),
                           parameters.get("body", None))
        elif tool_name == "get_datetime":
            return tool_func()
        elif tool_name == "get_weather":
            return tool_func(parameters.get("city", ""),
                           parameters.get("day", 0))
        
        return json.dumps({"success": False, "error": f"工具调用失败: {tool_name}"}, ensure_ascii=False)
    
    except Exception as e:
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

# ================ 主函数 ================
def main():
    print("=== AI智能体工具调用客户端 ===")
    print("欢迎使用具备文件操作能力的AI助手！")
    print("支持的功能：列出文件、重命名文件、删除文件、创建文件、读取文件")
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
    
    # 初始化历史记录（包含系统提示词和当前时间信息）
    history = [{"role": "system", "content": get_system_prompt()}]
    
    print(f"已连接到: {protocol}://{host}:{port}")
    print(f"使用模型: {MODEL}\n")
    
    try:
        while True:
            # 获取用户输入
            try:
                print("你: ", end='', flush=True)
                user_input = input()
            except KeyboardInterrupt:
                print("\n\n感谢使用AI助手！")
                break
            
            if not user_input.strip():
                print("请输入有效消息")
                continue
            
            # 添加用户消息到历史
            history.append({"role": "user", "content": user_input})
            
            # 限制历史记录长度
            if len(history) > 20:
                history = [history[0]] + history[-19:]
            
            # 记录开始时间
            start_time = time.time()
            
            print(f"AI: ", end='', flush=True)
            
            # 发送请求（非流式，用于解析工具调用）
            response, conn, status = send_request(protocol, host, port, path, API_KEY, 
                                                  history, TEMPERATURE, MAX_TOKENS, stream=False)
            
            if response is None:
                print("请求失败，请检查配置和网络连接")
                history.pop()
                continue
            
            # 处理响应
            response_data = process_response(response, conn)
            
            if response_data is None:
                print("响应解析失败")
                history.pop()
                continue
            
            # 提取响应内容
            ai_response = ""
            if 'choices' in response_data and len(response_data['choices']) > 0:
                choice = response_data['choices'][0]
                if 'message' in choice and 'content' in choice['message']:
                    ai_response = choice['message']['content']
            
            # 记录结束时间
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            # 检查是否包含工具调用
            tool_calls = parse_tool_call(ai_response)
            
            if tool_calls:
                print(f"\n检测到工具调用: {json.dumps(tool_calls, ensure_ascii=False)}")
                
                # 执行工具调用
                tool_results = []
                for tool_call in tool_calls:
                    result = execute_tool_call(tool_call)
                    tool_results.append({
                        "tool_name": tool_call.get('name'),
                        "result": result
                    })
                
                # 将工具执行结果添加到历史
                result_content = f"工具执行结果:\n{json.dumps(tool_results, ensure_ascii=False, indent=2)}"
                history.append({"role": "assistant", "content": ai_response})
                history.append({"role": "user", "content": result_content})
                
                # 再次调用LLM进行总结
                print("\n正在总结...\nAI: ", end='', flush=True)
                
                response2, conn2, status2 = send_request(protocol, host, port, path, API_KEY, 
                                                         history, TEMPERATURE, MAX_TOKENS, stream=True)
                
                if response2:
                    final_response = process_stream(response2, conn2)
                    history.append({"role": "assistant", "content": final_response})
                else:
                    print("总结请求失败")
            
            else:
                # 直接输出响应
                print(ai_response)
                history.append({"role": "assistant", "content": ai_response})
            
            print(f"\n\n[耗时: {elapsed_time:.2f}秒]\n")
    
    except KeyboardInterrupt:
        print("\n\n感谢使用AI助手！")
    
    except Exception as e:
        print(f"\n发生错误: {str(e)}")

if __name__ == "__main__":
    main()
