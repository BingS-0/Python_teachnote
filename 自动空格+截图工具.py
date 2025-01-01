import pyautogui
import keyboard
import time
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("自动截图工具")
        self.is_running = False
        self.is_paused = False
        self.folder_name = None
        
        # 创建界面元素
        self.start_button = tk.Button(root, text="开始截图", command=self.start_capture)
        self.start_button.pack(pady=10)
        
        self.pause_button = tk.Button(root, text="暂停截图", command=self.pause_capture, state=tk.DISABLED)
        self.pause_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="停止截图", command=self.stop_capture, state=tk.DISABLED)
        self.stop_button.pack(pady=5)
        
        self.status_label = tk.Label(root, text="状态：就绪")
        self.status_label.pack(pady=5)

    def create_new_folder(self):
        # 创建以时间戳命名的新文件夹
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        folder_name = f"screenshots_{timestamp}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def start_capture(self):
        if self.is_paused:
            # 如果是从暂停状态恢复，使用原来的文件夹
            self.is_paused = False
            self.is_running = True
            self.status_label.config(text="状态：等待2秒后开始...")
        else:
            # 如果是新开始，创建新文件夹
            self.folder_name = self.create_new_folder()
            self.is_running = True
            self.status_label.config(text="状态：等待2秒后开始...")
        
        self.start_button.config(state=tk.DISABLED)
        self.pause_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        
        # 2秒后开始截图
        self.root.after(2000, self.start_delayed_capture)

    def pause_capture(self):
        self.is_paused = True
        self.is_running = False
        self.start_button.config(state=tk.NORMAL, text="继续截图")
        self.pause_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态：已暂停")

    def stop_capture(self):
        self.is_running = False
        self.is_paused = False
        self.start_button.config(state=tk.NORMAL, text="开始截图")
        self.pause_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="状态：已停止")

    def capture_screenshot(self):
        if not self.is_running:
            return

        # 获取屏幕中间区域
        screen_width, screen_height = pyautogui.size()
        left = screen_width // 4
        top = screen_height // 4
        width = screen_width // 2
        height = screen_height // 2

        try:
            # 截图并保存
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot = pyautogui.screenshot(region=(left, top, width, height))
            screenshot.save(os.path.join(self.folder_name, f"screenshot_{timestamp}.png"))
            
            # 模拟按下空格键
            keyboard.press_and_release('space')
            
            # 继续下一次截图
            self.root.after(1000, self.capture_screenshot)
        except Exception as e:
            messagebox.showerror("错误", f"截图过程中出现错误：{str(e)}")
            self.stop_capture()

    def start_delayed_capture(self):
        if self.is_running:  # 确保在2秒延迟期间没有被停止
            self.status_label.config(text="状态：正在截图")
            self.capture_screenshot()

def main():
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()