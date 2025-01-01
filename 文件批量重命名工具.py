import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

class FileRenamer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件批量重命名工具")
        self.window.geometry("400x350")
        
        # 創建界面元素
        self.create_widgets()
        
    def create_widgets(self):
        # 添加文件類型選擇
        self.file_type_var = tk.StringVar(value="image")
        tk.Label(self.window, text="請選擇要重命名的文件類型:").pack(pady=5)
        
        types_frame = tk.Frame(self.window)
        types_frame.pack(pady=5)
        
        tk.Radiobutton(types_frame, text="圖片文件", variable=self.file_type_var, 
                      value="image", command=self.update_prefix).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(types_frame, text="PDF文件", variable=self.file_type_var, 
                      value="pdf", command=self.update_prefix).pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(types_frame, text="文件夾", variable=self.file_type_var, 
                      value="folder", command=self.update_prefix).pack(side=tk.LEFT, padx=10)


        # 選擇文件夾按鈕
        self.folder_btn = tk.Button(self.window, text="選擇文件夾", command=self.select_folder)
        self.folder_btn.pack(pady=10)
        
        # 顯示所選文件夾路徑
        self.folder_label = tk.Label(self.window, text="未選擇文件夾", wraplength=350)
        self.folder_label.pack(pady=5)
        

        
        
        # 前綴輸入框
        tk.Label(self.window, text="請輸入文件名前綴:").pack(pady=5)
        self.prefix_entry = tk.Entry(self.window)
        self.prefix_entry.pack(pady=5)
        self.prefix_entry.insert(0, "image")
        
        # 起始編號輸入框
        tk.Label(self.window, text="請輸入起始編號:").pack(pady=5)
        self.start_num_entry = tk.Entry(self.window)
        self.start_num_entry.pack(pady=5)
        self.start_num_entry.insert(0, "1")
        
        # 重命名按鈕
        self.rename_btn = tk.Button(self.window, text="開始重命名", command=self.rename_files)
        self.rename_btn.pack(pady=20)
        
        # 狀態標籤
        self.status_label = tk.Label(self.window, text="")
        self.status_label.pack(pady=10)
        
    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.config(text=folder_path)
            
    def rename_files(self):
        if not hasattr(self, 'folder_path'):
            messagebox.showerror("錯誤", "請先選擇文件夾！")
            return
            
        prefix = self.prefix_entry.get()
        try:
            start_num = int(self.start_num_entry.get())
        except ValueError:
            messagebox.showerror("錯誤", "起始編號必須是數字！")
            return
            
        # 根據選擇的文件類型設置支持的格式
        file_type = self.file_type_var.get()
        if file_type == "image":
            supported_formats = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']
        elif file_type == "pdf":
            supported_formats = ['.pdf']
        else:  # folder
            supported_formats = None
            
        # 獲取要重命名的文件列表
        if file_type == "folder":
            files = [f for f in os.listdir(self.folder_path) 
                    if os.path.isdir(os.path.join(self.folder_path, f))]
        else:
            files = [f for f in os.listdir(self.folder_path) 
                    if os.path.isfile(os.path.join(self.folder_path, f)) and
                    os.path.splitext(f)[1].lower() in supported_formats]

        if not files:
            messagebox.showinfo("提示", "所選文件夾中沒有找到文件！")
            return
            
        # 按文件名排序
        files.sort()
        
        # 重命名文件
        renamed_count = 0
        for i, old_name in enumerate(files):
            # 獲取文件擴展名
            ext = os.path.splitext(old_name)[1]
            # 新文件名
            new_name = f"{prefix}_{start_num + i}{ext}"
            
            old_path = os.path.join(self.folder_path, old_name)
            new_path = os.path.join(self.folder_path, new_name)
            
            try:
                os.rename(old_path, new_path)
                renamed_count += 1
            except Exception as e:
                messagebox.showerror("錯誤", f"重命名 {old_name} 時發生錯誤：{str(e)}")
                
        self.status_label.config(text=f"成功重命名 {renamed_count} 個文件！")
        messagebox.showinfo("完成", f"成功重命名 {renamed_count} 個文件！")

    def update_prefix(self):
        file_type = self.file_type_var.get()
        prefix_map = {
            "image": "image",
            "pdf": "pdf",
            "folder": "file"
        }
        self.prefix_entry.delete(0, tk.END)
        self.prefix_entry.insert(0, prefix_map[file_type])

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = FileRenamer()
    app.run()