import os, json, pathlib
from qiniu import Auth, BucketManager
from qiniu import CdnManager
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
BUCKET_NAME = 'langoo'
ACCESS_KEY = "Ja0b2SmPIGOMcPi_Ha2--82hnTxcI6DYQsSmhOIh"
SECRET_KEY = "NuT0fLYpHblSK5W-jS6nNAUoydRJmtpgW_TfzWXH"
DOMAIN = 'https://t0ij3fnp2.hn-bkt.clouddn.com'
LOCAL_DIR = './downloads' 

auth = Auth(ACCESS_KEY, SECRET_KEY)
bucket = BucketManager(auth)

def list_all_keys():
    marker = None
    eof = False
    limit = 1000
    keys = []
    while not eof:
        ret, eof, _ = bucket.list(BUCKET_NAME, prefix=None, marker=marker, limit=limit)
        if ret is None:
            raise RuntimeError('list failed')
        keys.extend([item['key'] for item in ret.get('items', [])])
        marker = ret.get('marker')
    return keys

def download_one(key: str):
    """把单个文件下载到本地同名路径"""
    url = f'{DOMAIN}/{key}'
    print(f'downloading {url}')
    local_path = pathlib.Path(LOCAL_DIR) / key
    local_path.parent.mkdir(parents=True, exist_ok=True)
    if local_path.exists():
        resp = bucket.stat(BUCKET_NAME, key)
        if resp[0]['fsize'] == local_path.stat().st_size:
            return key, 'skipped'
    private_url = auth.private_download_url(url, expires=3600)
    os.system(f'curl -s -o "{local_path}" "{private_url}"')
    return key, 'downloaded'

if __name__ == '__main__':
    keys = list_all_keys()
    print(f'共 {len(keys)} 个文件待下载')
    for key in keys:
        download_one(key)

    # with ThreadPoolExecutor(max_workers=10) as pool, tqdm(total=len(keys)) as bar:
    #     futures = {pool.submit(download_one, k): k for k in keys}
    #     for f in as_completed(futures):
    #         key, status = f.result()
    #         bar.set_description(status)
    #         bar.update(1)