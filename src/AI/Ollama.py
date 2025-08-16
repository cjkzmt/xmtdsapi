import requests
from src.api.ollama import getOllama,Updateollama,UpdateUrl
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util import Retry


def fetch_html(url: str, max_retries: int = 3, timeout: int = 10):
    """
    Fetch HTML content of a given URL with retry mechanism.
    Returns BeautifulSoup object or None on failure.
    """
    #print(f"[INFO] Fetching: {url}")
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
    }

    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=("HEAD", "GET"),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        resp = session.get(url, headers=headers, timeout=timeout)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except requests.RequestException as e:
        #print(f"[ERROR] Request failed: {e}")
        return None


def check_single_iteam(iteam):
    url = iteam['url']
    soup = fetch_html(f'http://{url}')
    #print(soup)
    if soup is not None:
        return True
    #print(f'{url} 网址不可用')
    data = {
        'id': iteam['urlId'],
        'isDel': True
    }
    UpdateUrl(data)
    return False












# def ollama(w,iteam,s=None):
#     try:
#         Url=iteam['url']
#         model=iteam['model']
#         # #print(f"{model}/{Url}")
#         url = f"http://{Url}/api/generate"
#         data = {
#             "model": model,
#             "prompt": w,
#             "stream": False if s is None else True,
#         }
#         response = requests.post(url, json=data, timeout=200)
#         return response.json()["response"]
#     except Exception as e:
#         #print(f'错误：：{Url}：{model}：{e}')
#         return None

def ollama(w, iteam, s=None):
    try:
        Url = iteam['url']
        model = iteam['model']
        url = f"http://{Url}/api/generate"
        data = {
            "model": model,
            "prompt": w,
            "stream": False if s is None else True,
        }
        response = requests.post(url, json=data, timeout=200)
        response.raise_for_status()  # 检查 HTTP 请求是否成功
        result = response.json()
        if 'response' in result:
            return result["response"]
        else:
            #print(f"Missing 'response' field in server response: {result}")
            return None
    except Exception as e:
        #print(f'错误：：{Url}：{model}：{e}')
        return None

def AI(w, model='qwen2.5:72b',max_retries=5):
    retries = 0
    while retries <= max_retries:
        data={'model': model,'Random':True,'status':'ENABLE'}
        ollama列表 = getOllama(data)['data']['records']
        if not ollama列表:
            print("没有可用ollama模型")
            exit()
        iteam=ollama列表[0]
        if check_single_iteam(iteam):
            # #print(f"使用ollama模型：{iteam}")
            答案 = ollama(w, iteam)
            if 答案 and 答案 !='服务器繁忙，请稍后再试。':return 答案
            #print(f"模型不可用，移除 {iteam['id']}")
            data={'id': iteam['id'],'status': 'DISABLE'}
            Updateollama(data)
            retries += 1
    #print("已达最大重试次数，未找到可用模型")
    return None


if __name__ == '__main__':
    t='''水的英文
    '''
    #print(AI(t))

