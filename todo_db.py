import sqlite3

class TodoDB:
    def __init__(self, db_name="todos.db"):
        self.db_name = db_name
        self._init_db()

    def _init_db(self):
        """初始化数据库，创建表"""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS tasks
                         (id INTEGER PRIMARY KEY, task TEXT, category TEXT, completed INTEGER)""")
            conn.commit()

    def _get_connection(self):
        """获取数据库连接"""
        return sqlite3.connect(self.db_name)

    def load_tasks(self):
        """加载所有任务"""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT id, task, category, completed FROM tasks")
            tasks = [{"id": row[0], "task": row[1], "category": row[2], "completed": bool(row[3])} for row in c.fetchall()]
            return tasks

    def add_task(self, task, category):
        """添加任务"""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("INSERT INTO tasks (task, category, completed) VALUES (?, ?, ?)",
                      (task, category, 0))
            conn.commit()

    def mark_task_completed(self, task_id):
        """标记任务为已完成"""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
            conn.commit()

    def delete_task(self, task_id):
        """删除任务"""
        with self._get_connection() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
