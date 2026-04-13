# AI智能体开发教学项目

这是一个基于Python的AI智能体开发教学项目，旨在帮助学习者掌握AI智能体开发的核心概念和实践技能。

## 项目结构

```
AI课程/
├── venv/                    # Python虚拟环境
├── practice01/              # 实践练习目录
│   └── llm_client.py        # LLM客户端测试脚本
├── .env                     # 环境变量配置文件
├── .env.example             # 环境变量配置模板
├── .gitignore               # Git忽略文件配置
├── requirements.txt         # 项目依赖列表
└── README.md               # 项目说明文档
```

## 文件功能说明

### 1. practice01/llm_client.py

**功能用途：**
- 读取项目根目录的.env文件内容
- 使用Python标准http.client库访问用户定义的LLM服务
- 统计token消耗、请求时间和token速度
- 解析和展示LLM响应结果

**教学目标：**
- 学习如何读取和解析.env环境配置文件
- 掌握Python标准库http.client的使用方法
- 理解OpenAI兼容协议的LLM API调用方式
- 学习如何统计API调用的性能指标（token消耗、时间、速度）
- 掌握JSON数据的序列化和反序列化
- 学习错误处理和调试技巧

## 环境配置

### 1. 安装依赖

```bash
# 使用虚拟环境中的pip安装依赖
venv\Scripts\pip.exe install -r requirements.txt
```

### 2. 配置环境变量

复制 `.env.example` 文件为 `.env`，并填写正确的LLM配置参数：

```env
# API基础URL
BASE_URL=http://127.0.0.1:1234/v1

# 模型名称
MODEL=qwen/qwen3.5-4b

# API密钥
API_KEY=your_api_key_here

# 温度参数（可选）
TEMPERATURE=1

# 最大生成长度（可选）
MAX_TOKENS=4096
```

### 3. 运行测试

```bash
# 运行LLM客户端测试
python practice01/llm_client.py
```

## 教学内容

### 模块1：环境配置与管理

- 学习Python虚拟环境的创建和使用
- 理解环境变量的作用和配置方法
- 掌握.gitignore文件的配置规则

### 模块2：HTTP客户端编程

- 学习使用http.client库发送HTTP请求
- 理解HTTP请求的结构（请求头、请求体、响应）
- 掌握JSON数据格式的处理

### 模块3：LLM API调用

- 了解OpenAI兼容协议的API端点
- 学习构建正确的请求数据格式
- 理解Authorization认证机制

### 模块4：性能统计与分析

- 学习如何测量API调用时间
- 理解token消耗的统计方法
- 计算token生成速度

## 技术要点

1. **环境变量加载**：使用自定义函数读取.env文件，无需依赖第三方库
2. **URL解析**：支持HTTP/HTTPS协议，自动提取主机、端口和路径
3. **错误处理**：包含完整的异常捕获和错误信息输出
4. **响应解析**：支持多种响应格式（content字段、reasoning_content字段、text字段）
5. **性能统计**：精确统计token消耗、请求时间和token速度

## 学习建议

1. 首先运行 `python practice01/llm_client.py` 观察输出结果
2. 修改.env文件中的配置参数，观察不同参数对结果的影响
3. 修改请求提示词，观察LLM的响应变化
4. 尝试修改代码，添加更多的功能和统计指标

## 注意事项

1. 确保LLM服务正在运行，并且可以通过配置的BASE_URL访问
2. 确保API_KEY正确，否则会收到认证错误
3. 网络请求可能需要一定时间，请耐心等待响应
4. 如果遇到超时错误，请检查LLM服务是否正常运行

## 扩展练习

1. 添加更多的LLM参数配置（如top_p、frequency_penalty等）
2. 实现流式响应处理
3. 添加请求重试机制
4. 实现批量请求处理
5. 添加更详细的性能分析和可视化
