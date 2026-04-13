# 测试配置加载
import os

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
    print("=== 测试配置加载 ===")
    
    # 获取脚本和项目目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_path = os.path.join(script_dir, '.env')
    
    print(f"脚本目录: {script_dir}")
    print(f".env文件路径: {env_path}")
    
    # 加载.env文件
    load_dotenv(env_path)
    
    # 从环境变量获取配置
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:1234/v1')
    MODEL = os.getenv('MODEL', 'qwen/qwen3.5-4b')
    API_KEY = os.getenv('API_KEY', 'sk-lm-cH81w7ac:xfAZOrS9dQKaTyY7qf1V')
    
    print(f"BASE_URL: {BASE_URL}")
    print(f"MODEL: {MODEL}")
    print(f"API_KEY: {API_KEY[:10]}...")
    
    # 测试URL解析
    print("\n测试URL解析")
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
    
    # 构建路径
    path_parts = url.split('/')[1:]
    if path_parts:
        path = '/' + '/'.join(path_parts)
        # 确保路径以/chat/completions结尾
        if not path.endswith('/chat/completions'):
            if path.endswith('/'):
                path += 'chat/completions'
            else:
                path += '/chat/completions'
    else:
        path = '/v1/chat/completions'
    
    print(f"协议: {protocol}")
    print(f"主机: {host}")
    print(f"端口: {port}")
    print(f"路径: {path}")
    
    print("\n测试完成")

if __name__ == "__main__":
    main()
