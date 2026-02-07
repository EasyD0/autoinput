import pyautogui
import time
import sys
import os
from enum import Enum, auto
from tkinter import ttk, scrolledtext
from tkinter import filedialog
import tkinter as tk

class TypingMode(Enum):
    NORMAL = auto()
    IDE = auto()
    AICHAT = auto()

def simulate_typing_IDE(input_string: str, interval: float):
    lines = input_string.split('\n')
    processed_lines = []

    prev_indent = 0
    for line in lines:
        if line.strip() == "":
            processed_lines.append("")
            continue

        line.replace("\t", "    ")
        line_withoutindent = line.lstrip()
        cur_indent = len(line) - len(line_withoutindent)

        if cur_indent >= prev_indent:
            processed_lines.append(" "*(cur_indent-prev_indent) + line_withoutindent)
        else:
            processed_lines.append("\b" * (prev_indent-cur_indent) + line_withoutindent)

        prev_indent = cur_indent

    pyautogui.write("\n".join(processed_lines), interval=interval)


def simulate_typing_AICHAT(input_string: str, interval: float):
    lines = input_string.split('\n')

    for line in lines:
        processed_line = line.replace("\t", "    ")
        pyautogui.write(processed_line, interval=interval)
        pyautogui.hotkey('shift', 'enter')


def simulate_typing(input_string: str, mode: TypingMode = TypingMode.AICHAT, interval: float = 0.002):
    print("准备就绪，3秒后开始输入...")
    time.sleep(3)

    processed_lines = input_string.split('\n')
    
    match mode:
        case TypingMode.NORMAL:
            print("正在输入(普通模式)...")
            pyautogui.write('\n'.join(processed_lines), interval=interval)
        case TypingMode.IDE:
            print("正在输入(IDE模式)...")
            simulate_typing_IDE(input_string, interval)
        case TypingMode.AICHAT:
            print("正在输入(AI聊天模式)...")
            simulate_typing_AICHAT(input_string, interval)


def read_file(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        print(f"读取文件失败: {e}")
        return ""


def command_program():
    if len(sys.argv) > 1:
        path = " ".join(sys.argv[1:])
        simulate_typing(read_file(path))
    else:
        path = f"a.py"
        print(f"未检测到参数，使用默认文件路径:\n{path}")
        simulate_typing(read_file(path))

    print("输入完成。")


def is_valid_path(path: str) -> bool:
    if os.path.isfile(path):
        return True
    return False


class TypingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动输入工具")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        self.create_widgets()
        
    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="输入内容", padding="10")
        input_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        ttk.Label(input_frame, text="输入文件路径或直接输入文本:").pack(anchor="w")
        
        self.input_text = scrolledtext.ScrolledText(input_frame, height=8, wrap="word")
        self.input_text.pack(fill="both", expand=True, pady=5)
        
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill="x", pady=5)
        
        ttk.Button(btn_frame, text="选择文件", command=self.select_file).pack(side="left")
        ttk.Button(btn_frame, text="清除", command=self.clear_text).pack(side="left", padx=5)
        
        settings_frame = ttk.LabelFrame(self.root, text="设置", padding="10")
        settings_frame.pack(fill="x", padx=10, pady=5)
        
        mode_frame = ttk.Frame(settings_frame)
        mode_frame.pack(fill="x", pady=3)
        
        ttk.Label(mode_frame, text="模式:").pack(side="left", padx=(0, 10))
        
        self.mode_var = tk.StringVar(value="AICHAT")
        mode_combo = ttk.Combobox(
            mode_frame, 
            textvariable=self.mode_var,
            values=["NORMAL", "IDE", "AICHAT"],
            state="readonly",
            width=15
        )
        mode_combo.pack(side="left")
        
        ttk.Label(mode_frame, text="  (NORMAL:普通输入  IDE:代码输入  AICHAT:AI对话)").pack(side="left")
        
        interval_frame = ttk.Frame(settings_frame)
        interval_frame.pack(fill="x", pady=3)
        
        ttk.Label(interval_frame, text="字符间隔(秒):").pack(side="left", padx=(0, 10))
        
        self.interval_var = tk.DoubleVar(value=0.002)
        interval_spin = ttk.Spinbox(
            interval_frame,
            from_=0.0001,
            to=1.0,
            increment=0.0001,
            textvariable=self.interval_var,
            width=10
        )
        interval_spin.pack(side="left")
        
        delay_frame = ttk.Frame(settings_frame)
        delay_frame.pack(fill="x", pady=3)
        
        ttk.Label(delay_frame, text="启动延迟(秒):").pack(side="left", padx=(0, 10))
        
        self.delay_var = tk.IntVar(value=3)
        delay_spin = ttk.Spinbox(
            delay_frame,
            from_=0,
            to=60,
            increment=1,
            textvariable=self.delay_var,
            width=10
        )
        delay_spin.pack(side="left")
        
        self.start_btn = ttk.Button(self.root, text="开始执行", command=self.start_typing)
        self.start_btn.pack(pady=10, ipadx=30, ipady=5)
        
        log_frame = ttk.LabelFrame(self.root, text="日志", padding="10")
        log_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, wrap="word", state="disabled")
        self.log_text.pack(fill="both", expand=True)
        
    def select_file(self):
        filepath = filedialog.askopenfilename(
            title="选择文件",
            filetypes=[
                ("所有文件", "*.*"),
                ("文本文件", "*.txt"),
                ("Python文件", "*.py"),
                ("代码文件", "*.js *.ts *.html *.css *.json")
            ]
        )
        if filepath:
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", filepath)
            self.log(f"已选择文件: {filepath}")
            
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        
    def log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        
    def get_input_content(self) -> str:
        content = self.input_text.get("1.0", tk.END).strip()
        if not content:
            self.log("错误: 请输入内容或选择文件")
            return None
            
        if is_valid_path(content):
            file_content = read_file(content)
            if file_content:
                self.log(f"已读取文件内容 (路径: {content})")
                return file_content
            else:
                self.log("错误: 无法读取文件内容")
                return None
        else:
            self.log("使用直接输入的文本")
            return content
        
    def start_typing(self):
        input_content = self.get_input_content()
        if input_content is None:
            return
            
        mode_str = self.mode_var.get()
        try:
            mode = TypingMode[mode_str]
        except KeyError:
            self.log(f"错误: 无效的模式 {mode_str}")
            return
            
        interval = self.interval_var.get()
        delay = self.delay_var.get()
        
        self.log(f"开始执行 - 模式: {mode_str}, 间隔: {interval}秒, 延迟: {delay}秒")
        self.log(f"内容长度: {len(input_content)} 字符")
        self.start_btn.config(state="disabled")
        
        def run():
            try:
                time.sleep(delay)
                simulate_typing(input_content, mode, interval)
                self.log("输入完成!")
            except Exception as e:
                self.log(f"执行出错: {e}")
            finally:
                self.root.after(0, lambda: self.start_btn.config(state="normal"))
                
        import threading
        thread = threading.Thread(target=run, daemon=True)
        thread.start()


def gui_program():
    root = tk.Tk()
    app = TypingApp(root)
    root.mainloop()


if __name__ == "__main__":
    gui_program()