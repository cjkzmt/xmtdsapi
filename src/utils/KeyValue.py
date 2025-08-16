import sqlite3

class Kv:
    db_name = 'kv.db'

    @staticmethod
    def _get_connection():
        conn = sqlite3.connect(Kv.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS kv (
            name TEXT PRIMARY KEY,
            value TEXT
        )''')
        conn.commit()
        return conn, cursor

    @staticmethod
    def get(name, value=None):
        if not name:
            return None
        conn, cursor = Kv._get_connection()
        cursor.execute('SELECT value FROM kv WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()
        if result:
            try:
                # 尝试将结果转换为整数
                numeric_result = int(result[0])
                # 如果 value 存在且类型不同，则返回默认值
                if value is not None and type(numeric_result) != type(value):
                    return value
                return numeric_result
            except ValueError:
                # 如果不是数字，则直接返回原始字符串
                if value is not None and type(result[0]) != type(value):
                    return value
                return result[0]
        else:
            return value if value is not None else None

    @staticmethod
    def save(name, value):
        if not name:
            return
        conn, cursor = Kv._get_connection()
        cursor.execute('INSERT OR REPLACE INTO kv (name, value) VALUES (?, ?)', (name, str(value)))
        conn.commit()
        conn.close()

# 示例使用
if __name__ == '__main__':
    # 测试 save 方法
    Kv.save("name", "Alice")
    Kv.save("age", 25)
    Kv.save("is_student", False)

    # 测试 get 方法
    print(Kv.get("name"))  # 输出：Alice
    print(Kv.get("age"))  # 输出：25
    print(Kv.get("is_student"))  # 输出：False
    print(Kv.get("nonexistent", "default_value"))  # 输出：default_value
    print(Kv.get(""))  # 输出：None