from tortoise.models import Model
from tortoise import fields
'''
cd be       
python -m aerich init -t settings.TORTOISE_ORM
python -m aerich init-db
aerich migrate 
aerich upgrade
python -m aerich migrate
python -m aerich upgrade
'''
class Time(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, description="名字")
    time = fields.DatetimeField( null=True,default=None, description="开始创建时间")
    createdTime = fields.DatetimeField(auto_now_add=True, description="开始创建时间")

class User(Model):#操作用户
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, index=True, description="用户名")
    password = fields.CharField(max_length=32,default="123456", description="密码")
    phone=fields.CharField(max_length=32, null=True,default=None,description="电话号码")
    number = fields.CharField(max_length=32,null=True,default=None, description="编号")
    portrait=fields.CharField(max_length=255,null=True,default=None, description="头像")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")
    regIp=fields.CharField(max_length=255, null=True,default=None, description="注册IP")
    createdTime = fields.DatetimeField(auto_now_add=True, description="开始创建时间")
    endCreateTime=fields.DatetimeField(null=True,default=None, description="结束创建时间")
    isDel=fields.BooleanField(default=False)

class TypeText (Model):#文案类型
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="文案类型名", unique=True)
    description = fields.CharField(max_length=255, description="类型描述")
    topicSW = fields.CharField(max_length=32, default="ENABLE", description="选题开关")
    copySW = fields.CharField(max_length=32, default="ENABLE", description="样本开关")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    
class PromptText(Model):#提示词文案
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=760,description="提示词", unique=True) 
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    
class TopicCopy(Model):
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=760,null=True,default=None,description="文案", unique=True)
    url = fields.CharField(max_length=64,null=True,default=None, description="链接")
    Author= fields.ForeignKeyField("models.Author",null=True, default=None, related_name="topiccopy_author", description="作者")
    TypeText = fields.ForeignKeyField("models.TypeText",null=True,default=None,related_name="topiccopy_typetexts",description="文案类型")
    topicnum=fields.IntField(default=0,description="选题数")
    copynum=fields.IntField(default=0,description="样本数")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Platform(Model):#新媒体平台名
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="新媒体平台名", unique=True)
    English=fields.CharField(max_length=255,null=True, default=None, description="英文名")
    sort = fields.IntField(default=0, description="排序")
    publish=fields.CharField(max_length=32, default="DISABLE", description="状态")
    loginurl = fields.CharField(max_length=255, null=True, default=None, description="登录地址")
    publishurl=fields.CharField(max_length=255,null=True, default=None, description="发布链接")
    Scrapeurl=fields.CharField(max_length=255,null=True, default=None, description="采集链接")
    character= fields.IntField(default=10, description="标题字数")
    keycount= fields.IntField(default=5, description="关键词数")
    verification=fields.CharField(max_length=32,null=True, default=None, description="验证信息")
    publishverif=fields.CharField(max_length=255,null=True, default=None, description="验证链接")
    advance=fields.IntField(default=13, description="预先发布天数")

class Author(Model):#作者
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="作者名字")
    number = fields.CharField(max_length=255,null=True, default=None,description="作者号", unique=True)
    url = fields.CharField(max_length=255, description="链接")
    urlnum = fields.IntField(default=0, description="链接数量")
    Platform =  fields.ForeignKeyField("models.Platform", related_name="authors", description="关联的新媒体平台")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class VideoTemplate(Model):#视频模板
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="模板名", unique=True)
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期") 

class Font(Model):
    id = fields.IntField(pk=True) 
    name = fields.CharField(max_length=255, description="字体名", unique=True)
    url=fields.CharField(max_length=255,null=True, default=None, description="字体路径")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Music(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="音乐名", unique=True)
    duration=fields.IntField(null=True, default=None,description="Music")
    url=fields.CharField(max_length=255,null=True, default=None, description="音乐路径")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Over(Model):#配音
    id = fields.IntField(pk=True)
    name = fields.CharField(null=True, default=None,max_length=255, description="配音名")
    filename= fields.CharField(max_length=255, description="配音文件名", unique=True)
    sex = fields.CharField(max_length=32,null=True, default=None, description="性别")
    speed = fields.FloatField(null=True, default=1.2, description="语速")
    url=fields.CharField(max_length=255,null=True, default=None, description="配音路径")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    
class VideoClips (Model):#视频片段
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="素材名", unique=True)
    clipsum = fields.IntField(description="片段数量")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    updatedTime = fields.DatetimeField(auto_now=True, description="更新日期")

class Menu(Model):  # 菜单
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="菜单名")
    description = fields.CharField(max_length=255,null=True, default=None, description="描述")
    href = fields.CharField(max_length=255,null=True, default=None, description="链接")
    icon = fields.CharField(max_length=255,null=True, default=None, description="图标")
    level = fields.IntField(default=0,description="菜单等级")
    orderNum = fields.IntField(default=0, description="排序")
    show = fields.BooleanField(default=True, description="是否显示")
    parent_id = fields.IntField(null=True, default=None, description="父级菜单")  
    createdBy = fields.ForeignKeyField("models.User", related_name="createdby", description="创建人")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    operator = fields.ForeignKeyField("models.User",null=True, default=None,  related_name="operator", description="操作人")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")

class ResourceCategory(Model):  #资源类别
    id= fields.IntField(pk=True)
    name= fields.CharField(max_length=255, description="资源类别名")
    selected =  fields.BooleanField(default=True, description="是否选中")
    sort = fields.IntField(default=0, description="排序")
    createdBy = fields.ForeignKeyField("models.User", related_name="resource_createdby", description="创建人")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    operator = fields.ForeignKeyField("models.User",null=True, default=None,  related_name="resource_operator", description="操作人")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")

class ReleasePlan(Model):#发布计划
    id = fields.IntField(pk=True)
    hour= fields.IntField(default=0, description="小时")
    minute= fields.IntField(default=0,description="分钟")

class SystemInfo(Model):#系统信息
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="名称", unique=True)
    value = fields.CharField(max_length=255, description="值")
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")

class Phone(Model): #手机
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="手机编号")
    Model= fields.CharField(max_length=255,default=None, null=True, description="手机型号")
    Brand= fields.CharField(max_length=255,default=None, null=True, description="品牌名")
    Owner= fields.CharField(max_length=255,default=None, null=True, description="手机所有人")
    sort = fields.IntField(default=0, description="排序")
    Verification= fields.CharField(max_length=255,default=None, null=True, description="设备id", unique=True)
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Keyword(Model): #关键词
    id = fields.IntField(pk=True)
    text = fields.CharField(max_length=16, description="关键词")
    sort = fields.IntField(default=0, description="排序")

class Computer(Model):#电脑
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="计算机名")
    Verification=fields.CharField(max_length=255,default=None, null=True, description="唯一标识", unique=True)
    createtext= fields.CharField(max_length=32, default="DISABLE", description="制作文案")
    createvideo= fields.CharField(max_length=32, default="DISABLE", description="制作视频")
    createclip= fields.CharField(max_length=32, default="DISABLE", description="制作素材")
    publishvideo= fields.CharField(max_length=32, default="DISABLE", description="发布视频")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期") 
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class PNumber(Model):#手机号码
    id = fields.IntField(pk=True)
    number = fields.BigIntField(description="手机号码", unique=True)
    code=fields.IntField(default=None, null=True,  description="编号")
    rent = fields.IntField(default=None, null=True,  description="月租")
    Owner =  fields.CharField(max_length=32, default=None, null=True, description="所有人")
    createdTime = fields.DatetimeField(auto_now_add=True, description="创建日期")
    Phone=fields.ForeignKeyField("models.Phone",default=None, null=True,  related_name="phone_number", description="所在手机")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Certifier (Model): #认证人
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="认证人名字")
    idnumber = fields.CharField(max_length=255,default=None, null=True, description="身份证号", unique=True)
    Owner =  fields.CharField(max_length=32, default=None, null=True, description="所有人")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="创建日期")
 
class TypeVideo(Model):#视频样式
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频样式名")
    videoheight= fields.IntField(default=1280, description="视频高度")
    videowidth= fields.IntField(default=720, description="视频宽度")

class TypeCover(Model):#封面样式
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="封面样式名")
    fixedtitle= fields.CharField(max_length=255, default=None, null=True, description="固定标题")

class TypeSubtitle(Model):#字幕样式
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="字幕样式名")
    fontsize= fields.IntField(default=1280, description="字幕字号")
    fontcolor= fields.CharField(max_length=32, description="字幕字色")

class TeamOwner(Model):#团队拥有者
    id = fields.IntField(pk=True)
    shorthand=fields.CharField(max_length=32, default=None, null=True, description="简称")
    name = fields.CharField(max_length=65, default=None, null=True, description="账号拥有者")
    alias=fields.CharField(max_length=128, default=None, null=True, description="别名")
    Title=fields.CharField(max_length=65, default=None, null=True, description="称号")
    number = fields.BigIntField(description="手机号码", default=None, null=True, unique=True)
    email=fields.CharField(max_length=255, default=None, null=True, description="邮箱")
    scope=fields.CharField(max_length=255, default=None, null=True, description="业务范围")
    path=fields.CharField(max_length=255, default=None, null=True, description="文件名")
    clipSum=fields.IntField(default=0, description="素材数量")
    address=fields.CharField(max_length=255, default=None, null=True, description="地址")
    note=fields.CharField(max_length=400, default=None, null=True, description="备注")
    status=fields.CharField(max_length=32, default="DISABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="创建日期")
    sort = fields.IntField(default=0, description="排序")

class AccountTeam(Model):
    id = fields.IntField(pk=True)
    number = fields.IntField(description="组号", unique=True)
    TeamOwner=fields.ForeignKeyField("models.TeamOwner", related_name="team_owner",description="团队拥有者", on_delete=fields.CASCADE)
    Phone=fields.ForeignKeyField("models.Phone",default=None, null=True,  related_name="team_phone", description="所在手机")
    Computer=fields.ForeignKeyField("models.Computer",default=None, null=True,  related_name="team_computer", description="所在电脑")
    createdTime = fields.DatetimeField(auto_now_add=True, description="制作日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    TypeVideo=fields.ForeignKeyField("models.TypeVideo",default=None, null=True,  related_name="team_typevideo", description="所在视频样式")
    TypeCover=fields.ForeignKeyField("models.TypeCover",default=None, null=True,  related_name="team_typecover", description="所在封面样式")
    TypeSubtitle=fields.ForeignKeyField("models.TypeSubtitle",default=None, null=True,  related_name="team_typesubtitle", description="所在字幕样式")

class Account(Model):
    id = fields.IntField(pk=True)
    AccountTeam=fields.ForeignKeyField("models.AccountTeam", related_name="team_account", description="所在组", on_delete=fields.CASCADE)
    Platform = fields.ForeignKeyField("models.Platform", related_name="accounts", description="新媒体平台")
    name = fields.CharField(max_length=255, default=None, null=True, description="名字")
    number = fields.CharField(max_length=255, default=None, null=True, description="账号ID")
    InitFans=fields.IntField(default=None, description="初始粉丝数")
    newFans=fields.IntField(default=None, description="当前粉丝数")
    isDel=fields.BooleanField(default=False)
    password = fields.CharField(max_length=128, null=True, default=None, description="密码")
    profile = fields.CharField(max_length=255, default=None, null=True, description="简介")
    PNumber = fields.ForeignKeyField("models.PNumber", related_name="accounts_pnumber", default=None, null=True, description="手机号码")
    Certifier = fields.ForeignKeyField("models.Certifier", related_name="accounts_certifier", default=None, null=True, description="认证人")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    note=fields.CharField(max_length=225, default="", description="备注")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")

class AiApi(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, description="名称")
    description=fields.CharField(max_length=225, default="", description="描述")
    url=fields.CharField(max_length=225,default=None, null=True, description="官网")
    port=fields.IntField(default=None, null=True,description="端口")
    model=fields.CharField(max_length=32, default=None, null=True, description="模型")
    note=fields.CharField(max_length=225, default=None, null=True, description="备注")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")

class ApiToken(Model):
    id = fields.IntField(pk=True)
    AiApi=fields.ForeignKeyField("models.AiApi", related_name="api_api", default=None, null=True, on_delete=fields.CASCADE, description="Ai")
    PNumber=fields.ForeignKeyField("models.PNumber", related_name="api_pnumber", default=None, null=True, description="电话号码")
    token = fields.CharField(max_length=1024, default=None, null=True, description="token") 
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")

class OllamaUrl(Model):
    id = fields.IntField(pk=True)
    url=fields.CharField(max_length=32, default=None, null=True, description="地址", unique=True)
    status = fields.CharField(max_length=64, default="DISABLE", description="状态")
    isDel=fields.BooleanField(default=False)

class OllamaModel(Model):
    id = fields.IntField(pk=True)
    OllamaUrl=fields.ForeignKeyField("models.OllamaUrl", related_name="ollama_ollamaurl", description="ollama地址", on_delete=fields.CASCADE)
    model=fields.CharField(max_length=128, default=None, null=True, description="模型")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Script(Model):#视频脚本
    id = fields.IntField(pk=True)
    topic=fields.ForeignKeyField("models.TopicCopy",null=True, default=None, related_name="script_topic", description="选题", on_delete=fields.CASCADE)
    copy=fields.ForeignKeyField("models.TopicCopy",null=True, default=None, related_name="script_tcopy", description="样本", on_delete=fields.CASCADE)
    AccountTeam=fields.ForeignKeyField("models.AccountTeam",null=True, default=None, related_name="script_accountteam", description="发布账号组", on_delete=fields.CASCADE)
    PromptText=fields.ForeignKeyField("models.PromptText",null=True, default=None, related_name="script_prompttext", description="提示语", on_delete=fields.CASCADE)
    ReleasePlan= fields.ForeignKeyField("models.ReleasePlan", related_name="task_plan", default=None, null=True, description="发布计划")
    publishtime = fields.DatetimeField(default=None, null=True, description="发布日期")
    Music=  fields.ForeignKeyField("models.Music",null=True, default=None, related_name="scripts_music", description="视频背景音乐", on_delete=fields.CASCADE)
    Over= fields.ForeignKeyField("models.Over",null=True, default=None, related_name="scripts_Over", description="视频配音", on_delete=fields.CASCADE)
    Font = fields.ForeignKeyField("models.Font",null=True, default=None, related_name="scripts_font", description="视频字体", on_delete=fields.CASCADE)
    VideoTemplate = fields.ForeignKeyField("models.VideoTemplate",null=True, default=None, related_name="script_videotemplate", description="预设模板")
    videopath = fields.CharField(max_length=64,default=None, null=True, description="视频文件路径")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    linestatus = fields.CharField(max_length=16,null=True, default=None,description="脚本状态")
    copystatus = fields.CharField(max_length=16,null=True, default=None,description="视频文案状态")
    videostatus = fields.CharField(max_length=16,null=True, default=None,description="视频状态")
    operator = fields.ForeignKeyField("models.User",null=True, default=None,  related_name="scripts_operator", description="操作人")
    drafline=fields.TextField(null=True, default=None, description="文案初稿")
    line = fields.CharField(max_length=760,null=True, default=None,description="脚本文案", unique=True)
    draftitle = fields.TextField(null=True, default=None,description="描述初稿")
    title = fields.TextField(null=True, default=None,description="标题描述")
    drafcover = fields.TextField(null=True, default=None, description="封面初稿")
    cover = fields.TextField(null=True, default=None, description="封面文案")
    visual = fields.TextField(null=True, default=None,description="画面文案")
    subtitle = fields.TextField(null=True, default=None,description="显示字幕")
    reading = fields.TextField(null=True, default=None,description="字幕读音")
    videoname = fields.CharField(max_length=64,default=None, null=True, description="视频文件名")
    status = fields.CharField(max_length=32, default="脚本文案待制作", description="状态")
    Computer = fields.ForeignKeyField("models.Computer",null=True, default=None, related_name="script_computer", description="操作电脑")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")

class Data(Model):#抖音数据
    id = fields.IntField(pk=True)
    Script = fields.ForeignKeyField("models.Script", related_name="data_script", default=None, null=True, description="视频脚本",on_delete=fields.CASCADE)
    Account= fields.ForeignKeyField("models.Account", related_name="data_account", default=None, null=True, description="发布账号")
    status = fields.CharField(max_length=16, default="DISABLE", description="状态")
    title = fields.CharField(max_length=252, default=None, null=True, description="作品,作品名称,视频描述,笔记标题")
    publishtime = fields.CharField(max_length=60, default=None, null=True,description="首次发布时间")
    views = fields.IntField(default=0, description="播放量,观看量")
    completion = fields.IntField(default=0, description="完播率")
    comment =  fields.IntField(default=0, description="评论量")
    like = fields.IntField(default=0, description="点赞量,喜欢")
    fav = fields.IntField(default=0, description="收藏量,推荐")
    followers = fields.IntField(default=0, description="粉丝增量,涨粉量,关注量")
    share = fields.IntField(default=0, description="分享量")
    watch = fields.IntField(default=0, description="平均播放时长,人均观看时长")
    # 体裁=fields.CharField(max_length=255, description="体裁")
    # 审核状态=fields.CharField(max_length=255, description="审核状态")
    # 完播率5s=fields.CharField(max_length=255, description="完播率5s")
    # 封面点击率=fields.CharField(max_length=255, description="封面点击率")
    # 跳出率2s=fields.CharField(max_length=255, description="跳出率2s")
    # 主页访问量=fields.CharField(max_length=255, description="主页访问量")
    # update = fields.DatetimeField(auto_now_add=True, description="更新日期")
    # 视频ID = fields.CharField(max_length=255, description="视频ID")
    # 转发聊天和朋友圈=fields.CharField(max_length=255, description="转发聊天和朋友圈")
    # 设为铃声 = fields.CharField(max_length=255, description="设为铃声")
    # 设为状态 = fields.CharField(max_length=255, description="设为状态")
    # 设为朋友圈封面 = fields.CharField(max_length=255, description="设为朋友圈封面")
    # 弹幕=fields.CharField(max_length=255, description="弹幕")




#     
# class UrlVDKey(Model):#视频采集链接
#     id = fields.IntField(pk=True)
#     url = fields.CharField(max_length=255, description="链接")
#     key = fields.CharField(max_length=255, description="关键词")
#     update = fields.DatetimeField(auto_now_add=True, description="录入日期")
#     
#     status = fields.CharField(max_length=32, default="Unfinished", description="状态")
#     User =fields.ForeignKeyField("models.User", related_name="urlvdkeys", description="录入人")
# class UrlVD (Model):#视频下载链接
#     id = fields.IntField(pk=True)
#     url = fields.CharField(max_length=255, description="链接")
#     name = fields.CharField(max_length=255, description="视频标题")
#     Author= fields.ForeignKeyField("models.Author", related_name="urlvds", description="作者")
#     views=fields.CharField(max_length=255, description="浏览量")
#     duration=fields.CharField(max_length=255, description="时长")
#     uploaddate = fields.CharField(max_length=255, description="上传时间")
#     update = fields.DatetimeField(auto_now_add=True, description="录入日期")
#     
#     status = fields.CharField(max_length=32, default="待下载", description="状态")
#     UrlVDKey =fields.ForeignKeyField("models.UrlVDKey", null=True,related_name="urlvds", description="关键词链接")
# class Footage(Model):#视频素材
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255, description="视频文件名")
#     path = fields.CharField(max_length=255, description="视频文件路径")
#     update = fields.DatetimeField(auto_now_add=True, description="下载日期")
#     
#     status = fields.CharField(max_length=32, default="Unfinished", description="状态")
#     UrlVD=fields.ForeignKeyField("models.UrlVD",null=True, related_name="footages", description="素材链接")
# class TrimVideo(Model):#视频分割片段
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255, description="视频文件名")
#     path = fields.CharField(max_length=255, description="视频文件路径")
#     update = fields.DatetimeField(auto_now_add=True, description="分割日期")
#     Footage=fields.ForeignKeyField("models.Footage", related_name="trimvideos", description="原始素材")
#     
#     status = fields.CharField(max_length=32, default="待裁剪", description="状态")
# class VideoCategory(Model):#视频类型
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255, description="视频分类名")
#     update = fields.DatetimeField(auto_now_add=True, description="录入日期")
#     
#     status = fields.CharField(max_length=32, default="ENABLE", description="状态")
# class CutVideo(Model):#视频裁剪片段
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255, description="视频文件名")
#     path = fields.CharField(max_length=255, description="视频文件路径")
#     update = fields.DatetimeField(auto_now_add=True, description="裁剪日期")
#     
#     status = fields.CharField(max_length=32, default="Unfinished", description="状态")
#     TrimVideo=fields.ForeignKeyField("models.TrimVideo", related_name="cutvideos", description="分割素材")
#     VideoCategory=fields.ForeignKeyField("models.VideoCategory", null=True, related_name="cutvideos", description="视频分类")
# class MirrorVideo(Model):#视频镜像片段
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255, description="视频分类名")
#     update = fields.DatetimeField(auto_now_add=True, description="录入日期")
#     
#     CutVideo=fields.ForeignKeyField("models.CutVideo", related_name="mirrorvideos", description="裁剪素材")
#     status = fields.CharField(max_length=32, default="待使用", description="状态")

    
#用户信息=============================================
# class Fans(Model):#粉丝
#     id = fields.IntField(pk=True)
#     number = fields.CharField(max_length=255,default=None, null=True,  description="号")
#     name = fields.CharField(max_length=255, description="名")
#     profile = fields.CharField(max_length=255,default=None, null=True, description="简介")
#     Sex= fields.CharField(max_length=255,default=None, null=True, description="性别")
#     Position=  fields.CharField(max_length=255,default=None, null=True, description="位置")
#     Account= fields.ManyToManyField("models.Account",default=None, null=True, related_name="fans_account", description="账号")
#     Video = fields.ManyToManyField("models.Video",default=None, null=True, related_name="fanss_video",description="视频")
#     createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
#     fansdate = fields.DatetimeField(default=None, null=True, description="关注日期")
#     Status= fields.CharField(max_length=32, default="ENABLE", description="状态")
    # updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")
#意向用户========================================================================
# class Lead(Model):#意向用户 
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255,default=None, null=True,  description="名")
#     contact= fields.CharField(max_length=255, default=None, null=True, description="手机号码")
#     wxnumber = fields.CharField(max_length=255,default=None, null=True,  description="微信号")
#     profile = fields.CharField(max_length=255,default=None, null=True, description="简介")
#     Sex= fields.CharField(max_length=255,default=None, null=True, description="性别")
#     Position=  fields.CharField(max_length=255,default=None, null=True, description="位置")
#     Fans = fields.ForeignKeyField("models.Fans",default=None, null=True, related_name="leads", description="粉丝")
#     status = fields.CharField(max_length=32, default="ENABLE", description="状态")
#     createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    # updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")

# class Payment(Model):#缴费记录
#     id = fields.IntField(pk=True)
#     amount = fields.IntField(description="金额")
#     PNumber=fields.ForeignKeyField("models.PNumber", related_name="payments", description="手机号码")
#     update = fields.DatetimeField(auto_now_add=True, description="录入日期")
#     status = fields.CharField(max_length=32, default="ENABLE", description="状态")
# # 账号内信息==================================================================================

# class Message(Model):#对话
#     id = fields.IntField(pk=True)
#     content = fields.CharField(max_length=255, description="内容")
#     date = fields.DatetimeField(description="日期")
#     Fans = fields.ForeignKeyField("models.Fans", related_name="messages", description="粉丝")
#     Account = fields.ForeignKeyField("models.Account", related_name="messages", description="账号")
#     status = fields.CharField(max_length=32, default="success", description="状态")
#     note = fields.CharField(max_length=255,null=True, default=None, description="备注")
# class Like(Model):#点赞
#     id = fields.IntField(pk=True)
#     Fans = fields.ForeignKeyField("models.Fans", related_name="likes", description="粉丝")
#     UploadVideo= fields.ForeignKeyField("models.Video", related_name="likes", description="视频")
#     date = fields.DatetimeField(auto_now_add=True, description="点赞时间")
# class Collect(Model):#收藏
#     id = fields.IntField(pk=True)
#     Fans = fields.ForeignKeyField("models.Fans", related_name="collects", description="粉丝")
#     UploadVideo= fields.ForeignKeyField("models.Video", related_name="collects", description="视频")
#     date = fields.DatetimeField(auto_now_add=True, description="收藏时间")
# class Comment(Model):#评论
#     id = fields.IntField(pk=True)
#     content = fields.CharField(max_length=255, description="内容")
#     Fans = fields.ForeignKeyField("models.Fans", related_name="comments", description="粉丝")
#     UploadVideo= fields.ForeignKeyField("models.Video", related_name="comments", description="视频")
#     date = fields.DatetimeField(auto_now_add=True, description="评论时间")



    
    
    
    






