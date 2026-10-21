# 本地文件自动分类 Agent

基于大语言模型（LLM）与原生 API 从零手写实现的轻量级 Agent Harness。通过自然语言指令，自动读取本地目录、规划任务、创建对应文件夹并移动文件。

##  核心特性
* **手写 Harness 循环**：不依赖 LangChain 等重型框架，纯手写 `run` 循环与 `execute_tool` 路由，深入理解 Agent 底层原理。
* **Function Calling**：通过 JSON Schema 注册了 `list_files`、`create_directory`、`move_file` 工具。
* **自我纠错机制**：在工具执行层加入异常捕获，报错信息会自动返回给大模型，引导模型重新发起正确的调用。

##  技术栈
* Python 3.x
* OpenAI SDK (兼容 DashScope / 阿里通义千问)

##  快速开始
1. 安装依赖：`pip install openai`
2. 配置环境变量：`export DASHSCOPE_API_KEY="你的API_KEY"`
3. 运行测试：`python agent_task.py`

##  架构说明
用户输入 -> `run()` -> 发送给大模型 -> 模型返回 Tool Calls -> `execute_tool()` 路由分发 -> 执行 Python 函数 -> 结果返回给模型 -> 循环直到任务完成。
