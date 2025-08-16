from DrissionPage import ChromiumPage, ChromiumOptions
import os
def signbrowser(datapath=None,port=None,browserpath=None,w=False):
    options = ChromiumOptions()
    options.mute(True)
    options.headless(w)
    options.set_argument('--start-maximized')
    if browserpath: options.set_browser_path(browserpath)
    if datapath and port is not None:
        data_path=os.path.join(datapath, str(port))
        os.makedirs(data_path, exist_ok=True)
        options.set_paths(local_port=(9999 - int(port)),user_data_path=data_path)
    page = ChromiumPage(addr_or_opts=options)
    return page

def signurl(page, url,cookie=None,wait=True):
    if page.url == url: return page
    try: tab_id = page.get_tab(url=url, as_id=True)
    except:
        def 域名(url): return url.replace('http://', '').replace('https://', '').split('/')[0]
        try: tab_id = page.get_tab(url=域名(url), as_id=True)
        except:
            if cookie: page.set.cookies(cookie)
            tab = page.new_tab(url)
            if wait:  tab.wait.load_start()
            return tab
    page.activate_tab(tab_id)
    tab = page.get_tab(tab_id)
    if tab.url == url: return tab
    tab.get(url)
    if wait:  tab.wait.load_start()
    return tab
def 网页文字(tab, txt):
    fb = []
    for i in tab.eles(txt):
        if i.text == txt:
            fb.append(i)
    return fb

def 文字点击(tab,txt,n=None):
    fb=网页文字(tab, txt)
    if fb : fb[0 if n==None else n].click()

def 双元素(tab,str,txt):
    dsj = tab.eles(str)
    for i in dsj:
        if i.text == txt: return i
            
def 双元点击(tab,str,txt):
    fb = 双元素(tab, str, txt)
    if fb is not None: fb.click()

def 按键(tab,key):
    tab.actions.key_down(key)
    tab.actions.key_up(key)

def 连键(tab,key,keys):
    tab.actions.key_down(key)
    for i in keys: tab.actions.type(i)
    tab.actions.key_up(key)

if __name__ == '__main__':
    pass
    # datapath=r'D:\XMTDS\Content\OtherContent\accounts'
    # tab=signbrowser(datapath,101)
    # tab.eles("@class=el-scrollbar__view el-time-spinner__list")[1].children()[int('00')].click()