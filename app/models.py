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
    name = fields.CharField(max_length=255, description="文案类型名")
    description = fields.CharField(max_length=255, description="类型描述")
    topicSW = fields.CharField(max_length=32, default="ENABLE", description="选题开关")
    copySW = fields.CharField(max_length=32, default="ENABLE", description="样本开关")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    
class PromptText(Model):#提示词文案
    id = fields.IntField(pk=True)
    text = fields.TextField(description="提示词") 
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class UrlText(Model):#文案链接
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, description="链接")
    Author= fields.ForeignKeyField("models.Author",null=True, default=None, related_name="urltexts", description="作者")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="Unfinished", description="状态")

class TopicCopy(Model):
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="编号")
    text = fields.TextField(description="文案")
    topicnum=fields.BigIntField(null=True, default=0,description="选题数")
    copynum=fields.BigIntField(null=True, default=0,description="样本数")
    TypeText = fields.ForeignKeyField("models.TypeText",null=True,default=None,related_name="topiccopy_typetexts",description="文案类型")
    Source_description = fields.CharField(max_length=32,null=True, default=None, description="来源描述")
    Source_id = fields.CharField(max_length=32,null=True,default=None,  description="来源文案ID")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Platform(Model):#新媒体平台名
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="新媒体平台名")
    sort = fields.IntField(default=0, description="排序")

class Author(Model):#作者
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="作者名字")
    number = fields.CharField(max_length=255,null=True, default=None,description="作者号")
    url = fields.CharField(max_length=255, description="链接")
    urlnum = fields.IntField(default=0, description="链接数量")
    Platform =  fields.ForeignKeyField("models.Platform", related_name="authors", description="关联的新媒体平台")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class VideoTemplate(Model):#视频模板
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="模板名")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期") 

class Computer(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="计算机名")
    unique_id=fields.CharField(max_length=255, description="唯一标识")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期") 

class Font(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="字体名")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    url=fields.CharField(max_length=255,null=True, default=None, description="字体路径")

class Music(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="音乐名")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    url=fields.CharField(max_length=255,null=True, default=None, description="音乐路径")

class VoiceOver(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="配音名")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    url=fields.CharField(max_length=255,null=True, default=None, description="音乐路径")

class VideoClips (Model):#视频片段
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="素材名")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    url=fields.CharField(max_length=255,null=True, default=None, description="音乐路径")

class Script(Model):#视频脚本
    id = fields.IntField(pk=True)
    VideoTemplate = fields.ForeignKeyField("models.VideoTemplate",null=True, default=None, related_name="script_videotemplate", description="预设模板")
    Template_id = fields.CharField(max_length=255,null=True, default=None, description="模板编号")
    batch = fields.IntField(description="批次")
    status= fields.CharField(max_length=32, default="Unfinished", description="状态")
    number = fields.CharField(max_length=32, description="文案编号")
    title = fields.TextField(null=True, default=None,description="标题描述")
    covercopy = fields.TextField(null=True, default=None, description="封面文案")
    visualcopy = fields.TextField(null=True, default=None,description="画面文案")
    subtitlecopy = fields.TextField(null=True, default=None,description="字幕文案")
    displaysubtitles = fields.TextField(null=True, default=None,description="显示字幕")
    subtitlepronunciation = fields.TextField(null=True, default=None,description="字幕读音")
    VideoClips=fields.ForeignKeyField("models.VideoClips",null=True, default=None, related_name="scripts_videoclips", description="视频素材")
    Font= fields.ForeignKeyField("models.Font",null=True, default=None, related_name="scripts_font", description="视频字体")
    Music=  fields.ForeignKeyField("models.Music",null=True, default=None, related_name="scripts_music", description="视频背景音乐")
    VoiceOver= fields.ForeignKeyField("models.VoiceOver",null=True, default=None, related_name="scripts_voiceover", description="视频配音")
    publishtime = fields.CharField(max_length=255,null=True, default=None, description="发布时间")
    operator = fields.ForeignKeyField("models.User",null=True, default=None,  related_name="scripts_operator", description="操作人")
    Computer = fields.ForeignKeyField("models.Computer",null=True, default=None, related_name="script_computer", description="操作电脑")
    createdTime = fields.DatetimeField(auto_now_add=True, description="录入日期")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")

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

class StartTime(Model):#项目初始时间
    id = fields.IntField(pk=True)
    time= fields.DatetimeField(null=True, default=None,  description="项目初始时间")

class Phone(Model): #手机
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="手机编号")
    Model= fields.CharField(max_length=255,default=None, null=True, description="手机型号")
    Brand= fields.CharField(max_length=255,default=None, null=True, description="品牌名")
    Owner= fields.CharField(max_length=255,default=None, null=True, description="手机所有人")
    sort = fields.IntField(default=0, description="排序")
    deviceid= fields.CharField(max_length=255,default=None, null=True, description="设备id")
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class PNumber(Model):#手机号码
    id = fields.IntField(pk=True)
    number = fields.BigIntField(description="手机号码")
    rent = fields.IntField(default=None, null=True,  description="月租")
    Owner =  fields.CharField(max_length=32, default=None, null=True, description="所有人")
    createdTime = fields.DatetimeField(auto_now_add=True, description="创建日期")
    Phone=fields.ForeignKeyField("models.Phone",default=None, null=True,  related_name="phone_number", description="所在手机")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")

class Certifier (Model): #认证人
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="认证人名字")
    idnumber = fields.CharField(max_length=255,default=None, null=True, description="身份证号")
    Owner =  fields.CharField(max_length=32, default=None, null=True, description="所有人")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    createdTime = fields.DatetimeField(auto_now_add=True, description="创建日期")
 
class Video(Model):#视频
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="视频编号")
    Script=fields.ForeignKeyField("models.Script", default=None, null=True,related_name="videos", description="脚本")
    name = fields.CharField(max_length=255,default=None, null=True, description="视频文件名")
    path = fields.CharField(max_length=255,default=None, null=True, description="视频文件路径")
    createdTime = fields.DatetimeField(auto_now_add=True, description="制作日期")
    status = fields.CharField(max_length=32, default="Unfinished", description="状态")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")

class Account(Model):
    id = fields.IntField(pk=True)
    Phone=fields.ForeignKeyField("models.Phone",default=None, null=True,  related_name="accounts_phone_number", description="所在手机")
    Platform = fields.ForeignKeyField("models.Platform", related_name="accounts", default=None, null=True, description="新媒体平台")
    team=fields.IntField(default=None, null=True, description="组号")
    name = fields.CharField(max_length=255, default=None, null=True, description="名字")
    number = fields.CharField(max_length=255, default=None, null=True, description="账号ID")
    isDel=fields.BooleanField(default=False)
    password = fields.CharField(max_length=128, null=True, default=None, description="密码")
    profile = fields.CharField(max_length=255, default=None, null=True, description="简介")
    PNumber = fields.ForeignKeyField("models.PNumber", related_name="accounts_pnumber", default=None, null=True, description="手机号码")
    Certifier = fields.ForeignKeyField("models.Certifier", related_name="accounts_certifier", default=None, null=True, description="认证人")
    status = fields.CharField(max_length=32, default="ENABLE", description="状态")
    note=fields.CharField(max_length=225, default="", description="备注")
    updatedTime = fields.DatetimeField(auto_now=True, description="最后更新日期")
    createdTime=  fields.DatetimeField(auto_now_add=True, description="录入日期")


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

#     
#     status = fields.CharField(max_length=32, default="ENABLE", description="状态")
# # 账号内信息==================================================================================


# class AStatus(Model):#账号状态
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255, description="状态名")





#     Certifier =  fields.ForeignKeyField("models.Certifier", related_name="wxas", description="认证人")
#     PNumber =  fields.ForeignKeyField("models.PNumber", related_name="wxas", description="手机号码")
#     Phone =  fields.ForeignKeyField("models.Phone", related_name="wxas", description="所在手机")
#     Platform =  fields.ForeignKeyField("models.Platform", related_name="wxas", description="新媒体平台")
#     AStatus = fields.ForeignKeyField("models.AStatus", related_name="wxas", description="账号状态")
#     update = fields.DatetimeField(auto_now_add=True, description="创建日期")
#     



#     
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

# class DYData(Model):#抖音数据
#     id = fields.IntField(pk=True)
#     number = fields.CharField(max_length=255, description="视频编号")
#     作品名称=fields.CharField(max_length=255, description="作品名称")
#     发布时间=fields.DatetimeField(description="制作日期")
#     体裁=fields.CharField(max_length=255, description="体裁")
#     审核状态=fields.CharField(max_length=255, description="审核状态")
#     播放量=fields.CharField(max_length=255, description="播放量")
#     完播率=fields.CharField(max_length=255, description="完播率")
#     完播率5s=fields.CharField(max_length=255, description="完播率5s")
#     封面点击率=fields.CharField(max_length=255, description="封面点击率")
#     跳出率2s=fields.CharField(max_length=255, description="跳出率2s")
#     平均播放时长=fields.CharField(max_length=255, description="平均播放时长")
#     点赞量=fields.CharField(max_length=255, description="点赞量")
#     分享量=fields.CharField(max_length=255, description="分享量")
#     评论量=fields.CharField(max_length=255, description="评论量")
#     收藏量=fields.CharField(max_length=255, description="收藏量")
#     主页访问量=fields.CharField(max_length=255, description="主页访问量")
#     粉丝增量=fields.CharField(max_length=255, description="粉丝增量")
#     update = fields.DatetimeField(auto_now_add=True, description="更新日期")

# class SPHData(Model):#视频号数据
#     id = fields.IntField(pk=True)
#     number = fields.CharField(max_length=30, description="视频编号")
#     视频描述 = fields.CharField(max_length=255, description="视频描述")
#     视频ID = fields.CharField(max_length=255, description="视频ID")
#     发布时间 = fields.DatetimeField(description="发布时间", format="%Y/%m/%d")
#     完播率 =  fields.CharField(max_length=255, description="完播率")
#     平均播放时长 = fields.CharField(max_length=255, description="平均播放时长")
#     播放量 = fields.CharField(max_length=255, description="播放量")
#     推荐 = fields.CharField(max_length=255, description="推荐")
#     喜欢=fields.CharField(max_length=255, description="喜欢")
#     评论量=fields.CharField(max_length=255, description="评论量")
#     分享量=fields.CharField(max_length=255, description="分享量")
#     关注量=fields.CharField(max_length=255, description="关注量")
#     转发聊天和朋友圈=fields.CharField(max_length=255, description="转发聊天和朋友圈")
#     设为铃声 = fields.CharField(max_length=255, description="设为铃声")
#     设为状态 = fields.CharField(max_length=255, description="设为状态")
#     设为朋友圈封面 = fields.CharField(max_length=255, description="设为朋友圈封面")
# class XHSData(Model):#小红书数据
#     id = fields.IntField(pk=True)
#     number = fields.CharField(max_length=30, description="视频编号")
#     笔记标题=fields.CharField(max_length=255, description="笔记标题")
#     首次发布时间=fields.DatetimeField(description="首次发布时间")
#     体裁=fields.CharField(max_length=255, description="体裁")
#     观看量=fields.CharField(max_length=255, description="观看量")
#     点赞=fields.CharField(max_length=255, description="点赞")
#     评论=fields.CharField(max_length=255, description="评论")
#     收藏=fields.CharField(max_length=255, description="收藏")
#     涨粉= fields.CharField(max_length=255, description="涨粉")
#     分享=fields.CharField(max_length=255, description="分享")
#     人均观看时长=fields.CharField(max_length=255, description="人均观看时长")
#     弹幕=fields.CharField(max_length=255, description="弹幕")
# class KSData(Model):#快手数据
#     id = fields.IntField(pk=True)
#     number = fields.CharField(max_length=30, description="视频编号")
#     作品=fields.CharField(max_length=255, description="作品")
#     发布时间 = fields.DatetimeField(description="发布时间")
#     播放量 = fields.CharField(max_length=255, description="播放量")
#     完播率 =  fields.CharField(max_length=255, description="完播率")
#     评论量 =  fields.CharField(max_length=255, description="评论量")
#     点赞量 =  fields.CharField(max_length=255, description="点赞量")
#     收藏量 =  fields.CharField(max_length=255, description="收藏量")
#     涨粉量 =  fields.CharField(max_length=255, description="涨粉量")
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


# class UploadVideo(Model):#上传视频
#     id = fields.IntField(pk=True)
#     number = fields.CharField(max_length=255, description="视频编号")
#     Video = fields.ForeignKeyField("models.Video", related_name="uploadvideos", description="视频")
#     DYData = fields.ForeignKeyField("models.DYData", related_name="uploadvideos", description="抖音数据")
#     SPHData = fields.ForeignKeyField("models.SPHData", related_name="uploadvideos", description="视频号数据")
#     XHSData = fields.ForeignKeyField("models.XHSData", related_name="uploadvideos", description="小红书数据")
#     KSData = fields.ForeignKeyField("models.KSData", related_name="uploadvideos", description="快手数据")





    
    
    
    






