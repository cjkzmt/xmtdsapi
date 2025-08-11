from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tortoise.expressions import Case, When,Q
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
import math
from .Platform import getAll
# from sqlalchemy import nullslast
from collections import defaultdict
import random
from tortoise.query_utils import Prefetch
from datetime import datetime, timedelta, time,timezone
from tortoise.transactions import in_transaction

Script_api = APIRouter()

class QueryCondition(Condition):
    AccountTeam_id: Optional[int] = None
    Day:Optional[int] = 28
    unScripList: Optional[list[int]] = []
    getinfo: Optional[str] = None

class InItem(BaseModel):
    id: Optional[int] = None
    topic_id:  Optional[int] = None
    copy_id:  Optional[int] = None
    AccountTeam_id:  Optional[int] = None
    PromptText_id:  Optional[int] = None
    ReleasePlan_id:  Optional[int] = None
    publishtime: Optional[str] = None
    Music_id: Optional[int] = None
    Over_id: Optional[int] = None
    Font_id: Optional[int] = None
    VideoTemplate_id:   Optional[int] = None
    videopath: Optional[str] = None
    drafline: Optional[str] = None
    line: Optional[str] = None
    draftitle: Optional[str] = None
    title:Optional[str] = None
    drafcover: Optional[str] = None
    cover: Optional[str] = None
    subtitle: Optional[str] = None
    reading: Optional[str] = None
    videoname: Optional[str] = None
    linestatus: Optional[str] = None
    copystatus: Optional[str] = None
    videostatus: Optional[str] = None
    status: Optional[str] = None
class DataItem(BaseModel):
    id: Optional[int] = None
    Script_id: Optional[int] = None
    Account_id: Optional[int] = None
    Platform: Optional[str] = None
    character:Optional[int] = None
    keycount:Optional[int] = None
    publishurl: Optional[str] = None
    verification:Optional[str] = None
    advance :Optional[int] = None
    publishverif:Optional[str] = None
    status: Optional[str] = None
class Item(InItem):
    shorthand:  Optional[str] = None
    VideoTemplate:  Optional[str] = None
    topictext:  Optional[str] = None
    copytext:  Optional[str] = None
    promptText:  Optional[str] = None
    AccountTeam:  Optional[int] = None
    operator_id: Optional[int] = None
    Computer_id: Optional[int] = None
    Font: Optional[str] = None
    Templatenum: Optional[str] = None
    Music: Optional[str] = None
    Over: Optional[str] = None
    speed:Optional[float] = None
    TypeVideo_id: Optional[int] = None
    TypeVideo: Optional[str] = None
    videoheight: Optional[int] = None
    videowidth: Optional[int] = None
    TypeCover_id: Optional[int] = None
    TypeCover: Optional[str] = None
    fixedtitle: Optional[str] = None
    TypeSubtitle_id: Optional[int] = None
    TypeSubtitle: Optional[str] = None
    fontsize: Optional[int] = None
    fontcolor: Optional[str] = None
    scope: Optional[str] = None
    createdTime: Optional[str] = None
    updatedTime: Optional[str] = None
    publish: List[DataItem]

class QueryResult(Result):
    records: List[Item]

@Script_api.post("/TaskList", summary='分页查询用户数据', description='功能描述')
async def TaskList(request: Request):
    Role = request.state.user_info.get("Role")
    if Role!="Computer":
        return ResponseModel(
        code="000001",
        mesg="身份信息错误",
        time=str(datetime.now()),
        data=[])
    PC_id = request.state.user_info.get("user_id")
    computer = await Computer.get(id=PC_id)
    Create_Text = True if computer.createtext=='ENABLE' else False
    Create_Video = True if computer.createvideo=='ENABLE' else False
    Publish_Video = True if computer.publishvideo=='ENABLE' else False
    data = await parse_request_body(request, QueryCondition)
    start_time = datetime.now(timezone.utc)
    end_time = datetime.now(timezone.utc).date()+ timedelta(days=data.Day)
    task_time = datetime.now(timezone.utc) + timedelta(hours=1)
    q = (
        Q(publishtime__gt=start_time) &
        Q(publishtime__lt=end_time) &
        ~Q(status='完成') &
        ~Q(id__in=data.unScripList))# &        
    query = Script.filter(q)
    annotated_query = query.annotate(
        publishtime_isnull=Case(
            When(publishtime__isnull=True, then=1),
            default=0)
    ).order_by("publishtime", "AccountTeam_id")
    Scripts = await annotated_query
    Script_tasks = []
    for iteam in Scripts:
        id = iteam.id
        if id in data.unScripList:
            continue
        Computer_id=iteam.Computer_id
        updatedTime=iteam.updatedTime
        if updatedTime < task_time  and Computer_id is not None and Computer_id !=PC_id :continue
        if len(Script_tasks)> data.pageSize:break
        if iteam.videoname:
            if Publish_Video:
                teamlist = await AccountTeam.filter(Computer_id=PC_id).values_list('id', flat=True)
                if len(teamlist)==0: continue
                if iteam.AccountTeam_id not in teamlist: continue
                if iteam.videostatus=='ENABLE':
                    Script_tasks.append({
                        'taskname':'Publish',
                        'id':iteam.id})
            continue
        if iteam.reading:
            if Create_Video:
                if iteam.copystatus=='ENABLE':
                    Script_tasks.append({
                    'taskname':'Video',
                    'id':iteam.id})
        if Create_Text:
            if iteam.line:
                if iteam.linestatus=='ENABLE':
                    if iteam.title is None:
                        Script_tasks.append({
                        'taskname':'title',
                        'id':iteam.id})
                    if iteam.cover is None:
                        Script_tasks.append({
                        'taskname':'cover',
                        'id':iteam.id})
                    if iteam.reading is None:
                        Script_tasks.append({
                        'taskname':'reading',
                        'id':iteam.id})
                continue
            Script_tasks.append({
                        'taskname':'line',
                        'id':iteam.id})
    for iteam in Script_tasks:
        Scripting= await Script.get(id=iteam['id'])
        Scripting.Computer_id=PC_id
        await Scripting.save()
    return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=Script_tasks)  

@Script_api.post("/getPages", summary='分页查询用户数据', description='功能描述')
async def getPages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    
    # 1. 定义常量提高可读性
    TASK_TYPES = {'ReviewScript', 'ReviewCopy', 'ReviewVideo', '脚本文案任务', '视频文案任务'}
    TASK_FILTERS = {
        'ReviewScript': {'line__isnull': False, 'linestatus__not': 'ENABLE'},
        'ReviewCopy': {'linestatus': 'ENABLE', 'copystatus__not': 'ENABLE'},
        'ReviewVideo': {'videoname__isnull': False, 'videostatus__not': 'ENABLE'},
        '脚本文案任务': {'line__isnull': True, 'topic_id__isnull': False},
        '视频文案任务': {
            'line__isnull': False, 
            'linestatus': 'ENABLE', 
            'reading__isnull': True, 
            'topic_id__isnull': False
        }
    }

    # 2. 构建基础查询
    query = Script.filter().prefetch_related(
        "VideoTemplate", "topic", "copy", "PromptText", "Font", "Music", "Computer", "Over", 
        Prefetch("AccountTeam", queryset=AccountTeam.all().prefetch_related(
            "TypeVideo", "TypeCover", "TypeSubtitle", 'TeamOwner'
        )),
    )
    query = condition(data, query)
    
    # 3. 应用过滤条件
    if data.AccountTeam_id:
        query = query.filter(AccountTeam_id=data.AccountTeam_id)
    
    if data.getinfo and data.getinfo in TASK_TYPES:
        # 优化时间计算
        now = datetime.now(timezone.utc)
        start_time = now
        end_time = now + timedelta(days=data.Day)
        
        query = query.filter(publishtime__gt=start_time, publishtime__lt=end_time)
        query = query.filter(id__notin=data.unScripList)
        
        # 使用字典映射替代多重if判断
        if data.getinfo in TASK_FILTERS:
            query = query.filter(**TASK_FILTERS[data.getinfo])

    # 4. 分页处理
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    
    # 优化排序逻辑
    annotated_query = query.annotate(
        publishtime_isnull=Case(
            When(publishtime__isnull=True, then=1),
            default=0
        )
    ).order_by("publishtime_isnull", "publishtime", "AccountTeam_id")
    
    scripts = await annotated_query.offset(offset).limit(data.pageSize)
    script_ids = [s.id for s in scripts]
    
    # 5. 批量获取关联数据
    # 获取Data数据
    rows = await Data.filter(
        Script_id__in=script_ids,
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
        'status'
    )
    
    # 构建数据映射
    data_map = defaultdict(list)
    for r in rows:
        data_map[r['Script_id']].append(DataItem(
            id=r['id'],
            Script_id=r['Script_id'],
            Account_id=r['Account_id'],
            Platform=r['Account__Platform__name'],
            publishurl=r['Account__Platform__publishurl'],
            character=r['Account__Platform__character'],
            keycount=r['Account__Platform__keycount'],
            verification=r['Account__Platform__verification'],
            advance=r['Account__Platform__advance'],
            publishverif=r['Account__Platform__publishverif'],
            status=r['status']
        ))
    
    # 6. 构建响应数据
    items_info = []
    for script in scripts:
        # 安全获取关联对象属性
        account_team = script.AccountTeam
        shorthand = scope = accountTeam = None
        TypeVideo_id = TypeVideo = videoheight = videowidth = None
        TypeCover_id = TypeCover = fixedtitle = None
        TypeSubtitle_id = TypeSubtitle = fontsize = fontcolor = None
        
        if account_team:
            accountTeam = account_team.number
            
            if account_team.TeamOwner:
                shorthand = account_team.TeamOwner.shorthand
                scope = account_team.TeamOwner.scope
            
            if account_team.TypeVideo:
                TypeVideo_id = account_team.TypeVideo.id
                TypeVideo = account_team.TypeVideo.name
                videoheight = account_team.TypeVideo.videoheight
                videowidth = account_team.TypeVideo.videowidth
            
            if account_team.TypeCover:
                TypeCover_id = account_team.TypeCover.id
                TypeCover = account_team.TypeCover.name
                fixedtitle = account_team.TypeCover.fixedtitle
            
            if account_team.TypeSubtitle:
                TypeSubtitle_id = account_team.TypeSubtitle.id
                TypeSubtitle = account_team.TypeSubtitle.name
                fontsize = account_team.TypeSubtitle.fontsize
                fontcolor = account_team.TypeSubtitle.fontcolor
        
        # 安全获取文本内容
        topic_text = getattr(script.topic, 'text', None) if script.topic else None
        copy_text = getattr(script.copy, 'text', None) if script.copy else None
        prompt_text = getattr(script.PromptText, 'text', None) if script.PromptText else None
        
        # 构建模板编号
        Templatenum = None
        if all([script.AccountTeam, script.topic, script.copy, script.PromptText]):
            Templatenum = f"{script.AccountTeam.number}_{script.topic_id}_{script.copy_id}_{script.PromptText_id}"
        
        items_info.append(Item(
            id=script.id,
            VideoTemplate_id=script.VideoTemplate_id,
            VideoTemplate=getattr(script.VideoTemplate, 'name', None),
            topic_id=script.topic_id,
            copy_id=script.copy_id,
            PromptText_id=script.PromptText_id,
            topictext=topic_text,
            copytext=copy_text,
            promptText=prompt_text,
            title=script.title,
            AccountTeam_id=script.AccountTeam_id,
            AccountTeam=accountTeam,
            shorthand=shorthand,
            scope=scope,
            TypeVideo_id=TypeVideo_id,
            TypeVideo=TypeVideo,
            videoheight=videoheight,
            videowidth=videowidth,
            TypeCover_id=TypeCover_id,
            TypeCover=TypeCover,
            fixedtitle=fixedtitle,
            TypeSubtitle_id=TypeSubtitle_id,
            TypeSubtitle=TypeSubtitle,
            fontsize=fontsize,
            fontcolor=fontcolor,
            cover=script.cover,
            drafline=script.drafline,
            line=script.line,
            linestatus=script.linestatus,
            subtitle=script.subtitle,
            reading=script.reading,
            copystatus=script.copystatus,
            Font_id=script.Font_id,
            Font=getattr(script.Font, 'name', None),
            publishtime=str(script.publishtime) if script.publishtime else None,
            Templatenum=Templatenum,
            ReleasePlan_id=script.ReleasePlan_id,
            operator_id=script.operator_id,
            Computer_id=script.Computer_id,
            videoname=script.videoname,
            videopath=script.videopath,
            videostatus=script.videostatus,
            Music_id=script.Music_id,
            Music=getattr(script.Music, 'name', None),
            Over_id=script.Over_id,
            Over=getattr(script.Over, 'filename', None),
            speed=getattr(script.Over, 'speed', None) if script.Over else None,
            status=script.status,
            publish=data_map.get(script.id, []),
            createdTime=str(script.createdTime),
            updatedTime=str(script.updatedTime)
        ))
    
    return queryResult(data, QueryResult, items_info, total)

@Script_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    async with in_transaction():
        Script_in = await parse_request_body(request, InItem)
        print(Script_in)
        if Script_in.id:
            Scripting = await Script.get(id=Script_in.id)
            if Script_in.draftitle:
                Scripting.draftitle = Script_in.draftitle if len(Script_in.draftitle)>3 else None
            if Script_in.title:
                Scripting.title = Script_in.title if len(Script_in.title)>3 else None
            if Script_in.cover:
                Scripting.cover = Script_in.cover if len(Script_in.cover)>3 else None
            if Script_in.status:
                Scripting.status = Script_in.status
            if Script_in.linestatus:
                Scripting.linestatus = Script_in.linestatus
            if Script_in.drafline and Scripting.drafline !=Script_in.drafline :
                Scripting.drafline = Script_in.drafline  if len(Script_in.drafline)>3 else None  
            if Script_in.line and Scripting.line !=Script_in.line :
                Scripting.line = Script_in.line  if len(Script_in.line)>3 else None
                Scripting.linestatus="DISABLE"
            if Script_in.subtitle:
                Scripting.subtitle = Script_in.subtitle  if len(Script_in.subtitle)>3 else None
            if Script_in.copystatus:
                Scripting.copystatus = Script_in.copystatus
            if Script_in.reading and Scripting.reading !=Script_in.reading :
                Scripting.reading = Script_in.reading if len(Script_in.reading)>3 else None
                Scripting.copystatus="DISABLE" 
            if Script_in.Font_id and Script_in.Font_id>0:
                Scripting.Font_id = Script_in.Font_id
            if Script_in.publishtime and Scripting.publishtime !=Script_in.publishtime:
                    Scripting.publishtime = Scripting.publishtime
                    Scripting.ReleasePlan_id=None
            if Script_in.videostatus :
                Scripting.videostatus = Script_in.videostatus
            if Script_in.videoname and Script_in.videoname!=Scripting.videoname:
                Scripting.videoname=Script_in.videoname
                Scripting.videostatus="DISABLE" 
            if Script_in.videopath :
                Scripting.videopath=Script_in.videopath
            if  Script_in.Music_id and Script_in.Music_id>0:
                Scripting.Music_id = Script_in.Music_id
            if Script_in.Over_id and Script_in.Over_id>0:
                Scripting.Over_id = Script_in.Over_id
            await Scripting.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await creatOneScript(Script_in.AccountTeam_id,publishtime=Script_in.publishtime,title=Script_in.title,videoname=Script_in.videoname)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

async def getAccountstatus(AccountTeam_id,name,status=None):
    platform = await  Platform.get(name=name)
    account = await Account.filter(AccountTeam_id=AccountTeam_id,platform_id=platform.id,status="ENABLE").first()
    x=  '已发布' if status == '已发布' else '未发布' if  account else '无账号'
    return x

class CreatScript(BaseModel):
    AccountTeamlist: List[int]
    topiccopylist: List[List[int]]

class idlistiteam(BaseModel):
    idlist: List[int]

@Script_api.post("/enablesCopys", summary='添加一个内容', description='功能描述')
async def enablesCopys(request: Request):
    body = await request.json()
    print(body)
    async with in_transaction():
        Script_in = await parse_request_body(request,idlistiteam)
        print(Script_in)
        for iteam in Script_in.idlist:
            Scripting = await Script.get(id=iteam)
            Scripting.copystatus="ENABLE" 
            Scripting.status="视频待制作" 
            await Scripting.save()
        return ResponseModel(code="000000", mesg="批量通过成功", time=str(datetime.now()), data=True)

@Script_api.post("/CreatScript", summary='添加一个内容', description='功能描述')
async def creatScript(request: Request):
    async with in_transaction():
        Script_in = await parse_request_body(request, CreatScript)
        print(Script_in)
        creatScripts(Script_in)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

@Script_api.get("/RefreshTask", summary='添加一个内容', description='功能描述')
async def RefreshTask():
    iteams = await Script.filter(publishtime__isnull=False,status__not='完成')
    print(len(iteams))
    for iteam in iteams:
        AccountTeam_id=iteam.AccountTeam_id
        publishstatus=''
        accountlikst = await Account.filter(AccountTeam_id=AccountTeam_id,status="ENABLE")
        for account in accountlikst:
            data=await Data.filter(Script_id=iteam.id,Account_id=account.id).first()
            if data is None:
                data=await Data.create(Script_id=iteam.id,Account_id=account.id)
            publishstatus+=data.status
        now = datetime.now(timezone.utc)
        Scripting = await Script.get(id=iteam.id)
        if iteam.publishtime < now:
            print(f"任务{iteam.id}已过期")
            if '已发布' in publishstatus:
                Scripting.status = '完成'
                await Scripting.save()
                continue
            Scripting.publishtime = Scripting.publishtime + timedelta(days=30)
        if '已发布' not  in  publishstatus:
            status = '视频待审核' if iteam.status == 'DISABLE' else '待发布'
            if iteam.videoname is None:
                status = '视频文案待审核' if iteam.status == 'DISABLE' else '视频待制作'
                if iteam.reading is None:
                    status = '脚本文案待审核' if iteam.status == 'DISABLE' else '视频文案待制作'
                    if iteam.line is None:
                        status = '脚本文案待制作'
        elif '未发布' not in publishstatus:
            status = '完成'
        Scripting.status=status
        await Scripting.save()
    return ResponseModel(
        code="000000",
        mesg="刷新任务成功",
        time=str(datetime.now()),
        data=True)
async def creatdata(AccountTeam_id,Script_id):
    iteams=await Account.filter(AccountTeam_id=AccountTeam_id)
    for iteam in iteams:
        data=await Data.filter(Script_id=Script_id,Account_id=iteam.id)
        if data: continue
        await Data.create(Script_id=Script_id,Account_id=iteam.id)

async def creatOneScript(AccountTeam_id,topicid=None,copyid=None,PromptTextid=None,publishtime=None,title=None,videoname=None):
    iteam=await Script.create(
        topic_id=topicid ,
        copy_id=copyid,
        AccountTeam_id=AccountTeam_id,
        PromptText_id=PromptTextid,
        publishtime=publishtime,
        title=title,
        videoname=videoname,
        status="待发布" if videoname else "脚本文案待制作")
    creatdata(AccountTeam_id,iteam.id)

async def creatScripts(Script_in:CreatScript):
    for AccountTeam_id in Script_in.AccountTeamlist:
        for pair in Script_in.topiccopylist:
            if len(pair) != 3:
                continue
            topicid, copyid,PromptTextid = pair
            await creatOneScript(AccountTeam_id,topicid=topicid,copyid=copyid,PromptTextid=PromptTextid)

async def creatScriptinfo(accountTeam=None):
    async with in_transaction():
        if accountTeam:
            AccountTeams=[accountTeam]
        else:
            AccountTeams = await AccountTeam.all().values('id', 'number', 'scope')
        if AccountTeams==[]:return '没有需要添加脚本的账号'
        typetextlist=await TypeText.all()
        topictype=[]
        copytype=[]
        for iteam in typetextlist:
            if iteam.status !='ENABLE':continue
            if iteam.topicSW=='ENABLE':
                topictype.append(iteam.id)
            elif iteam.copySW=='ENABLE':
                copytype.append(iteam.id)
        if topictype==[] or copytype==[]:
            return '文案类型有误'
        prompttextsum= await PromptText.all()
        if len(prompttextsum)==0:
            return '未添加提示词'
        topiccopysum=await TopicCopy.all()
        topictext=[]
        copytext=[]
        for iteam in topiccopysum:
            if iteam.status !='ENABLE':continue
            if iteam.TypeText_id in topictype:
                topictext.append(iteam.id)
            if iteam.TypeText_id in copytype:
                copytext.append(iteam.id)
        if topictext==[]:
            return '选题为空'
        if copytext==[]:
            return '样本为空'
        topiccopylist=[]
        for topic in topictext:
            for copy in copytext:
                for prompttext in prompttextsum:
                    topiccopylist.append([topic,copy,prompttext.id])
        script_data=CreatScript(
            AccountTeamlist=AccountTeams,
            topiccopylist= topiccopylist)
        await creatScripts(script_data)

async def getScript(publishTime,AccountTeam_id,ReleasePlan_id):
    iteam = await Script.filter(AccountTeam_id=AccountTeam_id, publishtime=publishTime )
    if iteam:
        return
    print("未找到匹配的任务")
    iteams = await Script.filter(AccountTeam_id=AccountTeam_id,publishtime=None)
    if iteams==[]:
        await creatScriptinfo(AccountTeam_id)
        iteams = await Script.filter(AccountTeam_id=AccountTeam_id,publishtime=None)
    if iteams:
        iteam= random.choice(iteams)
        Scripting = await Script.get(id=iteam.id)
        Scripting.publishtime=publishTime
        Scripting.ReleasePlan_id=ReleasePlan_id
        await Scripting.save()
        return
    raise ValueError(f"无法为 AccountTeam_id={AccountTeam_id} 创建有效的 Script")

@Script_api.get("/addScript", summary='批量添加脚本', description='功能描述')
async def addScript():
    owners = await TeamOwner.filter(status='ENABLE') .values('id','clipSum')
    now = datetime.now()
    today = now.date()
    plans = await ReleasePlan.all().values('id', 'hour', 'minute')
    async with in_transaction():
        for owner in owners:
            print(owner)
            clipSum= owner['clipSum']
            
            if clipSum==0:continue
            Days=math.ceil(clipSum/20/len(plans))
            if Days>28:Days=28
            print(Days)
            teams = await AccountTeam.filter(TeamOwner_id=owner['id'],status='ENABLE') .values('id')
            print(teams)
            for days in range(0, Days):
                for plan in plans:
                    for team in teams:
                        date = today + timedelta(days=days)
                        time_value = time(plan['hour'], plan['minute'])
                        publishtime_naive  = datetime.combine(date, time_value)
                        tz = timezone(timedelta(hours=8))
                        publishtime_bj = publishtime_naive.replace(tzinfo=tz)
                        publishtime = publishtime_bj.astimezone(timezone.utc)
                        now_utc = datetime.now(timezone.utc)
                        if publishtime < now_utc:continue
                        await getScript(publishtime,team['id'],plan['id'])
    return ResponseModel(
        code="000000",
        mesg="添加任务成功",
        time=str(datetime.now()),
        data=True)

@Script_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Script, {"id": id}, "删除成功")