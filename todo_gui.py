import tkinter as tk
from tkinter import messagebox
from todo_db import TodoDB

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("待办事项清单")
        self.db = TodoDB()

        # 任务输入框
        self.label_task = tk.Label(root, text="任务:")
        self.label_task.grid(row=0, column=0, padx=10, pady=10)
        self.entry_task = tk.Entry(root, width=40)
        self.entry_task.grid(row=0, column=1, padx=10, pady=10)

        # 分类输入框
        self.label_category = tk.Label(root, text="分类:")
        self.label_category.grid(row=1, column=0, padx=10, pady=10)
        self.entry_category = tk.Entry(root, width=40)
        self.entry_category.grid(row=1, column=1, padx=10, pady=10)

        # 添加任务按钮
        self.button_add = tk.Button(root, text="添加任务", command=self.add_task)
        self.button_add.grid(row=2, column=0, columnspan=2, pady=10)

        # 任务列表
        self.listbox_tasks = tk.Listbox(root, width=50)
        self.listbox_tasks.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # 删除任务按钮
        self.button_delete = tk.Button(root, text="删除任务", command=self.delete_task)
        self.button_delete.grid(row=4, column=0, columnspan=2, pady=10)

        # 加载任务
        self.load_tasks()

    def load_tasks(self):
        """加载任务到列表"""
        self.listbox_tasks.delete(0, tk.END)
        tasks = self.db.load_tasks()
        for task in tasks:
            status = "已完成" if task["completed"] else "未完成"
            self.listbox_tasks.insert(tk.END, f"{task['task']}（分类：{task['category']}，状态：{status}）")

    def add_task(self):
        """添加任务"""
        task = self.entry_task.get().strip()
        category = self.entry_category.get().strip()
        if task:
            self.db.add_task(task, category)
            self.load_tasks()
            self.entry_task.delete(0, tk.END)
            self.entry_category.delete(0, tk.END)
        else:
            messagebox.showwarning("警告", "任务内容不能为空！")

    def delete_task(self):
        """删除任务"""
        try:
            selected_task_index = self.listbox_tasks.curselection()[0]
            tasks = self.db.load_tasks()
            task_id = tasks[selected_task_index]["id"]
            self.db.delete_task(task_id)
            self.load_tasks()
        except IndexError:
            messagebox.showwarning("警告", "请选择一个任务！")
