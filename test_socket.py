# 使用socket模块测试端口是否开放
import socket

# 主函数
def main():
    print("=== 使用socket模块测试端口是否开放 ===")
    
    # 配置
    host = '127.0.0.1'
    port = 1234
    
    print(f"测试端口: {host}:{port}")
    
    try:
        # 创建socket连接
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        
        # 尝试连接
        result = s.connect_ex((host, port))
        
        if result == 0:
            print("端口开放，服务正在运行")
        else:
            print(f"端口未开放，错误代码: {result}")
        
        # 关闭连接
        s.close()
        
    except Exception as e:
        print(f"错误: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n测试完成")

if __name__ == "__main__":
    main()
