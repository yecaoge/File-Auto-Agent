TOOLS = [
    {
    "type": "function",
    "function": {
        "name": "list_files",
        "description": "列出指定目录下的所有文件和文件夹名称",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "要查看的目录绝对路径，比如 C:/Users/E/Desktop"
                }
            },
            "required": ["directory"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "create_directory",
        "description": "创建文件夹，如Image、Docs、Code文件夹",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "要创建的文件夹绝对路径"
                }
            },
            "required": ["path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "move_file",
        "description": "移动文件到指定的文件夹",
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": "原来的路径"
                },
                "destination": {
                    "type": "string",
                    "description": "要移动到的文件夹绝对路径"
                }
            },
            "required": ["source",'destination']
        }
    }
}
]