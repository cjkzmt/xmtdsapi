from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tortoise.expressions import Case, When,Q
from tenacity import retry, stop_after_attempt, wait_fixed
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import *
from .models import *
from .auth import *
from sqlalchemy import nullslast
import random
from tortoise.query_utils import Prefetch
from datetime import datetime, timedelta, time,timezone
from tortoise.transactions import in_transaction

Script_api = APIRouter()

class QueryCondition(Condition):
    AccountTeamId: Optional[int] = None
    Day:Optional[int] = 28
    unScriptIdList: Optional[list[int]] = None

class Item(BaseModel):
    id: Optional[int] = None
    VideoTemplateId:   Optional[int] = None
    VideoTemplate:  Optional[str] = None
    topicId:  Optional[int] = None
    topictext:  Optional[str] = None
    copyId:  Optional[int] = None
    copytext:  Optional[str] = None
    PromptTextId:  Optional[int] = None
    promptText:  Optional[str] = None
    draftitle: Optional[str] = None
    title:Optional[str] = None
    AccountTeamId:  Optional[int] = None
    AccountTeam:  Optional[int] = None
    cover: Optional[str] = None
    drafline: Optional[str] = None
    line: Optional[str] = None
    linestatus: Optional[str] = None
    subtitle: Optional[str] = None
    reading: Optional[str] = None
    copystatus: Optional[str] = None
    FontId: Optional[int] = None
    Font: Optional[str] = None
    publishtime: Optional[str] = None
    TemplateId: Optional[str] = None
    ReleasePlanId:  Optional[int] = None
    operatorId: Optional[int] = None
    ComputerId: Optional[int] = None
    videoname: Optional[str] = None
    videopath: Optional[str] = None
    videostatus: Optional[str] = None
    MusicId: Optional[int] = None
    Music: Optional[str] = None
    OverId: Optional[int] = None
    Over: Optional[str] = None
    speed:Optional[float] = None # 改成浮点数
    TypeVideoId: Optional[int] = None
    TypeVideo: Optional[str] = None
    videoheight: Optional[int] = None
    videowidth: Optional[int] = None
    TypeCoverId: Optional[int] = None
    TypeCover: Optional[str] = None
    fixedtitle: Optional[str] = None
    TypeSubtitleId: Optional[int] = None
    TypeSubtitle: Optional[str] = None
    fontsize: Optional[int] = None
    fontcolor: Optional[str] = None
    scope: Optional[str] = None
    douyin: Optional[str] = None
    sph: Optional[str] = None
    kuaishou: Optional[str] = None
    xiaohongshu: Optional[str] = None
    status: Optional[str] = None
    createdTime: Optional[str] = None
    updatedTime: Optional[str] = None

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
        ~Q(id__in=data.unScriptIdList))# &        
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
        if id in data.unScriptIdList:
            continue
        ComputerId=iteam.Computer_id
        updatedTime=iteam.updatedTime
        if updatedTime < task_time  and ComputerId is not None and ComputerId !=PC_id :continue
        if len(Script_tasks)> data.pageSize:break
        if iteam.videoname:
            if Publish_Video:
                if iteam.videstatus=='ENABLE':
                    Script_tasks.append({
                        'taskname':'Publish',
                        'ScriptId':iteam.id})
            continue
        if iteam.reading:
            if Create_Video:
                if iteam.copystatus=='ENABLE':
                    Script_tasks.append({
                    'taskname':'Video',
                    'ScriptId':iteam.id})
        if Create_Text:
            if iteam.line:
                if iteam.linestatus=='ENABLE':
                    if iteam.title is None:
                        Script_tasks.append({
                        'taskname':'title',
                        'ScriptId':iteam.id})
                    if iteam.cover is None:
                        Script_tasks.append({
                        'taskname':'cover',
                        'ScriptId':iteam.id})
                    if iteam.reading is None:
                        Script_tasks.append({
                        'taskname':'reading',
                        'ScriptId':iteam.id})
                continue
            Script_tasks.append({
                        'taskname':'line',
                        'ScriptId':iteam.id})
    for iteam in Script_tasks:
        Scripting= await Script.get(id=iteam['ScriptId'])
        Scripting.Computer_id=PC_id
        await Scripting.save()
    return ResponseModel(
            code="000000",
            mesg="获取成功",
            time=str(datetime.now()),
            data=Script_tasks)  

@Script_api.post("/getScriptPages", summary='分页查询用户数据', description='功能描述')
async def get_Script_pages(request: Request):
    data = await parse_request_body(request, QueryCondition)
    print(data)
    query = Script.filter().prefetch_related(
    "VideoTemplate", "topic", "copy", "PromptText", "Font", "Music", "Computer", "Over", 
    Prefetch("AccountTeam", queryset=AccountTeam.all().prefetch_related("TypeVideo", "TypeCover", "TypeSubtitle")),)
    query = condition(data,query)
    if data.AccountTeamId:
        query = query.filter(AccountTeam_id=data.AccountTeamId)
    if  data.getinfo and data.getinfo in 'ReviewScriptTaskReviewCopyReviewVideo脚本文案任务视频文案任务':
        print(data.getinfo)
        start_time = datetime.now(timezone.utc)
        end_time = datetime.now(timezone.utc).date()+ timedelta(days=data.Day)
        query = query.filter(publishtime__gt=start_time, publishtime__lt=end_time)
        if data.getinfo=='ReviewScript':
            query = query.filter(line__isnull=False,linestatus__not='ENABLE')
        if data.getinfo=='ReviewCopy':
            query = query.filter(linestatus='ENABLE',copystatus__not='ENABLE')
        if data.getinfo=='ReviewVideo':
            query = query.filter(videoname__isnull=False,videostatus__not='ENABLE')
        if data.getinfo=='脚本文案任务':
            query = query.filter(line__isnull=True,topic_id__isnull=False)
        if data.getinfo=='视频文案任务':
            query = query.filter(line__isnull=False,linestatus='ENABLE',reading__isnull=True,topic_id__isnull=False)
    total = await query.count()
    offset = (data.currentPage - 1) * data.pageSize
    annotated_query = query.annotate(
        publishtime_isnull=Case(
            When(publishtime__isnull=True, then=1),
            default=0
        )
    ).order_by("publishtime_isnull", "publishtime", "AccountTeam_id")
    Scripts = await annotated_query.offset(offset).limit(data.pageSize)
    iteams_info = []
    for iteam in Scripts:
        scope=accountTeam=TypeVideoId=TypeVideo=videoheight=videowidth=TypeCoverId=TypeCover=fixedtitle=TypeSubtitleId=TypeSubtitle=fontsize=fontcolor=None
        if iteam.AccountTeam:
            accountTeam=iteam.AccountTeam.number
            scope=iteam.AccountTeam.scope
            TypeVideoId=iteam.AccountTeam.TypeVideo_id
            TypeCoverId=iteam.AccountTeam.TypeCover_id
            TypeSubtitleId=iteam.AccountTeam.TypeCover_id
            if iteam.AccountTeam.TypeVideo:
                TypeVideo=iteam.AccountTeam.TypeVideo.name
                videoheight=iteam.AccountTeam.TypeVideo.videoheight
                videowidth=iteam.AccountTeam.TypeVideo.videowidth
            if iteam.AccountTeam.TypeCover:
                TypeCover=iteam.AccountTeam.TypeCover.name
                fixedtitle=iteam.AccountTeam.TypeCover.fixedtitle
            if iteam.AccountTeam.TypeSubtitle:
                TypeSubtitle=iteam.AccountTeam.TypeSubtitle.name
                fontsize=iteam.AccountTeam.TypeSubtitle.fontsize
                fontcolor=iteam.AccountTeam.TypeSubtitle.fontcolor
        iteams_info.append(Item(
            id=iteam.id,
            VideoTemplateId=iteam.VideoTemplate_id,
            VideoTemplate=iteam.VideoTemplate.name if iteam.VideoTemplate else None,
            topicId=iteam.topic_id,
            copyId=iteam.copy_id,
            PromptTextId=iteam.PromptText_id,
             topictext=iteam.topic.text if iteam.topic else None,
            copytext=iteam.copy.text if iteam.copy else None,
            promptText=iteam.PromptText.text if iteam.PromptText else None,
            title=iteam.title,
            AccountTeamId=iteam.AccountTeam_id,
            AccountTeam=accountTeam,
            scope=scope,
            TypeVideoId=TypeVideoId,
            TypeVideo=TypeVideo,
            videoheight=videoheight,
            videowidth=videowidth,
            TypeCoverId=TypeCoverId,
            TypeCover=TypeCover,
            fixedtitle=fixedtitle,
            TypeSubtitleId=TypeSubtitleId,
            TypeSubtitle=TypeSubtitle,
            fontsize=fontsize,
            fontcolor=fontcolor,
            cover=iteam.cover,
            drafline=iteam.drafline,
            line=iteam.line,
            linestatus=iteam.linestatus,
            subtitle=iteam.subtitle,
            reading=iteam.reading,   
            copystatus=iteam.copystatus,
            FontId=iteam.Font_id,
            Font=iteam.Font.name if iteam.Font else None,
            publishtime=str(iteam.publishtime) if iteam.publishtime else None,
            TemplateId=f'{str(iteam.AccountTeam.number)}_{str(iteam.topic_id)}_{str(iteam.copy_id)}_{str(iteam.PromptText_id)}' if iteam.topic and iteam.AccountTeam and iteam.copy and iteam.PromptText else None,
            ReleasePlanId=iteam.ReleasePlan_id,
            operatorId=iteam.operator_id,
            ComputerId=iteam.Computer_id,
            videoname=iteam.videoname,
            videopath=iteam.videopath,
            videostatus=iteam.videostatus,
            MusicId=iteam.Music_id,
            Music=iteam.Music.name if iteam.Music else None,
            OverId=iteam.Over_id,
            Over=iteam.Over.filename if iteam.Over else  None,
            speed=iteam.Over.speed if iteam.Over else  None,
            douyin=iteam.douyin,
            sph=iteam.sph,
            kuaishou=iteam.kuaishou,
            xiaohongshu=iteam.xiaohongshu,
            status=iteam.status,
            createdTime=str(iteam.createdTime),
            updatedTime=str(iteam.updatedTime)) )
    pages=(total + data.pageSize - 1) // data.pageSize if total > 0 else 0
    query_result = QueryResult(
        current=data.currentPage,
        hitcount=True,
        optimizeCountSql=False,
        orders=[], 
        pages=pages,
        records=iteams_info,
        searchCount=True,
        size=data.pageSize,
        total=total)
    return ResponseModel(
        code="000000",
        mesg="操作成功",
        time=str(datetime.now()),
        data=query_result)

@Script_api.post("/saveOrUpdate", summary='添加一个内容', description='功能描述')
async def saveOrUpdate(request: Request):
    async with in_transaction():
        Script_in = await parse_request_body(request, Item)
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
            if Script_in.FontId and Script_in.FontId>0:
                Scripting.Font_id = Script_in.FontId
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
            if  Script_in.MusicId and Script_in.MusicId>0:
                Scripting.Music_id = Script_in.MusicId
            if Script_in.OverId and Script_in.OverId>0:
                Scripting.Over_id = Script_in.OverId
            if Script_in.douyin:
                Scripting.douyin = Script_in.douyin
            if Script_in.sph:
                Scripting.sph = Script_in.sph
            if Script_in.kuaishou:
                Scripting.kuaishou = Script_in.kuaishou
            if Script_in.xiaohongshu:
                Scripting.xiaohongshu = Script_in.xiaohongshu
            await Scripting.save()
            return ResponseModel(code="000000", mesg="更新成功", time=str(datetime.now()), data=True)
        await creatOneScript(Script_in.AccountTeamId,publishtime=Script_in.publishtime,title=Script_in.title,videoname=Script_in.videoname)
        return ResponseModel(code="000000", mesg="添加成功", time=str(datetime.now()), data=True)

async def getAccountstatus(AccountTeamId,name,status=None):
    platform = await  Platform.get(name=name)
    account = await Account.filter(AccountTeam_id=AccountTeamId,platform_id=platform.id,status="ENABLE").first()
    x=  '已发布' if status == '已发布' else '未发布' if  account else '无账号'
    return x

class CreatScript(BaseModel):
    AccountTeamlist: List[int] #[87, 37, 4]
    topiccopylist: List[List[int]]  #[[87, 3], [87, 4]]

async def creatOneScript(AccountTeamId,topicid=None,copyid=None,PromptTextid=None,publishtime=None,title=None,videoname=None):
    await Script.create(
        topic_id=topicid ,
        copy_id=copyid,
        AccountTeam_id=AccountTeamId,
        PromptText_id=PromptTextid,
        publishtime=publishtime,
        title=title,
        videoname=videoname,
        douyin=await getAccountstatus(AccountTeamId,'抖音'),
        sph=await getAccountstatus(AccountTeamId,'视频号'),
        kuaishou=await getAccountstatus(AccountTeamId,'快手'),
        xiaohongshu=await getAccountstatus(AccountTeamId,'小红书'),
        status="待发布" if videoname else "脚本文案待制作")
async def creatScripts(Script_in:CreatScript):
    for AccountTeamId in Script_in.AccountTeamlist:
        for pair in Script_in.topiccopylist:
            if len(pair) != 3:
                continue
            topicid, copyid,PromptTextid = pair
            await creatOneScript(AccountTeamId,topicid=topicid,copyid=copyid,PromptTextid=PromptTextid)
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

async def getScript(publishTime,AccountTeamId,ReleasePlanId):
    try:
        iteam = await Script.get(AccountTeam_id=AccountTeamId, publishtime=publishTime )
        # print(f"找到{iteam.id}")
        return
    except Exception as e:
        if "does not exist" in str(e).lower():
            print("未找到匹配的任务")
        elif "multiple objects returned" in str(e).lower():
            print("找到多个匹配的任务，请检查数据唯一性约束")
    iteams = await Script.filter(AccountTeam_id=AccountTeamId,publishtime=None)
    if iteams==[]:
        # print("脚本不足创建脚本")
        await creatScriptinfo(AccountTeamId)
        iteams = await Script.filter(AccountTeam_id=AccountTeamId,publishtime=None)
    if iteams:
        iteam= random.choice(iteams)
        Scripting = await Script.get(id=iteam.id)
        Scripting.publishtime=publishTime
        Scripting.ReleasePlan_id=ReleasePlanId
        await Scripting.save()
        return
    raise ValueError(f"无法为 AccountTeamId={AccountTeamId} 创建有效的 Script")

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
    douyins=sphs=kuaishous=xiaohongshus='无账号'
    iteams = await Script.filter(publishtime__isnull=False,status__not='发布完成')
    print(len(iteams))
    for iteam in iteams:
        now = datetime.now(timezone.utc)
        if iteam.publishtime < now:
            print(f"任务{iteam.id}已过期")
            Scripting = await Script.get(id=iteam.id)
            Scripting.publishtime=None
            Scripting.ReleasePlan_id=None
            await Scripting.save()
            continue
        AccountTeamId=iteam.AccountTeam_id
        douyins = await getAccountstatus(AccountTeamId,'抖音',iteam.douyin)
        kuaishous =await getAccountstatus(AccountTeamId,'快手',iteam.kuaishou)
        sphs = await getAccountstatus(AccountTeamId,'视频号',iteam.sph)
        xiaohongshus = await getAccountstatus(AccountTeamId,'小红书',iteam.xiaohongshu)
        
        if '已发布' not  in  [douyins, sphs, kuaishous, xiaohongshus]:
            status = '视频待审核' if iteam.status == 'DISABLE' else '待发布'
            if iteam.videoname is None:
                status = '视频文案待审核' if iteam.status == 'DISABLE' else '视频待制作'
                if iteam.reading is None:
                    status = '脚本文案待审核' if iteam.status == 'DISABLE' else '视频文案待制作'
                    if iteam.line is None:
                        status = '脚本文案待制作'
        elif '未发布' not in [douyins, sphs, kuaishous, xiaohongshus]:
            status = '发布完成'
        
        Scripting = await Script.get(id=iteam.id)
        Scripting.status=status
        Scripting.sph=sphs
        Scripting.kuaishou=kuaishous
        Scripting.douyin=douyins
        Scripting.xiaohongshu=xiaohongshus
        await Scripting.save()
    return ResponseModel(
        code="000000",
        mesg="刷新任务成功",
        time=str(datetime.now()),
        data=True)

@Script_api.get("/addScript", summary='添加一个内容', description='功能描述')
async def addScript():
    teams = await AccountTeam.all().values('id')
    now = datetime.now()
    today = now.date()
    plans = await ReleasePlan.all().values('id', 'hour', 'minute')
    async with in_transaction():
        for days in range(0, 28):
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
    await RefreshTask()
    return ResponseModel(
        code="000000",
        mesg="添加任务成功",
        time=str(datetime.now()),
        data=True)

@Script_api.delete("/{id}",summary='删除指定内容',description='功能描述')
async def delete_iteam(id: int):
    return await delete(Script, {"id": id}, "删除成功")