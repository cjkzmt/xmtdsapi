from tortoise.models import Model
from tortoise import fields
from tortoise import Tortoise
from typing import List, Optional
import os
import math
import asyncio

class Pan(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, index=True, description="文件名")
    path = fields.CharField(max_length=255, description="路径")
    size = fields.IntField(default=0, description="文件大小")
    type = fields.CharField(max_length=128, null=True, default=None, description="文件类型")
    endCreateTime = fields.DatetimeField(auto_now_add=True, description="创建时间")

class PanData(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=128, description="文件名")
    number = fields.IntField(default=0, description="文件序号")
    data = fields.BinaryField(description="文件数据")

PAN_TORTOISE_ORM  = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': {
                'host': '8.140.162.237',
                'port': 3307,
                'user': '15011507220',
                'password': 'cui2210996',
                'database': 'db_dev_5469',
                'charset': 'utf8mb4',
                "pool_recycle": 3600,
                "connect_timeout": 60,
                'minsize': 1,
                'maxsize': 5,
                'echo': True,
            }
        }
    },
    'apps': {
        'models': {
            'models': ['aerich.models' ,'src.utils.Pan'],  # 只包含Pan模块自己的模型，避免与主程序冲突
            'default_connection': 'default',
        }
    }
}

async def sync(local_dir: str, path: str, file_list: Optional[List[str]] = None):
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
    await Tortoise.init(config=PAN_TORTOISE_ORM )
    SUM=len(path_list)
    for index, file_path in enumerate(path_list):
        file_name = os.path.basename(file_path)
        for attempt in range(3):
            try:
                with open(file_path, "rb") as f:
                    binary_data = f.read()
                file_size = os.path.getsize(file_path)
                sum_blocks = math.ceil(file_size / (1024 * 1024))
                file_type = os.path.splitext(file_path)[1] or "unknown"
                try:
                    pan_record = await Pan.get(name=file_name)
                    if  pan_record.size == file_size:
                        print(f'⚠️ 文件已存在且大小一致: {path}/{file_name}')
                        break
                except :  
                    pass
                await PanData.filter(name=file_name).delete()  # 先清空旧块
                await Pan.filter(name=file_name).delete()  # 先清空旧块
                sta_data = 0
                for i in range(sum_blocks):
                    end_data = min(sta_data + 1024 * 1024, file_size)
                    chunk = binary_data[sta_data:end_data]
                    await PanData.create(name=file_name, number=i, data=chunk)
                    sta_data = end_data
                await Pan.create(name=file_name,path=path,size=file_size, type=file_type)
                print(f'✅ （{index}/{SUM}）上传成功: {path}/{file_name}')
                break
            except Exception as e:
                print(f"❌ 上传失败 [{file_path}]: {e}")
                if attempt < 2:
                    print(f"🔄 重试第 {attempt + 1} 次...")
                    await asyncio.sleep(2)
                else:
                    print(f"❌ 最终上传失败 [{file_path}]")
    await Tortoise.close_connections()
async def downloaded(local_dir: str, path: str, file_list: Optional[List[str]] = None):
    os.makedirs(local_dir, exist_ok=True)
    if file_list:
        name_list = file_list
    else:
        records = await Pan.filter(path=path).all()
        name_list = [r.name for r in records]
    await Tortoise.init(config=PAN_TORTOISE_ORM )
    for name in name_list:
        output_path = os.path.join(local_dir, name)
        try:
            pan_record = await Pan.get(name=name, path=path)
            chunks = []
            for i in range(math.ceil(pan_record.size / (1024 * 1024))):
                data_record = await PanData.get(name=name, number=i)
                chunks.append(data_record.data)
            full_data = b''.join(chunks)
            with open(output_path, "wb") as f:
                f.write(full_data)
            print(f'✅ 下载成功: {output_path}')
        except Exception as e:
            print(f'❌ 下载失败 [{name}]: {e}')
            raise e
    await Tortoise.close_connections()
async def delete(path: str, file_list: List[str]):
    await Tortoise.init(config=PAN_TORTOISE_ORM)
    async def delete_file(file_name: str):
        try:
            pan_record = await Pan.get(name=file_name, path=path)
            await PanData.filter(name=file_name).delete()
            await pan_record.delete()
            print(f'✅ 删除成功: {path}/{file_name}')
        except Exception as e:
            print(f'❌ 删除失败 [{file_name}]: {e}')
    
    await asyncio.gather(*[delete_file(name) for name in file_list])
    await Tortoise.close_connections()

# 示例：本地测试
if __name__ == "__main__":
    async def demo():
        # 上传本地目录 ./upload 到云端路径 /test
        await sync("./upload", "/test")
        # 下载云端 /test 目录到本地 ./download
        await downloaded("./download", "/test")
        # 删除 /test 下的 test.txt
        await delete("/test", ["test.txt"])
    asyncio.run(demo())

