# list_all_files.py
from qiniu import Auth, BucketManager

# ===== 1. 填写你的七牛云凭证 =====
ACCESS_KEY = "Ja0b2SmPIGOMcPi_Ha2--82hnTxcI6DYQsSmhOIh"
SECRET_KEY = "NuT0fLYpHblSK5W-jS6nNAUoydRJmtpgW_TfzWXH"
DOMAIN = 'http://t0ij3fnp2.hn-bkt.clouddn.com' 
BUCKET_NAME = 'langoo'

# ===== 2. 初始化 =====
auth = Auth(ACCESS_KEY, SECRET_KEY)
bucket = BucketManager(auth)

# ===== 3. 获取全部文件 =====
marker = None   # 翻页游标
eof = False     # 结束标志
limit = 1000    # 每批最多 1000 条

all_files = []

while not eof:
    ret, eof, info = bucket.list(BUCKET_NAME, prefix=None, marker=marker, limit=limit)
    # 可选：如果只想拉取某个目录，可把 prefix 设为 'dir1/'
    if ret is None:
        raise RuntimeError(f"list failed: {info}")
    items = ret.get('items', [])
    for item in items:
        all_files.append({
            'key':     item['key'],
            'hash':    item['hash'],
            'fsize':   item['fsize'],
            'mime':    item['mimeType'],
            'putTime': item['putTime']      # 13 位时间戳
        })
    marker = ret.get('marker', None)   # 继续翻页

# ===== 4. 打印/使用结果 =====
print(f"共 {len(all_files)} 个文件")
for f in all_files:
    print(f)

# 如果需要保存为 JSON
import json, pathlib
pathlib.Path('all_files.json').write_text(json.dumps(all_files, ensure_ascii=False, indent=2))