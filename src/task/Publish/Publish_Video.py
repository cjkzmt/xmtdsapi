
import pyperclip
from datetime import datetime, timedelta
from  src.utils.browser import *
import re

发布语={
    "抖音":'tag:button@text()=发布',
    "小红书":'tag:span@@style=text-underline-offset: auto;@@text():发布',
    "视频号":'tag:button@text()=发表',
    "百家":'tag:span@text()=定时发布',
    "快手":'tag:div@text()=发布',
    'B站':'tag:span@text()=立即投稿'
}

上传节语={
    "抖音":("@class=phone-screen-iP9oLo","取消上传","重新上传",'点击上传','@@class=tag-inner@@text()=删除','@@type=button@@text()=删除','重新上传'),
    "小红书":("@class=media-area-new","取消上传","上传成功",'已取消','@@class=tag-inner@@text()=删除','@@type=button@@text()=删除','替换视频'),
    "视频号":("@class=post-media-preview-wrap","取消上传","评论",'网络出错，请重新上传','@@class=tag-inner@@text()=删除','@@type=button@@text()=删除'),
    "快手":('#preview-tours',"上传中","重新上传",'点击上传','@@class=tag-inner@@text()=删除','@@type=button@@text()=删除','预览封面预览作品',),
}

def 上传视频(tab,pt,视频路径):
    body = tab('tag:body')
    upload = body.ele('tag:input@type=file')
    if not upload:
        body =tab('.wujie_iframe').shadow_root
        upload = body.ele('tag:input@type=file')
    upload.input(视频路径)
    tab.wait(10)
    while True:
        上传节=body.ele(上传节语[pt][0])
        if 上传节:
            上传显示=上传节.text
            if 上传节语[pt][1] in 上传显示:# 上传中
                tab.wait(1)
            elif 上传节语[pt][2] in 上传显示:# 上传成功
                tab.wait(3)
                if pt == "视频号" and re.search(r'生成中|文件上传中', body.ele('@class=post-video-cover-wrap').text):
                    print('上传失败')
                    tab.refresh()
                else: break
            elif 上传节语[pt][3] in 上传显示:# 上传失败
                tab.refresh()
            else:# 上传
                upload = body.ele('tag:input@type=file')
                upload.input(视频路径)
                tab.wait(10)

def 发布(tab,pt):
    body = tab('tag:body')
    发布j=body.ele(发布语[pt])
    if not 发布j:
        body =tab('.wujie_iframe').shadow_root
    while body.ele(发布语[pt]):
        body.ele(发布语[pt]).click()
        tab.wait(3)
    print(f'{pt}发布成功~~')
    #tab.refresh()


标题节语={
    "抖音":('@class=semi-input semi-input-default',"@class=zone-container editor-kit-container editor editor-comp-publish notranslate chrome window chrome88"),
    "小红书":('tag:input@placeholder:标题','@data-placeholder:正文描述'),
    "视频号":(".input-editor",".input-editor"),
    "百家":('@class=input-box','@class=client_pages_edit_components_titleInput','tag:textarea@placeholder:标题','@placeholder:标题'),
    "快手":('#work-description-edit','@placeholder=添加合适的话题和描述，作品能获得更多推荐～'),
    "B站":('@placeholder=请输入稿件标题',"@placeholder=按回车键Enter创建标签"),}

def 写入标题(tab, Platform,btitle,atitle , character,keywords):
    body = tab('tag:body')
    标题节=body.ele(标题节语[Platform][0])
    if not 标题节:
        body =tab('.wujie_iframe').shadow_root
        标题节=body.ele(标题节语[Platform][0])
    标题节.click()
    标题节.clear()

    标题节.input(btitle)
    描述节 = body.ele(标题节语[Platform][1])
    if atitle:
        描述节.input(atitle + "  ")
    for gjc in keywords:
        描述节.input(f" #{gjc}\n")


def 抖音(tab,发布时间):
    同步节=tab('x://*[@id="root"]/div/div/div[2]/div[1]/div[12]/div[1]/div[2]/div[1]/div/label[2]/span')
    if 同步节:同步节.click()
    if 发布时间 > datetime.now() + timedelta(hours=2.5):
        文字点击(tab, "定时发布")
        fbsj = str(发布时间.strftime('%Y-%m-%d %H:%M'))
        pyperclip.copy(fbsj)
        sqhsj = tab('@placeholder=日期和时间')
        sqhsj.click()
        连键(tab,"CTRL",('a', 'v'))
        tab.wait(1)
    tab.wait(10)
def 小红书(tab, 发布时间):
    future_time = datetime.now() + timedelta(hours=2.5)
    if 发布时间 > future_time:
        while '发布'==tab('tag:button@data-v-34b0c0bc=').text:
            tab('定时发布').click(by_js=True)
        tab('tag:input@placeholder=选择日期和时间').click(by_js=True)
        if datetime.now().strftime('%Y%m%d') != 发布时间.strftime('%Y%m%d'):
            if datetime.now().strftime('%Y%m') != 发布时间.strftime('%Y%m'):
                tab('@aria-label=下个月').click()
            日=int(发布时间.strftime('%d'))
            i=tab.eles(f'@@class=el-date-table-cell__text@@text()={str(日)}')[-1 if int(日)>20 else 0]
            i.click()
        tab("@placeholder=选择时间").click()
        tab.eles("@class=el-scrollbar__view el-time-spinner__list")[0].children()[int(发布时间.strftime('%H'))].click()
        # print(发布时间.strftime('%H'))
        # print(发布时间.strftime('%M'))
        tab.wait(2)
        tab.eles("@class=el-scrollbar__view el-time-spinner__list")[1].children()[int(发布时间.strftime('%M'))].click()
        tab.wait(2)
        tab('@@class=el-time-panel__btn confirm@@text()=确定').click()
        tab.wait(2)
        tab('@@class=@@text()=确定').click()
        tab.wait(2)

def 视频号(tab, 发布时间):
    body = tab('tag:body')
    时间节=body.ele('@class=location-name')
    if not 时间节:
        body =tab('.wujie_iframe').shadow_root
        时间节=body.ele('@class=location-name')
    # 时间节.click()
    # body.ele('@text()=不显示位置').click()
    if 发布时间 > datetime.now() + timedelta(hours=2.5):
        body.ele('tag:span@text()=定时').click()
        # while tab('@@class=weui-desktop-picker__dd@@style=display: none;'):
        body.ele('@placeholder=请选择发表时间').click()
        if datetime.now().strftime('%Y%m%d') != 发布时间.strftime('%Y%m%d'):
            if datetime.now().strftime('%Y%m') != 发布时间.strftime('%Y%m'):
                body.ele('@class=weui-desktop-btn__icon weui-desktop-btn__icon__right').click()
            for i in body.eles(f'@@href=javascript:;@@class='):
                if i.text ==str(int(发布时间.strftime('%d'))):
                    i.click()
                    break
        body.ele("@placeholder=请选择时间").click()
        body.ele("@class=weui-desktop-picker__time__panel weui-desktop-picker__time__hour").children()[int(发布时间.strftime('%H'))].click()
        body.ele("@class=weui-desktop-picker__time__panel weui-desktop-picker__time__minute").children()[int(发布时间.strftime('%M'))].click()
        body.ele('tag:span@text()=定时').click()


def 快手(tab, 发布时间):
    future_time = datetime.now() + timedelta(hours=2.5)
    if 发布时间 > future_time:
        文字点击(tab, '定时发布')
        tab.ele("@class=ant-picker-input").click()
        if datetime.now().strftime('%Y%m') != 发布时间.strftime('%Y%m'):
            tab.ele('@class=ant-picker-next-icon').click()
        日期 = '@title=' + 发布时间.strftime('%Y-%m-%d')
        tab.ele(日期).click()
        时分=tab.eles('@class=ant-picker-time-panel-column')
        时分[0].child(int(发布时间.strftime('%H')) + 1).click()
        时分[1].child(int(发布时间.strftime('%M')) + 1).click()
        时分[2].child(1).click()
        tab.actions.key_down('ENTER')
    while 网页文字(tab, "上传成功")is None:
        print("等待上传")
        tab.wait(1)

def chooseTime(tab,Platform, publishtime):
    平台 = {
        '抖音':抖音,
        '小红书':小红书,
        '视频号':视频号,
        '快手':快手}
    平台[Platform](tab, publishtime)



