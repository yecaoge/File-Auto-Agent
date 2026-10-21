import json
import os
import shutil

from openai import OpenAI
from Tools import TOOLS

client = OpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.environ["DASHSCOPE_API_KEY"]
)
MODEL = "qwen-plus"
MAX_TURNS = 5

SYSTEM = """你是一个桌面整理文件助手。
你可以读取、创建文件夹和移动文件。
当你整理文件时，请遵循以下规则：
1. 图片文件（如 .jpg, .png）请移动到 Images 文件夹。
2. 文档文件（如 .txt, .docx）请移动到 Docs 文件夹。
3. 代码文件（如 .py, .js）请移动到 Code 文件夹。
4. 移动前，请确保目标文件夹存在，如果不存在，请调用 create_directory 创建它。
请一步一步思考，先查看文件，再创建对应的文件夹，最后移动文件。"""


def list_files(directory):
    try:
        items = os.listdir(directory)
        if not items:
            return "该目录为空。"
        return "目录内容：\n" + "\n".join(items)
    except Exception as e:
        return f"读取出错: {e}"


def create_directory(path):
    try:
        os.makedirs(path, exist_ok=True)
        return f"文件夹 {path} 已成功创建（或已存在）。"
    except Exception as e:
        return f"创建文件夹出错: {e}"


def move_file(source, destination):
    ALLOWED_DIR = os.path.abspath(test_dir)
    try:
        if not os.path.abspath(source).startswith(ALLOWED_DIR):
            return '安全拦截：越权操作，只能在指定目录操作！'
        shutil.move(source, destination)
        return f'文件已从{source}移动到{destination}'
    except Exception as e:
        return f"移动出错：{e}"


def execute_tool(name: str, args: dict) -> str:
    if name == 'list_files':
        return list_files(args['directory'])
    if name == 'create_directory':
        return create_directory(args['path'])
    if name == 'move_file':
        return move_file(args['source'], args['destination'])


def run(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": user_message}
    ]
    for turn in range(MAX_TURNS):
        print(f"\nAI 思考中 (第 {turn + 1} 轮)...")
        response = client.chat.completions.create(
            model=MODEL, messages=messages, tools=TOOLS)
        msg = response.choices[0].message
        messages.append(msg)
        if not msg.tool_calls:
            return msg.content

        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments)
            print(f"  🔧 决定调用: {tc.function.name} | 参数: {args}")

            result = execute_tool(tc.function.name, args)
            print(f"  ✅ 执行结果: {result}")
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result
            })
    return "达到最大轮次限制。"


if __name__ == "__main__":
    # 先准备一个测试文件夹和几个文件，方便 AI 去查
    test_dir = "C:/Users/E/Desktop/sandbox"
    # 给 AI 下达任务
    task = f"帮我看看 {test_dir} 里有什么文件，然后按照规则建好对应的文件夹，没有的文件不需要提前创建文件夹。将文件移动到对应的文件夹"
    # 启动 AI
    final_result = run(task)
    print("\n🎉 AI 最终回复:", final_result)
