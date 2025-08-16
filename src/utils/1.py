from qiniu import Auth, BucketManager
import requests

# 配置七牛云密钥信息
ACCESS_KEY = "Ja0b2SmPIGOMcPi_Ha2--82hnTxcI6DYQsSmhOIh"
SECRET_KEY = "NuT0fLYpHblSK5W-jS6nNAUoydRJmtpgW_TfzWXH"
DOMAIN = 'http://t0ij3fnp2.hn-bkt.clouddn.com'
BUCKET_NAME = 'langoo'

# 初始化认证对象
q = Auth(ACCESS_KEY, SECRET_KEY)

def download_file(file_key, local_path):
    """
    下载七牛云私有空间文件到本地
    :param file_key: 文件在存储空间中的key（文件名）
    :param local_path: 本地保存路径（包含文件名）
    """
    try:
        # 生成私有下载链接（有效期1小时）
        base_url = f'{DOMAIN}/{file_key}'
        private_url = q.private_download_url(base_url, expires=3600)
        
        # 发起下载请求
        response = requests.get(private_url)
        
        # 检查响应状态
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"文件下载成功！保存路径: {local_path}")
            return True
        else:
            print(f"下载失败，HTTP状态码: {response.status_code}")
            print(f"响应内容: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"下载过程中发生错误: {str(e)}")
        return False

# 示例用法
if __name__ == "__main__":
    # 需要下载的文件名（在七牛云中的key）
    file_key = "Music/忙碌的生活人山人海.MP3"  # 替换为实际文件名
    
    # 本地保存路径
    local_file = "./忙碌的生活人山人海.MP3"  # 替换为本地路径
    
    # 执行下载
    download_file(file_key, local_file)
