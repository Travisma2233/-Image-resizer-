import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import webbrowser

class ImageResizerApp:
    def __init__(self, root):
        self.root = root
        self.selected_files = []
        self.setup_language()
        self.setup_styles()
        self.setup_ui()

    def setup_language(self):
        self.languages = {
            "中文": {
                "title": "图片分辨率转换器",
                "select_image": "选择图片",
                "delete_selected": "删除选中",
                "selected_files": "已选择的文件",
                "preview": "图片预览",
                "original_size": "原始尺寸：",
                "target_resolution": "选择目标分辨率",
                "custom": "自定义",
                "select_save_dir": "选择保存目录",
                "convert": "开始转换",
                "save_dir_not_selected": "未选择保存目录",
                "please_select_image": "请先选择图片文件！",
                "invalid_resolution": "请输入有效的分辨率数值！",
                "empty_preview": "请选择要转换的图片文件\n支持jpg、jpeg、png、bmp、gif格式",
                "processing": "正在处理第 {}/{}个文件...",
                "all_completed": "所有文件处理完成！"
            },
            "English": {
                "title": "Image Resolution Converter",
                "select_image": "Select Images",
                "delete_selected": "Delete Selected",
                "selected_files": "Selected Files",
                "preview": "Image Preview",
                "original_size": "Original Size: ",
                "target_resolution": "Select Target Resolution",
                "custom": "Custom",
                "select_save_dir": "Select Save Directory",
                "convert": "Convert",
                "save_dir_not_selected": "Save directory not selected",
                "please_select_image": "Please select image files first!",
                "invalid_resolution": "Please enter valid resolution values!",
                "empty_preview": "Please select images to convert\nSupports jpg, jpeg, png, bmp, gif formats",
                "processing": "Processing file {}/{}...",
                "all_completed": "All files processed successfully!"
            }
        }
        self.current_language = "中文"

    def setup_styles(self):
        style = ttk.Style()
        self.current_font = ("Microsoft YaHei", 10) if self.current_language == "中文" else ("Times New Roman", 10)
        
        # 基础样式
        style.configure('Main.TFrame', background='#f5f5f5')
        
        # 按钮通用布局
        button_layout = [('Button.focus', {'children': [
            ('Button.button', {'children': [
                ('Button.padding', {'children': [
                    ('Button.label', {'sticky': 'nswe'})
                ], 'sticky': 'nswe'})
            ], 'sticky': 'nswe'})
        ], 'sticky': 'nswe'})]
        
        # 按钮样式配置
        button_styles = {
            'Delete.TButton': {'bg': 'white', 'active_bg': '#f0f0f0', 'fg': 'black'},
            'Accent.TButton': {'bg': 'white', 'active_bg': '#f0f0f0', 'fg': 'black'},
            'Secondary.TButton': {'bg': 'white', 'active_bg': '#f0f0f0', 'fg': 'black'},
            'Preview.TButton': {'bg': 'black', 'active_bg': '#333333', 'fg': 'white'}
        }
        
        for btn_style, colors in button_styles.items():
            style.layout(btn_style, button_layout)
            style.configure(btn_style,
                          font=self.current_font,
                          background=colors['bg'],
                          foreground=colors['fg'],
                          borderwidth=1,
                          relief="raised")
            style.map(btn_style,
                     background=[('active', colors['active_bg'])],
                     relief=[('pressed', 'sunken')])
        
        # 标签和框架样式
        style.configure('Info.TLabel', background='#f5f5f5', foreground='black', font=self.current_font)
        style.configure('Empty.TLabel', background='white', foreground='black', font=self.current_font)
        style.configure('GitHub.TLabel', background='#f5f5f5', foreground='black', font=self.current_font)
        style.configure('Status.TLabel', background='#f5f5f5', foreground='black', font=self.current_font)
        
        for frame_style in ['Preview.TLabelframe', 'Files.TLabelframe', 'Custom.TLabelframe']:
            style.configure(frame_style, background='white', foreground='black')
            style.configure(f'{frame_style}.Label', background='white', foreground='black', font=self.current_font)

    def setup_ui(self):
        self.root.title(self.languages[self.current_language]["title"])
        self.root.geometry("1000x700")
        self.root.configure(bg='#f5f5f5')
        self.root.minsize(1200, 1000)
        
        # 主框架设置
        main_frame = ttk.Frame(self.root, padding="15", style='Main.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 语言选择
        language_frame = ttk.Frame(main_frame, style='Main.TFrame')
        language_frame.pack(fill=tk.X, pady=(0, 10))
        self.language_var = tk.StringVar(value=self.current_language)
        language_menu = ttk.Combobox(language_frame, textvariable=self.language_var,
                                   values=list(self.languages.keys()), width=10, state="readonly")
        language_menu.pack(side=tk.RIGHT)
        language_menu.bind('<<ComboboxSelected>>', self.change_language)
        
        # 左侧面板
        left_panel = ttk.Frame(main_frame, style='Main.TFrame')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 文件操作按钮
        button_frame = ttk.Frame(left_panel, style='Main.TFrame')
        button_frame.pack(pady=(0, 10))
        self.select_btn = ttk.Button(button_frame, text=self.languages[self.current_language]["select_image"],
                                   command=self.select_image, style='Accent.TButton')
        self.select_btn.pack(side=tk.LEFT, padx=(0, 10))
        self.delete_btn = ttk.Button(button_frame, text=self.languages[self.current_language]["delete_selected"],
                                   command=self.delete_selected, style='Delete.TButton')
        self.delete_btn.pack(side=tk.LEFT)
        
        # 文件列表
        files_frame = ttk.LabelFrame(left_panel, text=self.languages[self.current_language]["selected_files"],
                                   padding="10", style='Files.TLabelframe')
        files_frame.pack(fill=tk.X, pady=(0, 10))
        self.files_listbox = tk.Listbox(files_frame, selectmode=tk.EXTENDED, height=4,
                                      font=self.current_font, bg='white', fg='#333333')
        self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL, command=self.files_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.files_listbox.configure(yscrollcommand=scrollbar.set)
        self.files_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # 预览区域
        preview_frame = ttk.LabelFrame(left_panel, text=self.languages[self.current_language]["preview"],
                                     padding="5", style='Preview.TLabelframe')
        preview_frame.pack(fill=tk.BOTH, expand=True)
        
        # 原始尺寸显示（居中）
        size_frame = ttk.Frame(preview_frame, style='Main.TFrame')
        size_frame.pack(fill=tk.X, pady=(5, 0))
        self.size_label = ttk.Label(size_frame, text="", style='Info.TLabel')
        self.size_label.pack(anchor=tk.CENTER)
        
        self.preview_canvas = tk.Canvas(preview_frame, bg='white', highlightthickness=0)
        self.preview_canvas.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.empty_label = ttk.Label(self.preview_canvas, text=self.languages[self.current_language]["empty_preview"],
                                   style='Empty.TLabel', justify=tk.CENTER)
        self.preview_canvas.create_window(450, 300, window=self.empty_label, anchor='center')
        
        # 预览控制按钮
        self.preview_controls = ttk.Frame(preview_frame, style='Preview.TLabel')
        self.preview_controls.pack(pady=5)
        self.prev_btn = ttk.Button(self.preview_controls, text="←", command=self.prev_image,
                                 style='Preview.TButton', width=3)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        self.next_btn = ttk.Button(self.preview_controls, text="→", command=self.next_image,
                                 style='Preview.TButton', width=3)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        self.preview_controls.pack_forget()
        
        # 右侧面板
        right_panel = ttk.Frame(main_frame, style='Main.TFrame')
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 分辨率选择
        resolution_frame = ttk.LabelFrame(right_panel, text=self.languages[self.current_language]["target_resolution"],
                                        padding="10", style='Custom.TLabelframe')
        resolution_frame.pack(fill=tk.X)
        
        self.resolutions = ["640x480", "800x600", "1024x768", "1280x720", "1920x1080", "2560x1440", "3840x2160",
                           self.languages[self.current_language]["custom"]]
        self.resolution_var = tk.StringVar(value=self.resolutions[0])
        self.resolution_combo = ttk.Combobox(resolution_frame, textvariable=self.resolution_var,
                                           values=self.resolutions, width=15, state="readonly")
        self.resolution_combo.pack(padx=5, pady=5)
        self.resolution_combo.bind('<<ComboboxSelected>>', self.on_resolution_change)
        
        # 自定义分辨率输入
        self.custom_frame = ttk.Frame(resolution_frame, style='Main.TFrame')
        self.width_var, self.height_var = tk.StringVar(), tk.StringVar()
        ttk.Entry(self.custom_frame, width=6, textvariable=self.width_var).pack(side=tk.LEFT)
        ttk.Label(self.custom_frame, text="x", style='Info.TLabel').pack(side=tk.LEFT, padx=2)
        ttk.Entry(self.custom_frame, width=6, textvariable=self.height_var).pack(side=tk.LEFT)
        
        # 操作按钮
        operation_frame = ttk.Frame(right_panel, style='Main.TFrame')
        operation_frame.pack(fill=tk.X, pady=10)
        self.save_btn = ttk.Button(operation_frame, text=self.languages[self.current_language]["select_save_dir"],
                                 command=self.select_save_directory, style='Secondary.TButton')
        self.save_btn.pack(side=tk.LEFT, padx=(0, 5))
        self.convert_btn = ttk.Button(operation_frame, text=self.languages[self.current_language]["convert"],
                                    command=self.convert_image, style='Accent.TButton')
        self.convert_btn.pack(side=tk.LEFT)
        
        self.save_label = ttk.Label(right_panel, text=self.languages[self.current_language]["save_dir_not_selected"],
                                  style='Info.TLabel', wraplength=200)
        self.save_label.pack(pady=5)
        
        self.status_label = ttk.Label(right_panel, text="", style='Status.TLabel', wraplength=200)
        self.status_label.pack(pady=5)
        
        # GitHub水印
        github_label = ttk.Label(self.root, text="GitHub: Travisma2233", cursor="hand2", style='GitHub.TLabel')
        github_label.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=5)
        github_label.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/Travisma2233"))

    def change_language(self, event=None):
        self.current_language = self.language_var.get()
        self.update_ui_text()

    def update_ui_text(self):
        self.root.title(self.languages[self.current_language]["title"])
        self.select_btn.configure(text=self.languages[self.current_language]["select_image"])
        self.delete_btn.configure(text=self.languages[self.current_language]["delete_selected"])
        
        # 更新所有LabelFrame的标题
        for widget in self.root.winfo_children():
            self._update_widget_text(widget)
        
        # 更新空状态文本
        self.empty_label.configure(text=self.languages[self.current_language]["empty_preview"])
        
        # 更新分辨率选项
        current_resolutions = self.resolutions[:-1]  # 除去最后的"自定义"选项
        current_resolutions.append(self.languages[self.current_language]["custom"])
        self.resolutions = current_resolutions
        current_value = self.resolution_var.get()
        self.resolution_combo.configure(values=self.resolutions)
        if current_value == self.languages["中文" if self.current_language == "English" else "English"]["custom"]:
            self.resolution_var.set(self.languages[self.current_language]["custom"])
        
        # 更新其他文本
        if not hasattr(self, 'save_directory'):
            self.save_label.configure(text=self.languages[self.current_language]["save_dir_not_selected"])
        self.save_btn.configure(text=self.languages[self.current_language]["select_save_dir"])
        self.convert_btn.configure(text=self.languages[self.current_language]["convert"])
        
        # 更新原始尺寸文本
        if hasattr(self, 'current_preview_index') and self.selected_files:
            img = Image.open(self.selected_files[self.current_preview_index])
            width, height = img.size
            self.size_label.config(text=f"{self.languages[self.current_language]['original_size']}{width}x{height}")

    def _update_widget_text(self, widget):
        if isinstance(widget, ttk.LabelFrame):
            current_text = widget.cget("text")
            # 检查是否是需要更新的标签框
            for key in ["selected_files", "preview", "target_resolution"]:
                if current_text == self.languages["中文" if self.current_language == "English" else "English"][key]:
                    widget.configure(text=self.languages[self.current_language][key])
        # 递归处理所有子部件
        for child in widget.winfo_children():
            self._update_widget_text(child)

    def select_image(self):
        files = filedialog.askopenfilenames(
            filetypes=[("图片文件", "*.jpg *.jpeg *.png *.bmp *.gif")] if self.current_language == "中文" else
                     [("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        if files:
            self.selected_files.extend(files)
            self.update_files_list()
            # 预览第一张图片
            if len(self.selected_files) == 1:
                self.preview_image(self.selected_files[0])

    def update_files_list(self):
        self.files_listbox.delete(0, tk.END)
        for file in self.selected_files:
            self.files_listbox.insert(tk.END, os.path.basename(file))

        # 更新预览状态
        if self.selected_files:
            self.empty_label.place_forget()
            self.current_preview_index = 0
            self.preview_image(self.selected_files[0])
            self.update_preview_controls()
        else:
            # 清除预览
            self.preview_canvas.delete('all')
            self.empty_label.place(relx=0.5, rely=0.5, anchor='center')
            if hasattr(self, 'preview_controls'):
                self.preview_controls.pack_forget()
            self.size_label.configure(text="")
            # 重置预览图片
            self.preview_canvas.image = None

    def delete_selected(self):
        selected_indices = self.files_listbox.curselection()
        if not selected_indices:
            return

        # 从后往前删除，避免索引变化
        for index in sorted(selected_indices, reverse=True):
            del self.selected_files[index]

        # 清除预览状态
        if not self.selected_files:
            self.preview_canvas.delete('all')
            self.empty_label.place(relx=0.5, rely=0.5, anchor='center')
            if hasattr(self, 'preview_controls'):
                self.preview_controls.pack_forget()
            self.size_label.configure(text="")
            # 重置预览图片
            self.preview_canvas.image = None
        
        self.update_files_list()

    def preview_image(self, file_path):
        img = Image.open(file_path)
        # 显示原始尺寸
        width, height = img.size
        self.size_label.config(
            text=f"{self.languages[self.current_language]['original_size']}{width}x{height}"
        )
        self.update_preview(img)

    def select_save_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.save_directory = directory
            self.save_label.config(text=os.path.basename(directory) or directory)

    def on_resolution_change(self, event=None):
        if self.resolution_var.get() == self.languages[self.current_language]["custom"]:
            self.custom_frame.pack(padx=5, pady=(10, 0))
        else:
            self.custom_frame.pack_forget()

    def convert_image(self):
        if not self.selected_files:
            self.status_label.config(text=self.languages[self.current_language]["please_select_image"])
            return

        if not hasattr(self, 'save_directory'):
            self.status_label.config(text=self.languages[self.current_language]["save_dir_not_selected"])
            return

        try:
            # 获取目标分辨率
            if self.resolution_var.get() == self.languages[self.current_language]["custom"]:
                try:
                    width = int(self.width_var.get())
                    height = int(self.height_var.get())
                except ValueError:
                    self.status_label.config(text=self.languages[self.current_language]["invalid_resolution"])
                    return
            else:
                width, height = map(int, self.resolution_var.get().split('x'))

            total_files = len(self.selected_files)
            
            # 禁用转换按钮，防止重复点击
            self.convert_btn.configure(state='disabled')
            
            for i, file_path in enumerate(self.selected_files, 1):
                # 更新处理状态
                self.status_label.config(
                    text=self.languages[self.current_language]["processing"].format(i, total_files)
                )
                self.root.update_idletasks()  # 使用update_idletasks代替update

                # 打开并调整图片大小
                img = Image.open(file_path)
                resized_img = img.resize((width, height), Image.Resampling.LANCZOS)

                # 保存转换后的图片
                file_name = os.path.basename(file_path)
                name, ext = os.path.splitext(file_name)
                output_path = os.path.join(self.save_directory, f"{name}_resized_{width}x{height}{ext}")
                resized_img.save(output_path)

            # 完成后更新状态
            self.status_label.config(text=self.languages[self.current_language]["all_completed"])
            
            # 重新启用转换按钮
            self.convert_btn.configure(state='normal')

        except Exception as e:
            self.status_label.config(text=str(e))
            self.convert_btn.configure(state='normal')

    def on_file_select(self, event):
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            self.preview_image(self.selected_files[index])
            self.current_preview_index = index
            self.update_preview_controls()

    def prev_image(self):
        if hasattr(self, 'current_preview_index') and self.current_preview_index > 0:
            self.current_preview_index -= 1
            self.preview_image(self.selected_files[self.current_preview_index])
            self.files_listbox.selection_clear(0, tk.END)
            self.files_listbox.selection_set(self.current_preview_index)
            self.files_listbox.see(self.current_preview_index)
            self.update_preview_controls()

    def next_image(self):
        if hasattr(self, 'current_preview_index') and self.current_preview_index < len(self.selected_files) - 1:
            self.current_preview_index += 1
            self.preview_image(self.selected_files[self.current_preview_index])
            self.files_listbox.selection_clear(0, tk.END)
            self.files_listbox.selection_set(self.current_preview_index)
            self.files_listbox.see(self.current_preview_index)
            self.update_preview_controls()

    def update_preview_controls(self):
        if self.selected_files:
            self.preview_controls.grid()
            self.prev_btn.configure(state='normal' if self.current_preview_index > 0 else 'disabled')
            self.next_btn.configure(
                state='normal' if self.current_preview_index < len(self.selected_files) - 1 else 'disabled')
        else:
            self.preview_controls.grid_remove()

    def update_preview(self, img):
        try:
            # 获取Canvas当前大小
            canvas_width = self.preview_canvas.winfo_width()
            canvas_height = self.preview_canvas.winfo_height()
            
            if canvas_width <= 1 or canvas_height <= 1:  # Canvas尚未完全初始化
                canvas_width = 900
                canvas_height = 600
            
            # 计算缩放比例
            width_ratio = (canvas_width - 20) / img.size[0]  # 留出一些边距
            height_ratio = (canvas_height - 20) / img.size[1]
            ratio = min(width_ratio, height_ratio)
            
            # 计算新尺寸
            new_width = int(img.size[0] * ratio)
            new_height = int(img.size[1] * ratio)
            
            # 如果已经有缓存的相同尺寸图片，直接使用
            if hasattr(self, '_cached_preview') and \
               hasattr(self, '_cached_size') and \
               self._cached_size == (new_width, new_height):
                photo = self._cached_preview
            else:
                # 调整图片大小
                preview_img = img.copy()
                preview_img = preview_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                # 创建PhotoImage并缓存
                photo = ImageTk.PhotoImage(preview_img)
                self._cached_preview = photo
                self._cached_size = (new_width, new_height)
            
            # 清除Canvas上的所有内容
            self.preview_canvas.delete('all')
            
            # 在Canvas中央显示图片
            x = canvas_width // 2
            y = canvas_height // 2
            self.preview_canvas.create_image(x, y, image=photo, anchor='center')
            self.preview_canvas.image = photo  # 保持引用
            
        except Exception as e:
            print(f"预览更新错误: {str(e)}")
            self.preview_canvas.delete('all')
            self.empty_label.place(relx=0.5, rely=0.5, anchor='center')


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageResizerApp(root)
    root.mainloop() 