import json
def getSparkToken(tab):
    cookies = tab.cookies()
    ticket_cookies = [cookie.get('value') for cookie in cookies 
                   if cookie.get('name') == 'ssoSessionId']
    return ticket_cookies[0]
def getStepToken(tab):
    deviceId=tab.local_storage().get('deviceId')[1:-1]
    cookies = tab.cookies()
    ticket_cookies = [cookie.get('value') for cookie in cookies 
                     if cookie.get('name') == 'Oasis-Token']
    return f'{deviceId}@{ticket_cookies[0]}'
def getQwenToken(tab):
    cookies = tab.cookies()
    ticket_cookies = [cookie.get('value') for cookie in cookies 
                     if cookie.get('name') == 'tongyi_sso_ticket']
    return ticket_cookies[0] if ticket_cookies else None
def getKimiToken(tab):
    return tab.local_storage().get('refresh_token')
def getminimaxToken(tab):
    return tab.local_storage().get('_token')
def getdeepseekToken(tab):
    user_token = tab.local_storage().get('userToken')
    if isinstance(user_token, str):
        # 如果是字符串，先解析为字典
        user_token_dict = json.loads(user_token)
        return user_token_dict.get('value')
    elif isinstance(user_token, dict):
        # 如果已经是字典，直接获取value
        return user_token.get('value')
    else:
        # 其他情况直接返回
        return user_token

def getToken(tab,name):
    app={'spark':getSparkToken,'step':getStepToken,'qwen':getQwenToken,'kimi':getKimiToken,'minimax':getminimaxToken,'deepseek':getdeepseekToken}
    return app[name](tab)
