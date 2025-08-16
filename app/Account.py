from .models import *
from .db_connector import tortoise_tx
@tortoise_tx()
async def UpAccount(id,info):
    iteam=await Account.filter(id=id).prefetch_related('AccountTeam','Platform')
    if not iteam: return False
    iteam=iteam[0]
    p=iteam.Platform.name + str(iteam.AccountTeam.number)
    if iteam.name != info['name']:
        print(f'❌  {p}账号:{id} 名字有误{iteam.name} 现是{info["name"]}')
        return False
    number=info['number'].strip() 
    if iteam.number:
        if iteam.number != number:
            print(f'❌  {p}账号:{id} ID有误{iteam.number} 现是{number}')
            return False
    else:
        iteam.number=number
    newFans=int(info['newFans'])
    if iteam.InitFans is None:
        iteam.InitFans=newFans
    iteam.newFans=newFans
    await iteam.save()
    return True