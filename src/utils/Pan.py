from mysql.connector import Error
import mysql.connector
import math
import os

config = {
    'host': '8.140.162.237',
    'port': 3307,
    'database': 'db_dev_5469',
    'user': '15011507220',
    'password': 'cui2210996',
    'charset': 'utf8mb4',
}


def query_db(table_name: str, search_dict: dict):
    # print(f"查询表: {table_name}{search_dict}")
    if not search_dict:
        return {}

    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor(buffered=True) as cursor:
                # 1. 取列名
                cursor.execute(f"SHOW COLUMNS FROM `{table_name}`")
                columns = [col[0] for col in cursor.fetchall()]

                # 2. 构造 WHERE 子句
                placeholders = [f"`{k}` = %s" for k in search_dict.keys()]
                where_clause = " AND ".join(placeholders)
                query = f"SELECT * FROM `{table_name}` WHERE {where_clause}"

                # 3. 执行查询
                cursor.execute(query, tuple(search_dict.values()))
                rows = cursor.fetchall()

                if not rows:
                    return {}

                # 4. 结果转字典
                return [dict(zip(columns, row)) for row in rows]

    except mysql.connector.Error as e:
        print("数据库操作错误：", e)
        return {}
def delete_db( 表名, 字段名, 值):
    delete_query = f"""
    DELETE FROM `{表名}`
    WHERE `{字段名}` = %s
    """
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(delete_query, (值,))
                affected_rows = cursor.rowcount
                conn.commit()
                # if affected_rows > 0:
                #     print(f"成功删除 {affected_rows} 条记录")
    except mysql.connector.Error as e:
        print("数据库操作错误：", e)

def create_db(table, data):
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(table, data)
                conn.commit()
    except Error as e:
        print("Error while connecting to MySQL", e)


def sync(local_dir, path, file_list = None):
    try:
        path_list = []
        if file_list:
            for file_name in file_list:
                file_path = os.path.join(local_dir, file_name)
                if os.path.isfile(file_path):
                    path_list.append(file_path)
                else:
                    print(f"⚠️ 文件不存在: {file_path}")
        else:
            for root, _, files in os.walk(local_dir):
                for file_name in files:
                    file_path = os.path.join(root, file_name)
                    path_list.append(file_path)
        SUM=len(path_list)
        for index, file_path in enumerate(path_list):
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                binary_data = f.read()
            file_size = os.path.getsize(file_path)
            sum_blocks = math.ceil(file_size / (1024 * 1024))
            file_type = os.path.splitext(file_path)[1] or "unknown"
            pan_record = query_db( 'pan', {'name': file_name})
            if pan_record:
                pan_record=pan_record[0]
                if  pan_record['size'] == file_size:
                    print(f'⚠️ 文件已存在且大小一致: {path}/{file_name}')
                    continue
            delete_db( 'pan', 'name', file_name)
            delete_db( 'pandata', 'name', file_name)
            sta_data = 0
            syncpandata = f"""INSERT INTO pandata ( name,number,data) VALUES (%s,%s,%s)"""
            for i in range(sum_blocks):
                end_data = min(sta_data + 1024 * 1024, file_size)
                chunk = binary_data[sta_data:end_data]
                pdata = (file_name, i, chunk)
                create_db(syncpandata,pdata)
                sta_data = end_data
            syncpandata = f"""INSERT INTO pan (name,path,size,type) VALUES(%s,%s,%s,%s)"""
            pdata = (file_name, path, file_size, file_type)
            create_db(syncpandata,pdata)
            print(f'✅ （{index+1}/{SUM}）上传成功: {path}/{file_name}')
    except Exception as e:
        raise e

def downloaded(local_dir, path, file_list = None):
    os.makedirs(local_dir, exist_ok=True)
    if file_list:
        name_list = file_list
    else:
        records = query_db( 'pan', {'path': path})
        name_list = [r['name'] for r in records]
    SUM=len(name_list)
    for index, name in enumerate(name_list):
        output_path = os.path.join(local_dir, name)
        try:
            pan_record = query_db( 'pan', {'name': name})[0]
            chunks = []
            for i in range(math.ceil(pan_record['size'] / (1024 * 1024))):
                data_record =  query_db( 'pandata',  {'name': name,'number':i})[0]   
                chunks.append(data_record['data'])
            full_data = b''.join(chunks)
            with open(output_path, "wb") as f:
                f.write(full_data)
            print(f'✅ （{index+1}/{SUM}）下载成功: {output_path}')
        except Exception as e:
            print(f'❌ 下载失败 [{name}]: {e}')
            raise e

def deletePan(path, file_list):
    for file_name in file_list:
        try:
            delete_db( 'pan', 'name', file_name)
            delete_db( 'pandata', 'name', file_name)
            print(f'✅ 删除成功: {path}/{file_name}')
        except Exception as e:
            print(f'❌ 删除失败 [{file_name}]: {e}')

