from tortoise.models import Model
from tortoise import fields

PROGRAM_NAME = 'SPLS'

class User(Model):#操作用户
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=32, index=True, description="用户名")
    password = fields.CharField(max_length=32,default="123456", description="密码")
    number = fields.CharField(max_length=32, description="编号")
    status = fields.CharField(max_length=32, default="Active", description="状态")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
class Platform(Model):#新媒体平台名
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="新媒体平台名")
class Author(Model):#作者
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="作者名字")
    Platform =  fields.ForeignKeyField("models.Platform", related_name="authors", description="关联的新媒体平台对象")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")
class Payment(Model):#缴费记录
    id = fields.IntField(pk=True)
    amount = fields.IntField(description="金额")
    PNumber=fields.ForeignKeyField("models.PNumber", related_name="payments", description="手机号码")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
class PNumber(Model):#手机号码
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=20, description="手机号码")
    rent = fields.IntField(default=0, description="月租")
    Certifier =  fields.ForeignKeyField("models.Certifier", related_name="pnumbers", description="认证人")
    update = fields.DatetimeField(auto_now_add=True, description="创建日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")
# 账号内信息==================================================================================
class Brand (Model):#品牌
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="品牌名")
class PhoneModel (Model):#手机型号
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="手机型号")
    Brand =  fields.ForeignKeyField("models.Brand", related_name="phonemodels", description="品牌")
class Phone(Model): #手机
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频标题")
    PhoneModel =  fields.ForeignKeyField("models.PhoneModel", related_name="phones", description="品牌")
    status = fields.CharField(max_length=32, default="Active", description="状态")
class Certifier (Model): #认证人
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="认证人名字")
    idnumber = fields.CharField(max_length=255, description="身份证号")
    status = fields.CharField(max_length=32, default="Active", description="状态")
class AStatus(Model):#账号状态
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="状态名")
class Account(Model):#视频号账号
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="账号ID")
    name = fields.CharField(max_length=255, description="名字")
    password = fields.CharField(max_length=128, null=True, default=None, description="密码")
    profile = fields.CharField(max_length=255, description="简介")
    PNumber =  fields.ForeignKeyField("models.PNumber", related_name="accounts", description="手机号码")
    Phone =  fields.ForeignKeyField("models.Phone", related_name="accounts", description="所在手机")
    Certifier =  fields.ForeignKeyField("models.Certifier", related_name="accounts", description="认证人")
    Platform =  fields.ForeignKeyField("models.Platform", related_name="accounts", description="新媒体平台")
    WXAccount =  fields.ForeignKeyField("models.WXAccount", null=True, default=None,related_name="accounts", description="微信号")
    AStatus = fields.ForeignKeyField("models.AStatus", related_name="accounts", description="账号状态")
    update = fields.DatetimeField(auto_now_add=True, description="创建日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
class WXAccount(Model):#微信号账号
    id = fields.IntField(pk=True)
    wechatid = fields.CharField(max_length=255, description="号")
    wechatname = fields.CharField(max_length=255, description="名")
    password = fields.CharField(max_length=128, null=True, default=None, description="密码")
    profile = fields.CharField(max_length=255, description="简介")
    Certifier =  fields.ForeignKeyField("models.Certifier", related_name="wxas", description="认证人")
    PNumber =  fields.ForeignKeyField("models.PNumber", related_name="wxas", description="手机号码")
    Phone =  fields.ForeignKeyField("models.Phone", related_name="wxas", description="所在手机")
    Platform =  fields.ForeignKeyField("models.Platform", related_name="wxas", description="新媒体平台")
    AStatus = fields.ForeignKeyField("models.AStatus", related_name="wxas", description="账号状态")
    update = fields.DatetimeField(auto_now_add=True, description="创建日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")

#意向用户========================================================================
class Lead(Model):#意向用户 
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="名")
    contact= fields.CharField(max_length=255, description="手机号码")
    wxnumber = fields.CharField(max_length=255, description="微信号")
    wxname = fields.CharField(max_length=255, description="微信名")
    profile = fields.CharField(max_length=255, description="简介")
    Sex= fields.ForeignKeyField("models.Sex", related_name="leads", description="性别")
    Position=  fields.ForeignKeyField("models.Position", related_name="leads", description="位置")
    Fans = fields.ManyToManyField("models.Fans", null=True, related_name="leads", description="粉丝")
    status = fields.CharField(max_length=32, default="Active", description="状态")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    fansdate = fields.DatetimeField(auto_now_add=True, description="关注日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
#用户内信息=========================================================================================
class FansStatus(Model):#用户状态
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="名")
class Sex(Model):#性别
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="名")
class Position(Model):#位置
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="名")
#用户信息=============================================
class Fans(Model):#粉丝
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, default=None,  description="号")
    name = fields.CharField(max_length=255, description="名")
    profile = fields.CharField(max_length=255, description="简介")
    Sex= fields.ForeignKeyField("models.Sex", related_name="fanss", description="性别")
    Position=  fields.ForeignKeyField("models.Position", related_name="fanss", description="位置")
    Account= fields.ManyToManyField("models.Account", related_name="fanss", description="账号")
    FansStatus=  fields.ManyToManyField("models.FansStatus", related_name="fanss", description="用户状态")
    UploadVideo = fields.ManyToManyField("models.Video", related_name="fanss",null=True, default=None, description="视频")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    fansdate = fields.DatetimeField(auto_now_add=True, description="关注日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
class Message(Model):#对话
    id = fields.IntField(pk=True)
    content = fields.CharField(max_length=255, description="内容")
    date = fields.DatetimeField(description="日期")
    Fans = fields.ForeignKeyField("models.Fans", related_name="messages", description="粉丝")
    Account = fields.ForeignKeyField("models.Account", related_name="messages", description="账号")
    status = fields.CharField(max_length=32, default="success", description="状态")
    note = fields.CharField(max_length=255,null=True, default=None, description="备注")
class Like(Model):#点赞
    id = fields.IntField(pk=True)
    Fans = fields.ForeignKeyField("models.Fans", related_name="likes", description="粉丝")
    UploadVideo= fields.ForeignKeyField("models.Video", related_name="likes", description="视频")
    date = fields.DatetimeField(auto_now_add=True, description="点赞时间")
class Collect(Model):#收藏
    id = fields.IntField(pk=True)
    Fans = fields.ForeignKeyField("models.Fans", related_name="collects", description="粉丝")
    UploadVideo= fields.ForeignKeyField("models.Video", related_name="collects", description="视频")
    date = fields.DatetimeField(auto_now_add=True, description="收藏时间")
class Comment(Model):#评论
    id = fields.IntField(pk=True)
    content = fields.CharField(max_length=255, description="内容")
    Fans = fields.ForeignKeyField("models.Fans", related_name="comments", description="粉丝")
    UploadVideo= fields.ForeignKeyField("models.Video", related_name="comments", description="视频")
    date = fields.DatetimeField(auto_now_add=True, description="评论时间")
class UploadVideo(Model):#上传视频
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="视频编号")
    Video = fields.ForeignKeyField("models.Video", related_name="uploadvideos", description="视频")
    DYData = fields.ForeignKeyField("models.DYData", related_name="uploadvideos", description="抖音数据")
    SPHData = fields.ForeignKeyField("models.SPHData", related_name="uploadvideos", description="视频号数据")
    XHSData = fields.ForeignKeyField("models.XHSData", related_name="uploadvideos", description="小红书数据")
    KSData = fields.ForeignKeyField("models.KSData", related_name="uploadvideos", description="快手数据")
class DYData(Model):#抖音数据
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="视频编号")
    作品名称=fields.CharField(max_length=255, description="作品名称")
    发布时间=fields.DatetimeField(description="制作日期")
    体裁=fields.CharField(max_length=255, description="体裁")
    审核状态=fields.CharField(max_length=255, description="审核状态")
    播放量=fields.CharField(max_length=255, description="播放量")
    完播率=fields.CharField(max_length=255, description="完播率")
    完播率5s=fields.CharField(max_length=255, description="完播率5s")
    封面点击率=fields.CharField(max_length=255, description="封面点击率")
    跳出率2s=fields.CharField(max_length=255, description="跳出率2s")
    平均播放时长=fields.CharField(max_length=255, description="平均播放时长")
    点赞量=fields.CharField(max_length=255, description="点赞量")
    分享量=fields.CharField(max_length=255, description="分享量")
    评论量=fields.CharField(max_length=255, description="评论量")
    收藏量=fields.CharField(max_length=255, description="收藏量")
    主页访问量=fields.CharField(max_length=255, description="主页访问量")
    粉丝增量=fields.CharField(max_length=255, description="粉丝增量")
    update = fields.DatetimeField(auto_now_add=True, description="更新日期")

class SPHData(Model):#视频号数据
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=30, description="视频编号")
    视频描述 = fields.CharField(max_length=255, description="视频描述")
    视频ID = fields.CharField(max_length=255, description="视频ID")
    发布时间 = fields.DatetimeField(description="发布时间", format="%Y/%m/%d")
    完播率 =  fields.CharField(max_length=255, description="完播率")
    平均播放时长 = fields.CharField(max_length=255, description="平均播放时长")
    播放量 = fields.CharField(max_length=255, description="播放量")
    推荐 = fields.CharField(max_length=255, description="推荐")
    喜欢=fields.CharField(max_length=255, description="喜欢")
    评论量=fields.CharField(max_length=255, description="评论量")
    分享量=fields.CharField(max_length=255, description="分享量")
    关注量=fields.CharField(max_length=255, description="关注量")
    转发聊天和朋友圈=fields.CharField(max_length=255, description="转发聊天和朋友圈")
    设为铃声 = fields.CharField(max_length=255, description="设为铃声")
    设为状态 = fields.CharField(max_length=255, description="设为状态")
    设为朋友圈封面 = fields.CharField(max_length=255, description="设为朋友圈封面")
class XHSData(Model):#小红书数据
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=30, description="视频编号")
    笔记标题=fields.CharField(max_length=255, description="笔记标题")
    首次发布时间=fields.DatetimeField(description="首次发布时间")
    体裁=fields.CharField(max_length=255, description="体裁")
    观看量=fields.CharField(max_length=255, description="观看量")
    点赞=fields.CharField(max_length=255, description="点赞")
    评论=fields.CharField(max_length=255, description="评论")
    收藏=fields.CharField(max_length=255, description="收藏")
    涨粉= fields.CharField(max_length=255, description="涨粉")
    分享=fields.CharField(max_length=255, description="分享")
    人均观看时长=fields.CharField(max_length=255, description="人均观看时长")
    弹幕=fields.CharField(max_length=255, description="弹幕")
class KSData(Model):#快手数据
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=30, description="视频编号")
    作品=fields.CharField(max_length=255, description="作品")
    发布时间 = fields.DatetimeField(description="发布时间")
    播放量 = fields.CharField(max_length=255, description="播放量")
    完播率 =  fields.CharField(max_length=255, description="完播率")
    评论量 =  fields.CharField(max_length=255, description="评论量")
    点赞量 =  fields.CharField(max_length=255, description="点赞量")
    收藏量 =  fields.CharField(max_length=255, description="收藏量")
    涨粉量 =  fields.CharField(max_length=255, description="涨粉量")
class UrlVDKey(Model):#视频采集链接
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, description="链接")
    key = fields.CharField(max_length=255, description="关键词")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待采集", description="状态")
    User =fields.ForeignKeyField("models.User", related_name="urlvdkeys", description="录入人")
class UrlVD (Model):#视频下载链接
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, description="链接")
    name = fields.CharField(max_length=255, description="视频标题")
    Author= fields.ForeignKeyField("models.Author", related_name="urlvds", description="作者")
    views=fields.CharField(max_length=255, description="浏览量")
    duration=fields.CharField(max_length=255, description="时长")
    uploaddate = fields.CharField(max_length=255, description="上传时间")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待下载", description="状态")
    UrlVDKey =fields.ForeignKeyField("models.UrlVDKey", null=True,related_name="urlvds", description="关键词链接")
class Footage(Model):#视频素材
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频文件名")
    path = fields.CharField(max_length=255, description="视频文件路径")
    update = fields.DatetimeField(auto_now_add=True, description="下载日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待筛选", description="状态")
    UrlVD=fields.ForeignKeyField("models.UrlVD",null=True, related_name="footages", description="素材链接")
class TrimVideo(Model):#视频分割片段
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频文件名")
    path = fields.CharField(max_length=255, description="视频文件路径")
    update = fields.DatetimeField(auto_now_add=True, description="分割日期")
    Footage=fields.ForeignKeyField("models.Footage", related_name="trimvideos", description="原始素材")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待裁剪", description="状态")
class VideoCategory(Model):#视频类型
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频分类名")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")
class CutVideo(Model):#视频裁剪片段
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频文件名")
    path = fields.CharField(max_length=255, description="视频文件路径")
    update = fields.DatetimeField(auto_now_add=True, description="裁剪日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待筛选", description="状态")
    TrimVideo=fields.ForeignKeyField("models.TrimVideo", related_name="cutvideos", description="分割素材")
    VideoCategory=fields.ForeignKeyField("models.VideoCategory", null=True, related_name="cutvideos", description="视频分类")
class MirrorVideo(Model):#视频镜像片段
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="视频分类名")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    CutVideo=fields.ForeignKeyField("models.CutVideo", related_name="mirrorvideos", description="裁剪素材")
    status = fields.CharField(max_length=32, default="待使用", description="状态")
class Video(Model):#视频
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="视频编号")
    Script=fields.ForeignKeyField("models.Script", related_name="videos", description="脚本")
    name = fields.CharField(max_length=255, description="视频文件名")
    path = fields.CharField(max_length=255, description="视频文件路径")
    update = fields.DatetimeField(auto_now_add=True, description="制作日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待筛选", description="状态")
class UrlAuthor(Model):#作者链接
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, description="链接")
    Author= fields.ForeignKeyField("models.Author", related_name="urlauthors", description="作者")
    Collectiondate = fields.DatetimeField(auto_now_add=True, description="录入日期")  
    status = fields.CharField(max_length=32, default="待筛选", description="状态")
class UrlText(Model):#文案链接
    id = fields.IntField(pk=True)
    url = fields.CharField(max_length=255, description="链接")
    Author= fields.ForeignKeyField("models.Author", related_name="urltexts", description="作者")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待采集", description="状态")

class TypeText (Model):#文案类型
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="文案类型名")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")

class UrlExtractionT(Model):#链接提取文案
    id = fields.IntField(pk=True)
    text = fields.TextField(description="文案") 
    TypeText=fields.ManyToManyField("models.TypeText", related_name="urlextractionts", description="文案类型")
    UrlText=fields.ForeignKeyField("models.UrlText", related_name="urlextractionts", description="文案链接")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")

class PromptText(Model):#提示词文案
    id = fields.IntField(pk=True)
    text = fields.TextField(description="提示词") 
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="待筛选", description="状态")

class TypeTT (Model):#文案模类型
    id = fields.IntField(pk=True)
    number= fields.CharField(max_length=255, description="类型编号")
    name = fields.CharField(max_length=255, description="类型名")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="at", description="状态")

class Proposaltext(Model):#选题文案
    id = fields.IntField(pk=True)
    UrlExtractionT = fields.ManyToManyField("models.UrlExtractionT", related_name="proposaltexts", description="链接提取文案")

class ModelText(Model):#范本文案
    id = fields.IntField(pk=True)
    UrlExtractionT = fields.ManyToManyField("models.UrlExtractionT", related_name="modeltexts", description="链接提取文案")

class TextTemplate(Model):#文案模板
    id = fields.IntField(pk=True)
    number= fields.CharField(max_length=255, description="模板编号")
    text = fields.TextField(description="文案") 
    Proposaltext=fields.ForeignKeyField("models.Proposaltext", related_name="texttemplates", description="选题文案")
    PromptText=fields.ForeignKeyField("models.PromptText", related_name="texttemplates", description="提示词文案")
    ModelText=fields.ForeignKeyField("models.ModelText", related_name="texttemplates", description="范本文案")
    TypeTT=fields.ForeignKeyField("models.TypeTT", related_name="texttemplates", description="文案模类型")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, default=None, description="删除日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")

class Script(Model):#视频脚本
    id = fields.IntField(pk=True)
    number = fields.CharField(max_length=255, description="文案编号")
    预设模板 = fields.ForeignKeyField("models.VideoTemplate", related_name="scripts", description="预设模板")
    标题描述 = fields.TextField(description="标题描述")
    抖音关键词 = fields.CharField(max_length=255, description="抖音关键词")
    视频号关键词 = fields.CharField(max_length=255, description="视频号关键词")
    小红书关键词 = fields.CharField(max_length=255, description="小红书关键词")
    快手关键词 = fields.CharField(max_length=255, description="快手关键词")
    视频字体 = fields.CharField(max_length=255, description="视频字体")
    封面模板 = fields.CharField(max_length=255, description="封面模板")
    封面文案 = fields.CharField(max_length=255, description="封面文案")
    视频模板 = fields.CharField(max_length=255, description="视频模板")
    画面文案 = fields.TextField(description="画面文案")
    字幕模板 = fields.CharField(max_length=255, description="字幕模板")
    字幕文案 = fields.CharField(max_length=255, description="字幕文案")
    显示字幕 = fields.TextField(description="显示字幕")
    视频配音 = fields.CharField(max_length=255, description="视频配音")
    字幕读音 = fields.TextField(description="字幕读音")
    背景音乐 = fields.CharField(max_length=255, description="背景音乐")
    视频素材 = fields.CharField(max_length=255, description="视频素材")
    模板编号 = fields.CharField(max_length=255, description="模板编号")
    类型编号 = fields.CharField(max_length=255, description="类型编号")
class VideoTemplate(Model):#视频模板
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255, description="模板名")
    path = fields.CharField(max_length=255, description="模板路径")
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")  




    
    
    
    






