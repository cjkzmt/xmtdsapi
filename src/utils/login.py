from src.utils.Verification import Verification
import json
import requests
import tkinter as tk

def create_dialog(msg1, msg2,value,value2):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    dialog = tk.Toplevel(root)
    dialog.title("初始化设置")

    result = [None, None]

    label1 = tk.Label(dialog, text=msg1)
    label1.pack(pady=5)
    entry1 = tk.Entry(dialog, width=50)
    entry1.insert(0,value )  # 设置默认值
    entry1.pack(pady=5)

    label2 = tk.Label(dialog, text=msg2)
    label2.pack(pady=5)
    entry2 = tk.Entry(dialog, width=50)
    entry2.insert(0,value2)  # 设置默认值
    entry2.pack(pady=5)

    def submit():
        result[0] = entry1.get()
        result[1] = entry2.get()
        dialog.destroy()
        root.destroy()  # 关闭主窗口并结束事件循环

    submit_button = tk.Button(dialog, text="提交", command=submit)
    submit_button.pack(pady=10)

    dialog.mainloop()
    root.mainloop()

    return tuple(result)

def gethome(API_URL):
    url = API_URL + "/api"
    try:
        request = requests.get(url, timeout=5)
        request.raise_for_status()  # 抛出 HTTP 错误
        request_json = request.json()
        if request_json['mesg'] == "欢迎使用新媒体大师":
            return True
    except requests.exceptions.RequestException as e:
        print(f"网络请求失败: {e}")
    except ValueError:
        print("Error: Invalid JSON response")
    return False
def Verify(API_URL, id):
    url = API_URL + "/api/computer/Verify"
    uniqueid = Verification()
    data = {"id": int(id), "Verification": uniqueid}
    # 使用 json 参数代替 data 参数，确保发送的是 JSON 数据
    try:
        request = requests.post(url, json=data)
        if 'Internal Server Error'==request.text:
            request = requests.post(url, json=data)
        request_json = request.json()
        if isinstance(request_json.get('data'), str):
            # 如果 data 是字符串，则尝试解析为 JSON
            data_dict = json.loads(request_json['data'])
            return data_dict
        elif isinstance(request_json.get('data'), dict):
            # 如果 data 已经是字典，则直接返回
            return request_json['data']
        else:
            print("警告: 接口返回的 data 无法解析")
            return {}
    except ValueError:
        print("Error: Invalid JSON response")
    return None
def login(API_URL,PC_ID):
    if API_URL and PC_ID:
        if gethome(API_URL):
            print("链接服务器成功")
            request=Verify(API_URL,PC_ID)
            if request and 'access_token' in  request:
                print("登录成功")
                access_token=request['access_token']
                refresh_token=request['refresh_token']
                return API_URL,PC_ID,access_token,refresh_token
    msg1="请输入服务器地址:"
    msg2="请输入电脑ID:"
    value=API_URL or "http://0.0.0.0:8180"
    value2=PC_ID or 0
    while True:
        info=create_dialog(msg1,msg2,value,value2)
        if info[0] and info[1]:
            value=info[0]
            value2=info[1]
            if gethome(value):
                print("链接服务器成功")
                API_URL=value
                request=Verify(API_URL,value2)
                if 'access_token' in  request:
                    print("登录成功")
                    PC_ID=value2
                    access_token=request['access_token']
                    refresh_token=request['refresh_token']
                    break
                else:
                    msg2="登录失败，请检请输入电脑ID是否正确"
            else:
                msg1="请输入正确的服务器地址或确认服务器是否开启"
        else:
            print("请输入正确的服务器地址和电脑ID")
    return API_URL,PC_ID,access_token,refresh_token



if __name__ == "__main__":
    from KeyValue import Kv
    API_URL = Kv.get("API_URL","")
    PC_ID = Kv.get("PC_ID",0)
    API_URL,PC_ID,access_token,refresh_token=login(API_URL,PC_ID)
    Kv.save('API_URL',API_URL)
    Kv.save('PC_ID',PC_ID)
    Kv.save('access_token',access_token)
    Kv.save('refresh_token',refresh_token)
