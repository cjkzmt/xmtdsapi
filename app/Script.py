from .models import *
from tortoise.transactions import in_transaction
from zhmm import *
from datetime import datetime, timedelta, timezone
from tortoise.query_utils import Prefetch
from tortoise.exceptions import OperationalError
from collections import defaultdict
from src.task.Video.UpClip import GetClip
from .db_connector import tortoise_tx
@tortoise_tx()
async def getVideoInfo():
    try:
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(days=28)
        info=GetClip()
        TeampathS=[]
        for path, clipSum in info.items():
            if clipSum<1:continue
            TeampathS.append(path)
        print(TeampathS)
        Teamlist=await TeamOwner.filter(path__in=TeampathS)
        print([i.id for i in Teamlist])
        script_qs = Script.filter(
            AccountTeam__TeamOwner_id__in=[i.id for i in Teamlist],
            status__not='完成',
            copystatus='ENABLE',
            videostatus__not= 'ENABLE',
            publishtime__gt=now,
            publishtime__lt=end_time,
        )
        script_qs=script_qs.order_by("publishtime").prefetch_related("Font", "Music",  "Over",Prefetch("AccountTeam", queryset=AccountTeam.all().prefetch_related("TypeVideo", "TypeCover", "TypeSubtitle",'TeamOwner')),)
        all_scripts = await script_qs
        print(f'✅ 获取到 {len(all_scripts)} 个剪辑任务')
        if not all_scripts: 
            print('❌ 没有剪辑任务，或任务以完成')
            return None
        return all_scripts
    except Exception as e:
        raise e

@tortoise_tx()
async def getPublishInfo():
    try:
        async with in_transaction():
            Teamlist = await AccountTeam.filter(Computer_id=PCID,status="ENABLE")
            if len(Teamlist)==0: 
                print('❌ 此电脑没有可用账号，请先添加账号')
                return None
            platformlist = await Platform.filter(publish="ENABLE")
            keywords =[i.text for i in  await Keyword.all()] 
            max_advance = max(p.advance for p in platformlist) if platformlist else 0
            now = datetime.now(timezone.utc)
            end_time = now + timedelta(days=max_advance)
            script_qs = Script.filter(
                    AccountTeam_id__in=[t.id for t in Teamlist],
                    status__not='完成',
                    videostatus='ENABLE',
                    publishtime__gt=now,
                    publishtime__lt=end_time)
            all_scripts = await script_qs.order_by("publishtime")
            if not all_scripts:
                print('❌ 当前电脑无发布任务，或任务已经完成')
                return None
            accountlist = await Account.filter(status="ENABLE",Platform_id__in=[i.id for i in platformlist],AccountTeam_id__in=[t.id for t in Teamlist])
            if not accountlist:
                print('❌ 此电脑没有可用账号，请先添加账号')
                return None
            data_qs = Data.filter(
                    status="DISABLE",
                    Account_id__in=[i.id for i in accountlist],
                    Script_id__in=[s.id for s in all_scripts]
                ).prefetch_related(
                    'Script',
                    Prefetch("Account", queryset=Account.all().prefetch_related("Platform")))
            DataAlllist = await data_qs
            platform_map = {p.id: p.advance for p in platformlist}
            result = [d for d in DataAlllist if now < d.Script.publishtime < now + timedelta(days=platform_map.get(d.Account.Platform_id, 0))]
            if len(result)==0:
                print('❌ 当前电脑无发布任务，或任务已经完成')
                return None
            data_map = defaultdict(list)

            for r in result:
                data_map[r.Script_id].append({
                    'id': r.id,
                    'Account_id': r.Account.id,
                    'Platform': r.Account.Platform.name,
                    'character':r.Account.Platform.character,
                    'verification':r.Account.Platform.verification,
                    'publishverif':r.Account.Platform.publishverif,
                    'loginurl':r.Account.Platform.loginurl,
                    'keycount':r.Account.Platform.keycount,
                    'url':r.Account.Platform.publishurl,
                })
            videoname=[]
            Script_map = defaultdict(list)
            for r in all_scripts:
                videoname.append(r.videoname)
                Script_map[r.AccountTeam_id].append({
                    'id': r.id,
                    'videoname': r.videoname,
                    'title':r.title,
                    'publishtime':str(r.publishtime),
                    'Data':data_map[r.id]
                })
            return Teamlist,keywords,Script_map,videoname
    except Exception as e:
        raise e

@tortoise_tx()
async def Upvideostatus(idlist):
    if idlist is None or len(idlist) == 0: return
    try:
        await Script.bulk_update(
            [Script(id=id, status="ENABLE", videoname=name) for id, name in idlist],
            fields=['status', 'videoname']
        )
    except OperationalError as e:
        raise e

@tortoise_tx()
async def getPublishData(Scripts):
    rows = await Data.filter(
    Script_id__in=[s.id for s in Scripts],
    Account__status='ENABLE'
        ).values(
            'id', 'Script_id', 'Account_id',
            'Account__Platform__name',
            'Account__Platform__publishurl',
            'Account__Platform__character',
            'Account__Platform__keycount',
            'Account__Platform__verification',
            'Account__Platform__advance',
            'Account__Platform__publishverif',
            'status')
    return rows

@tortoise_tx()
async def UpScriptsStatus(id):
    await Data.filter(id=id).update(status='完成')

