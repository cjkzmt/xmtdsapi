from fastapi import APIRouter,Query,Request, HTTPException, Header, Response , Depends
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from time import sleep
from typing import Optional,List,Union, Dict
from .response_model import ResponseModel
from .models import *
from .auth import *
from tortoise.query_utils import Prefetch
import tortoise.exceptions 
Script_api = APIRouter()
class Scriptin(BaseModel):
    id: Optional[int] = None
    VideoTemplate:  Optional[str] = None
    Template_id:Optional[str] = None
    batch: Optional[Union[str, int]] = None
    status: Optional[str] = "Unfinished"
    number: Optional[str] = None
    title: Optional[str] = None
    covercopy: Optional[str] = None
    visualcopy: Optional[str] = None
    subtitlecopy: Optional[str] = None
    displaysubtitles: Optional[str] = None
    subtitlepronunciation: Optional[str] = None
    VideoClips: Optional[str] = None
    Font: Optional[str] = None
    Music: Optional[str] = None
    VoiceOver: Optional[str] = None
    operator: Optional[str] = None
    updatedTime: Optional[str] = None
    Computer: Optional[str] = None
    computerTime: Optional[str] = None
    publishtime: Optional[str] = None
@Script_api.post("/saveOrUpdate", summary='添加或更改', description='功能描述')
async def saveOrUpdate(script_in: Scriptin):
    if script_in.id is None:
        videotemplate, created = await VideoTemplate.get_or_create(name=script_in.VideoTemplate)
        if script_in.number is None:
            while True:
                try:
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    key = script_in.Template_id + timestamp
                    num = generate_short_str(key)
                    script = await Script.get(number=num)
                    sleep(0.1)
                except Exception as e:
                    print(f"停止重试，原因: {e}")
                    break
        else:
            num = script_in.number
            if  await Script.filter(number=num).exists():
                return ResponseModel[str](
                    code="000000",
                    mesg="创建失败，编号重复",
                    time=str(datetime.now()),
                    data=script_in.number
                )
        if script_in.VoiceOver:
            try:
                voiceover=await VoiceOver.get(name=script_in.VoiceOver)
            except:
                script_in.VoiceOver=  None
        script=await Script.create(
            number=num,
            Template_id=script_in.Template_id,
            VideoTemplate_id=videotemplate.id,
            batch=script_in.batch,
            status=script_in.status,
            Font_id=(await Font.get(name=script_in.Font)).id if script_in.Font else None,
            Music_id=(await Music.get(name=script_in.Music)).id if script_in.Music else None,
            VoiceOver_id=voiceover.id if script_in.VoiceOver else None,
            title=script_in.title,
            covercopy=script_in.covercopy,
            displaysubtitles=script_in.displaysubtitles,
            subtitlecopy=script_in.subtitlecopy,
            subtitlepronunciation=script_in.subtitlepronunciation,
            publishtime=script_in.publishtime
            )
        return ResponseModel[str](
        code="000000",
        mesg="创建成功",
        time=str(datetime.now()),
        data=script.number
    )
    Scripting = await Script.get(id=script_in.id)
    if script_in.title is not None:
        Scripting.title=script_in.title
    if script_in.covercopy is not None:
        Scripting.covercopy=script_in.covercopy
    if script_in.visualcopy is not None:
        Scripting.visualcopy=script_in.visualcopy
    if script_in.subtitlecopy is not None:
        Scripting.subtitlecopy=script_in.subtitlecopy
    if script_in.displaysubtitles is not None:
        Scripting.displaysubtitles=script_in.displaysubtitles
    if script_in.subtitlepronunciation is not None:
        Scripting.subtitlepronunciation=script_in.subtitlepronunciation
    if script_in.VideoClips is not None:
        try:
            videoclips = await VideoClips.get(name=script_in.VideoClips)
            Scripting.VideoClips_id = videoclips.id
        except tortoise.exceptions.DoesNotExist:
            # 处理字体不存在的情况，例如创建新字体或返回错误提示
            return ResponseModel[str](
                code="111111",
                mesg=f"素材 {script_in.VideoClips} 不存在",
                time=str(datetime.now()),
                data=None
            )
    if script_in.Font is not None:
        try:
            font = await Font.get(name=script_in.Font)
            Scripting.Font_id = font.id
        except tortoise.exceptions.DoesNotExist:
            # 处理字体不存在的情况，例如创建新字体或返回错误提示
            return ResponseModel[str](
                code="111111",
                mesg=f"字体 {script_in.Font} 不存在",
                time=str(datetime.now()),
                data=None
            )
    if script_in.Music is not None:
        music = await Music.get(name=script_in.Music)
        Scripting.Music_id=music.id
    if script_in.VoiceOver is not None:
        voiceover = await VoiceOver.get(name=script_in.VoiceOver)
        Scripting.VoiceOver_id=voiceover.id 
    if script_in.operator is not None:
        operator, created = await User.get_or_create(name=script_in.operator)
        Scripting.operator_id=operator.id
        Scripting.updatedTime=datetime.now()
    if script_in.Computer is not None:
        computer, created = await Computer.get_or_create(name=script_in.Computer)
        Scripting.Computer_id=computer.id
        Scripting.computerTime=datetime.now()
    
    await Scripting.save()
    return ResponseModel[str](
        code="000000",
        mesg="修改成功",
        time=str(datetime.now()),
        data=Scripting.number
    )
class Responsepici(BaseModel):
    pici: int
    data:  Union[List[Scriptin], Scriptin, bool]=[]






@retry(stop=stop_after_attempt(3), wait=wait_fixed(1), retry=retry_if_exception_type(tortoise.exceptions.OperationalError))
async def safe_query(filters):
    return await Script.filter(**filters).all().prefetch_related(
        "VideoTemplate",
        "Font",
        "Music",
        "VoiceOver",
        "operator",
        "Computer",
        "VideoClips"
    )

@Script_api.get("/", summary='查询 Script', description='根据 id, url, Author_id, update, status 查询')
async def query_url_author(Script_in: Scriptin = Depends()):
    if 'batch' in Script_in.model_dump().keys()and Script_in.batch == 'max':
        batchs = await Script.all().values('batch')
        pici = max((script['batch'] for script in batchs), default=1)
        Script_in.batch = pici
    filters = {k: v for k, v in Script_in.model_dump().items() if v is not None}
    Scripts = await safe_query(filters)
    chain = [
        Scriptin(
            id=script.id,
            VideoTemplate=script.VideoTemplate.name if script.VideoTemplate else None, 
            Template_id=script.Template_id,
            batch=script.batch,
            status=script.status,
            number=script.number,
            title=script.title,
            covercopy=script.covercopy,
            visualcopy=script.visualcopy,
            subtitlecopy=script.subtitlecopy,
            displaysubtitles=script.displaysubtitles,
            subtitlepronunciation=script.subtitlepronunciation,
            VideoClips=script.VideoClips.name if script.VideoClips else None,
            Font=script.Font.name if script.Font else None,
            Music=script.Music.name if script.Music else None,
            VoiceOver=script.VoiceOver.name if script.VoiceOver else None,
            operator=script.operator.name if script.operator else None,
            updatedTime=script.updatedTime.strftime("%Y-%m-%d %H:%M:%S") if script.updatedTime else None,
            Computer=script.Computer.name if script.Computer else None,
            computerTime=script.computerTime.strftime("%Y-%m-%d %H:%M:%S") if script.computerTime else None,
        )
        for script in Scripts
    ]

    return ResponseModel(
        code="000000",
        mesg="查询-脚本-成功",
        time=str(datetime.now()),
        data=chain
    )

