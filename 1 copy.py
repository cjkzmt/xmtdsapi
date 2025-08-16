
from src.utils.browser import *

accountspath=r'D:\XMTDS\Content\OtherContent\accounts'

tab = signbrowser(accountspath,101)
nanme=tab("@class=account-name").text
number=tab("小红书账号:").text.replace("小红书账号:","")
print(f'✅ 小红书 账号:{nanme} 账号:{number}')