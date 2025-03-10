import sys
import os
import sqlite3


def init_db():
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY,task TEXT,category TEXT,completed INTEGER)""")
    conn.commit()
    conn.close()


def load_tasks():
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("SELECT task,category,completed FROM tasks")
    tasks = [{"task": row[0], "category": row[1], "completed": bool(row[2])} for row in c.fetchall()]
    conn.close()
    return tasks


def save_task(task, category):
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks(task,category,completed) VALUES(?,?,?)", (task, category, 0))
    conn.commit()
    conn.close()


def mark_task_completed(task_id):
    conn = sqlite3.connect("todos.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()


init_db()
todos = load_tasks()  # todos的意思是待办事项  代办事项列表


def show_menu():  # 这是一个函数 def定义
    print("\n待办事项清单")
    print("1.添加任务")
    print("2.查看任务")
    print("3.删除任务")
    print("4.修改任务")  # 自己添加的功能，一次实现 牛逼
    print("5.退出")


while True:
    show_menu()
    choice = input("请选择操作（1-5）：")  # input的返回类型是字符串

    if choice == "1":
        task = input("输入要添加的任务：").strip()  # strip()是用来消除句子两端的空格的
        if task:
            category = input("输入任务分类（例如：工作/生活/学习：").strip()
            save_task(task, category)
            todos.append({"task": task, "category": category, "completed": False})
            print(f"已添加的任务：{task}(分类：{category})")
        else:
            print("任务内容不能为空！")


    elif choice == "2":
        print("\n当前任务：")
        for index, item in enumerate(todos, 1):
            print(f"{index}.{item['task']}(分类：{item['category']})")

    elif choice == "3":
        try:
            num = int(input("要删除的任务编号："))
            if 1 <= num <= len(todos):
                removed = todos.pop(num - 1)
                mark_task_completed(num)
                print(f"已删除任务：{removed['task']}(分类：{removed['category']})")
            else:
                print("无效的编号！")
        except ValueError:
            print("请输入数字编号！")

    elif choice == "4":
        try:
            num2 = int(input("要修改的任务编号："))
            if 1 <= num2 <= len(todos):
                task2 = input("请输入修改后的任务：")
                if task2:
                    category = input("输入任务分类（例如：工作/生活/学习：")
                    todos[num2 - 1] = {"task": task2, "category": category.strip(),
                                       "completed": todos[num2 - 1]["completed"]}
                else:
                    print("任务内容不能为空！")
        except ValueError:
            print("请输入数字编号！")

    elif choice == "5":
        print("再见！")
        break

    else:
        print("无效输入，请重新选择")

'''
关键知识点总结：
列表操作：append(), pop()

文件操作：open(), read(), write()

错误处理：try-except

字符串处理：strip()

函数定义与调用

循环结构：while True

条件判断：if-elif-else

字典：存储键值对数据。

列表嵌套字典：管理多个复杂对象。

SQLite 数据库操作：连接、查询、插入、更新
'''
