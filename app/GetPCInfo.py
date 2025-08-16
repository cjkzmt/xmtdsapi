from .models import *
from tortoise.transactions import in_transaction
from zhmm import *
from src.utils.Verification import Verification
from .db_connector import tortoise_tx
@tortoise_tx()
async def GetPCInfo():
    async with in_transaction():
        # 获取电脑信息
        try:
            item = await Computer.get(id=PCID)
        except Exception as e:
            raise f'❌ 查无此电脑{PCID}:{e}'
        
        # 验证电脑身份
        verification = Verification()
        if item.Verification:
            if item.Verification != verification:
                raise f'❌ 此电脑{PCID}的唯一ID有误！,请确认您的电脑ID！'
            else:
                print(f'✅ 电脑:{item.name}登陆成功！')
        else:
            # 首次注册
            item.Verification = verification
            await item.save()
            print(f'✅ 电脑{PCID}:{item.name}注册成功！')
        
        # 返回权限设置
        return (
            item.createtext == 'ENABLE',
            item.createvideo == 'ENABLE', 
            item.publishvideo == 'ENABLE',
            item.createclip == 'ENABLE',

        )


