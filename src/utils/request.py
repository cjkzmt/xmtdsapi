import requests
from requests.exceptions import HTTPError,Timeout
from src.utils.KeyValue import Kv
import json
from time import sleep
from src.utils.login import login

# 模拟刷新令牌的函数
def RefreshToken():
    API_URL = Kv.get("API_URL", "")
    refresh_token = Kv.get("refresh_token", "")
    url = API_URL + "/api/user/refresh_token?refreshtoken=" + refresh_token
    try:
        response = requests.post(url)
        response_json = response.json()
        # 检查是否有 content 字段，并作为 data 使用
        data = response_json.get('content')  # 修改字段名从 'data' 到 'content'
        if isinstance(data, str):
            # 如果 data 是字符串，则尝试解析为 JSON
            data_dict = json.loads(data)
            return data_dict
        elif isinstance(data, dict):
            # 如果 data 已经是字典，则直接返回
            return data
        else:
            print("警告: 接口返回的 data 无法解析")
            return {}
    except ValueError:
        print("Error: Invalid JSON response")
        return None

def get_token():
    access_token = Kv.get("access_token", "")
    if access_token:
        return access_token
    redirect_to_login()
    return Kv.get("access_token", "")

# 模拟路由跳转函数
def redirect_to_login():
    API_URL = Kv.get("API_URL", "")
    PC_ID = Kv.get("PC_ID", 0)
    API_URL, PC_ID, access_token, refresh_token = login(API_URL, PC_ID)
    Kv.save('API_URL', API_URL)
    Kv.save('PC_ID', PC_ID)
    Kv.save('access_token', access_token)
    Kv.save('refresh_token', refresh_token)

class Request:
    def __init__(self, method, url, data=None,params=None):
        self.method = method
        self.url = url
        self.data = data
        self.params = data

def request(request_obj, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            API_URL = Kv.get("API_URL", "")
            url = API_URL + request_obj.url
            kwargs = {}
            if request_obj.data:
                kwargs['json'] = request_obj.data

            # 请求拦截器
            if 'headers' not in kwargs:
                kwargs['headers'] = {}
            token = get_token()
            # print(token)
            if token:
                kwargs['headers']['Authorization'] = token
        
            response = requests.request(request_obj.method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except Timeout:
            print("请求超时，正在重试...")
            redirect_to_login()
        except HTTPError as e:
            status_code = e.response.status_code
            if status_code == 500:
                print("服务器错误，正在重试...")
                retries += 1
                sleep(1)
            elif status_code == 401:
                # print("Token 过期，正在刷新...")
                try:
                    request=RefreshToken()
                    if 'access_token' in  request:
                        Kv.save('access_token', request['access_token'])
                        Kv.save('refresh_token', request['refresh_token'])
                        # print("刷新令牌成功"+request['access_token'])
                except Exception as e:
                    print(f"刷新令牌失败: {e}")
                    return None  # 退出重试
            elif status_code == 403:
                return {'data': {'code': '123456'}}
            else:
                raise
    
    print("请求失败，达到最大重试次数")
    return None
