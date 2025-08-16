import os
from typing import List, Optional
from qiniu import Auth, BucketManager, put_file, etag
import requests
# ---------- 配置 ----------
QINIU_ACCESS_KEY = os.getenv("QINIU_AK", "Ja0b2SmPIGOMcPi_Ha2--82hnTxcI6DYQsSmhOIh")
QINIU_SECRET_KEY = os.getenv("QINIU_SK", "NuT0fLYpHblSK5W-jS6nNAUoydRJmtpgW_TfzWXH")
QINIU_BUCKET     = os.getenv("QINIU_BUCKET", "lgej")
QINIU_DOMAIN     = os.getenv("QINIU_DOMAIN", "https://你的域名/")  # 用于生成外链，可选
# ---------------------------


auth   = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
bucket = BucketManager(auth)


def _etag_local(path: str) -> str: return etag(path)
def _exists_in_qiniu(key: str) -> bool:
    from qiniu import BucketManager
    bm = BucketManager(auth)
    ret, _ = bm.stat(QINIU_BUCKET, key)
    return ret is not None
def sync(local_dir: str, remote_prefix: str = "",file_list: Optional[List[str]] = None):
    local_dir = os.path.abspath(local_dir)
    if not os.path.isdir(local_dir):raise ValueError(f"本地目录不存在: {local_dir}")
    remote_prefix = remote_prefix.strip("/")
    if remote_prefix:remote_prefix += "/"
    if file_list:to_upload = [os.path.join(local_dir, f) for f in file_list]
    else:
        to_upload = [
            os.path.join(root, f)
            for root, _, files in os.walk(local_dir)
            for f in files]
    for local_path in to_upload:
        if not os.path.isfile(local_path):
            print(f"⚠️  跳过（非文件）: {local_path}")
            continue
        rel_path = os.path.relpath(local_path, local_dir).replace("\\", "/")
        key = remote_prefix + rel_path
        if _exists_in_qiniu(key) and _etag_local(local_path) == _etag_local(local_path):
            print(f"⏩  已存在，跳过: {key}")
            continue
        up_token = auth.upload_token(QINIU_BUCKET, key, 3600)
        ret, info = put_file(up_token, key, local_path, version='v2')
        assert ret['key'] == key
        assert ret['hash'] == etag(local_path)
        if ret is not None:
            print(f"✅  已上传: {local_path} -> {key}")
        else:
            print(f"❌  上传失败: {local_path}  {info}")

    print("同步完成 ✅")