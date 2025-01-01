import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from datetime import datetime

class ImageToPdfConverter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("文件夾批量轉PDF工具")
        self.window.geometry("400x300")
        
        # 保存選擇的主文件夾路徑
        self.main_folder = None
        
        self.create_widgets()
        
    def create_widgets(self):
        # 選擇文件夾按鈕
        self.folder_btn = tk.Button(self.window, text="選擇主文件夾", command=self.select_folder)
        self.folder_btn.pack(pady=10)
        
        # 顯示所選文件夾路徑
        self.folder_label = tk.Label(self.window, wraplength=350)
        self.folder_label.pack(pady=5)
        
        # 轉換按鈕
        self.convert_btn = tk.Button(self.window, text="轉換為PDF", command=self.convert_to_pdf)
        self.convert_btn.pack(pady=10)
        
        # 狀態標籤
        self.status_label = tk.Label(self.window, text="", wraplength=350)
        self.status_label.pack(pady=5)
        
    def select_folder(self):
        self.main_folder = filedialog.askdirectory()
        if self.main_folder:
            self.folder_label.config(text=f"已選擇: {self.main_folder}")
            
    def convert_folder_to_pdf(self, folder_path):
        images = []
        # 支持的圖片格式
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        
        # 獲取文件夾中的所有圖片
        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith(image_extensions):
                image_path = os.path.join(folder_path, filename)
                try:
                    image = Image.open(image_path)
                    # 如果圖片不是RGB模式，轉換為RGB
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    images.append(image)
                except Exception as e:
                    raise Exception(f"處理圖片 {filename} 時出錯：{str(e)}")
        
        if images:
            # 使用文件夾名稱和時間作為PDF文件名
            folder_name = os.path.basename(folder_path)
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            pdf_path = f"{folder_name}_{current_time}.pdf"
            
            # 保存PDF
            images[0].save(
                pdf_path,
                "PDF",
                resolution=100.0,
                save_all=True,
                append_images=images[1:]
            )
            return pdf_path
        return None
            
    def convert_to_pdf(self):
        if not self.main_folder:
            messagebox.showwarning("警告", "請先選擇主文件夾！")
            return
        
        # 獲取所有子文件夾
        subfolders = [f.path for f in os.scandir(self.main_folder) if f.is_dir()]
        
        if not subfolders:
            messagebox.showwarning("警告", "主文件夾中沒有找到子文件夾！")
            return
        
        converted_pdfs = []
        errors = []
        
        # 處理每個子文件夾
        for folder in subfolders:
            try:
                pdf_path = self.convert_folder_to_pdf(folder)
                if pdf_path:
                    converted_pdfs.append(pdf_path)
            except Exception as e:
                errors.append(f"處理文件夾 {os.path.basename(folder)} 時出錯：{str(e)}")
        
        # 顯示結果
        if converted_pdfs:
            success_message = f"成功創建 {len(converted_pdfs)} 個PDF文件：\n" + "\n".join(converted_pdfs)
            self.status_label.config(text=success_message)
            messagebox.showinfo("成功", success_message)
        
        if errors:
            error_message = "\n".join(errors)
            messagebox.showerror("錯誤", error_message)
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageToPdfConverter()
    app.run()
