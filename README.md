# 自动输入工具 (AutoInput Tool)

一个功能强大的Python自动输入工具，可以将文本或文件内容自动输入到任何应用程序中，支持多种输入模式和自定义配置。

## 功能特点

- **多种输入模式**：
  - **普通模式**：直接输入文本内容
  - **IDE模式**：智能处理代码缩进，适合输入到集成开发环境
  - **AI聊天模式**：自动处理换行，适合输入到聊天应用

- **双界面支持**：
  - 图形用户界面(GUI)：简单易用，适合普通用户
  - 命令行界面(CLI)：适合高级用户和脚本集成

- **自定义配置**：
  - 可调整字符输入间隔
  - 可设置启动延迟时间

- **灵活的输入源**：
  - 直接输入文本
  - 从文件读取内容（支持所有文件类型）

## 安装与依赖

### 依赖库

- `pyautogui`：用于模拟键盘输入
- `tkinter`：用于构建GUI界面（Python标准库）

### 安装方法

1. 克隆或下载项目文件：
```bash
git clone <repository-url>
cd autoinput
```

2. 安装依赖：
```bash
pip install pyautogui
```

## 使用方法

### GUI界面（推荐）

1. 直接运行程序：
```bash
python autoInput.py
```

2. 在界面中进行以下操作：
   - 输入文本内容或选择文件路径
   - 选择输入模式（NORMAL/IDE/AICHAT）
   - 设置字符间隔和启动延迟
   - 点击"开始执行"按钮

### 命令行界面

1. 使用文件路径作为参数：
```bash
python autoInput.py <文件路径>
```

2. 示例：
```bash
python autoInput.py "c:\Users\ace\Documents\example.txt"
```

## 输入模式说明

### NORMAL（普通模式）
- 直接输入文本内容
- 保持原始换行格式

### IDE（代码输入模式）
- 智能处理代码缩进
- 使用退格键调整缩进层级
- 适合输入到VS Code、PyCharm等IDE

### AICHAT（AI对话模式）
- 使用Shift+Enter进行换行
- 适合输入到ChatGPT、Claude等AI聊天应用
