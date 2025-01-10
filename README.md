Python 文件打包流程

# 首次使用
0.	虛擬環境
pip install pipenv
0.1 建立虚拟环境
pipenv install
0.2  !!!!安装pyinstaller模块用于打包(要用6.2.0否則错win32ctypes.pywin32.pywintypes.error: (225, '', '无法成功完成操作，因为文件包含病毒或潜在的垃圾软件。)
pip install pyinstaller==6.2.0


# 已安裝過的直接從這下面開始
a)	进入虚拟环境（上一步可省略,因为没有虚拟环境的话会自动建立一个）
pipenv shell 
b)	cd到指定文件位置
cd <yourPath>
c)	安装需要打包的代码块中使用到的所有的python模块
pip install pipreqs && pipreqs . && pip install -r requirements.txt
d)	使用pyinstaller命令直接开始打包
pyinstaller --onefile --clean to_pdf.py

# 激活新的虚拟环境
e)	退出当前虚拟环境（如果已激活）：
exit
f)	在你的项目目录中创建一个新的虚拟环境：这条命令会删除当前项目的虚拟环境（如果存在）。
pipenv --rm
g)	创建并激活新的虚拟环境：
pipenv shell
