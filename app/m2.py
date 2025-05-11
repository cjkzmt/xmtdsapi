from tortoise.models import Model
from tortoise import fields

PROGRAM_NAME = 'SPLS'

class BaseModel(Model):
    class Meta:
        abstract = True

    id = fields.IntField(pk=True)
    update = fields.DatetimeField(auto_now_add=True, description="录入日期")
    deledate = fields.DatetimeField(null=True, description="删除日期")
    status = fields.CharField(max_length=32, default="Active", description="状态")

class User(BaseModel):
    class Meta:
        table = f"{PROGRAM_NAME}_User"

    name = fields.CharField(max_length=32, index=True, description="用户名")
    password = fields.CharField(max_length=32, default="123456", description="密码")
    number = fields.CharField(max_length=32, description="编号")

class Platform(BaseModel):
    class Meta:
        table = f"{PROGRAM_NAME}_Platform"

    name = fields.CharField(max_length=255, description="新媒体平台名")

class Author(BaseModel):
    class Meta:
        table = f"{PROGRAM_NAME}_Author"

    name = fields.CharField(max_length=255, description="作者名字")
    platform = fields.ForeignKeyField("models.Platform", related_name="authors", description="关联的新媒体平台对象")

# 账号内信息
class Account(BaseModel):
    class Meta:
        abstract = True

    number = fields.CharField(max_length=255, description="账号号")
    name = fields.CharField(max_length=255, description="账号名")
    profile = fields.CharField(max_length=255, description="简介")
    pnumber = fields.ForeignKeyField("models.PNumber", related_name="accounts", description="手机号码")
    certifier = fields.ForeignKeyField("models.Certifier", related_name="accounts", description="认证人")
    platform = fields.ForeignKeyField("models.Platform", related_name="accounts", description="新媒体平台")
    astatus = fields.ForeignKeyField("models.AStatus", related_name="accounts", description="账号状态")

class DYAccount(Account):
    class Meta:
        table = f"{PROGRAM_NAME}_DYAccount"

    password = fields.CharField(max_length=128, null=True, default=None, description="密码")
    phone = fields.ForeignKeyField("models.Phone", related_name="dy_accounts", description="所在手机")

class SPHAccount(Account):
    class Meta:
        table = f"{PROGRAM_NAME}_SPHAccount"

    wx_account = fields.ForeignKeyField("models.WXAccount", related_name="sph_accounts", description="微信号")

class WXAccount(Account):
    class Meta:
        table = f"{PROGRAM_NAME}_WXAccount"

    wechat_id = fields.CharField(max_length=255, description="微信号")
    wechat_name = fields.CharField(max_length=255, description="微信名")
    password = fields.CharField(max_length=128, null=True, default=None, description="密码")
    phone = fields.ForeignKeyField("models.Phone", related_name="wx_accounts", description="所在手机")