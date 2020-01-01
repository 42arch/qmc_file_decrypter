import threading
import time
import tkinter as tk
from threading import Thread
from tkinter import *
from tkinter import filedialog, messagebox

from decrypt import qmc_file_decrypt


class HandleThread(Thread):
    def __init__(self, file_list_box, log_area, file_list, output_dir):
        super().__init__()
        self.file_list_box = file_list_box
        self.log_area = log_area
        self.file_list = file_list
        self.output_dir = output_dir

    def run(self):
        # for i in self.file_list:
        #     start_time = time.time()
        #     self.log_area.insert(END, '正在处理 %s ...\n' % i)
        #     qmc_file_decrypt(self.file_list[i], self.output_dir)
        #     end_time = time.time()
        #     total_time = end_time - start_time
        #     self.file_list_box.delete(0)
        #     self.file_list.pop(i)
        #     self.log_area.insert(END, '文件处理完毕\n')
        #     self.log_area.insert(END, '共耗时 %d 秒\n' % total_time)
        #     self.log_area.insert(END, '******************************* \n')
        #     self.log_area.see(END)
        #     self.log_area.update()

        for i in list(self.file_list):
            start_time = time.time()
            self.log_area.insert(END, '正在处理 %s ...\n' % i)
            qmc_file_decrypt(self.file_list[i], self.output_dir)
            end_time = time.time()
            total_time = end_time - start_time
            self.file_list_box.delete(0)
            del self.file_list[i]
            self.log_area.insert(END, '文件处理完毕\n')
            self.log_area.insert(END, '共耗时 %d 秒\n' % total_time)
            self.log_area.insert(END, '******************************* \n')
            self.log_area.see(END)
            self.log_area.update()


class App:
    def __init__(self, root):

        self.root = root
        self.file_list = {}
        # self.file_name_list = []
        self.file_names = StringVar()
        self.out_dir = StringVar()
        self.init_menu()
        self.init_input_frame()
        self.init_handle_frame()

    def init_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        # file_menu.add_command(label='添加文件', command=self._open_file)
        file_menu.add_command(label='添加文件', command=self._open_directory)
        file_menu.add_command(label='指定输出路径', command=self._assign_output_dir)
        file_menu.add_command(label='清除所有文件', command=self._clear_all_file)
        file_menu.add_command(label='退出', command=self.root.quit)
        menubar.add_cascade(label='操作', menu=file_menu)

        about_menu = tk.Menu(menubar, tearoff=0)
        about_menu.add_command(label='使用说明', command=self._how_to_use)
        about_menu.add_command(label='关于', command=self._about)
        menubar.add_cascade(label='关于', menu=about_menu)

    def init_input_frame(self):
        # self.out_dir.set('aaaaaa')
        input_frame = tk.Frame(bg='grey')
        input_frame.place(x=5, y=5, width=190, height=290)
        input_label = tk.Label(input_frame, bg='yellow', text='待处理文件').pack(side='top', fill='x')
        list_box_scroll = tk.Scrollbar(input_frame)
        list_box_scroll.pack(side=RIGHT, fill=Y)
        self.file_list_box = tk.Listbox(input_frame, listvariable=self.file_names)
        self.file_list_box.pack(side='top', fill=BOTH, expand=YES, anchor=CENTER)
        list_box_scroll.config(command=self.file_list_box.yview)
        self.file_list_box.config(yscrollcommand=list_box_scroll.set)
        out_dir_label = tk.Label(input_frame, bg='yellow', text='输出文件路径').pack(side=TOP, fill=X)
        out_dir_entry = tk.Entry(input_frame, bg='grey', textvariable=self.out_dir).pack(side=BOTTOM, fill=X)

    def init_handle_frame(self):
        handle_frame = tk.Frame(bg='yellow')
        handle_frame.place(x=205, y=5, width=290, height=290)
        handle_button = tk.Button(handle_frame, text='开始转换', command=self.do_it).pack(side=TOP)
        scroll = tk.Scrollbar(handle_frame)
        scroll.pack(side=RIGHT, fill=Y)
        self.log_area = tk.Text(handle_frame, bg='cyan', foreground='gray')
        self.log_area.pack(side=BOTTOM)
        scroll.config(command=self.log_area.yview)
        self.log_area.config(yscrollcommand=scroll.set)

    def _open_directory(self):
        file_opened = filedialog.askopenfilenames()
        for file in file_opened:
            file_path = file
            file_name = file_path.split('/')[-1]
            print(file_name)
            if self.is_qmc_file(file_name) and file_name not in self.file_list:
                file = {file_name: file_path}
                # self.file_name_list.append(file_name)
                self.file_list.update(file)
                print(self.file_list)
                self.file_names.set(list(self.file_list))
                # print(self.file_name_list)
                # print(self.file_list_box.get(0, len(self.file_list) - 1))
            else:
                pass

    def _assign_output_dir(self):
        out_dir_str = filedialog.askdirectory()
        self.out_dir.set(out_dir_str)

    def _clear_all_file(self):
        self.file_list_box.delete(0, len(self.file_list) - 1)
        self.file_list = {}

    def is_qmc_file(self, file_name):
        suffix_list = ['qmcogg', 'qmcflac']
        try:
            file_suffix = file_name.split('.')[-1]
            if file_suffix not in suffix_list:
                return False
            else:
                return True
        except Exception as e:
            return False

    def do_it(self):
        # print(self.file_list)
        if self.out_dir.get() == '':
            messagebox.showwarning(title='警告', message='请先指定输出文件夹！')
            pass
        elif len(self.file_list) == 0:
            messagebox.showwarning(title='提示', message='请先输入要处理的文件!')
        else:
            out_dir_str = self.out_dir.get()
            # file_items = self.file_list_box.get(0, len(self.file_list) - 1)

            print(threading.activeCount())
            if threading.activeCount() <= 1:
                t = HandleThread(file_list_box=self.file_list_box, log_area=self.log_area, file_list=self.file_list,
                                 output_dir=out_dir_str)
                t.start()
            else:
                messagebox.showinfo(title='提示', message='正在处理中，请稍后再进行其他操作！')

    def _how_to_use(self):
        messagebox.showinfo(title='使用说明', message='此工具可将QQ音乐下载下来的VIP加密歌曲文件转换成一般播放器可识别的文件格式'
                                                  '， 目前支持解密的文件格式包括：.qmcogg, .qmcflac')

    def _about(self):
        messagebox.showinfo(title='关于', message='此工具仅供个人学习交流，未用于任何商业用途！')


root = tk.Tk()
root.title('qq音乐VIP歌曲破解器')
root.geometry('500x300')
root.resizable(False, False)
app = App(root)
root.mainloop()
