
from src.task.Publish.PublishVideo import PublishVideo
from src.task.Text.Createline import Createline
from src.task.Text.Createtitle import Createtitle
from src.task.Text.Createcover import Createcover
from src.task.Text.Createreading import Createreading
from src.task.Video.CreateVideo import CreateVideo
from src.task.Video.Createwav import Createwav
from src.task.Video.CreateVideoCover import CreateVideoCover
from src.task.Video.CreateVideoSubtitle import CreateVideoSubtitle
from src.task.Video.ClipSynthesis import ClipSynthesis
from src.utils.Ffmpeg import *

from dotenv import load_dotenv
load_dotenv()
GPU_SUPPORTED = CheckPC()  # 直接使用模块级变量
if not GPU_SUPPORTED: print("注意：将使用CPU模式运行...")
Info={'id': 13, 'VideoTemplateId': None, 'VideoTemplate': None, 'topicId': 92, 'topictext': '这房子我住了二十年，感情深，但确实老了。\n这次花了3个月翻新，我提了几个硬要求：冬天不用抖，夏天不用扇；能种花、能种菜；朋友来了能坐下吃顿热乎饭，烤串也顺手。\n我不管材料、不管工序，只认结果。\n最后交钥匙那天，师傅说：‘以后两年里，哪儿不舒服，一个电话。’\n我算了笔账——按现在的工价和材料，如果我自己一样样去跑，花的钱和时间，远不止现在这样省心。\n现在每天推门进来，心里只有一句话：早知道能这么舒服，早该弄了。', 'copyId': 33, 'copytext': '中年男人一生的执念：回村建房。一位老板放下生意，亲自守着砌起八百平新房。他说这房子是他的乐高，想要阳光、空气和水融入家中。他拒绝浮夸装饰，只要童年的星空与回忆。城市是舞台，他只想回乡做观众。那天，我们沉默着抬头，看见同一片久违的星空。每个人心里都有一个不曾远离的老家，一片渴望唤醒的星空。', 'PromptTextId': 1, 'promptText': '请根据下述的语言习惯和语气，帮我改写一条短视频口插稿，要求用选题项给出的内容替换下述的短视频文案样本知识点，但保留文案的语言习惯和内容结构。只需要纯文字文案。短视频文案样本：', 'draftitle': None, 'title': '二十年旧房大改造，从寒冬酷暑到四季如春，暖地凉台、宽敞饭厅，师傅承诺两年内随时上门维修，省心省力，住进梦想之家！', 'AccountTeamId': 3, 'AccountTeam': 101, 'cover': '老房翻新住出新生活\n二十年家的蜕变从心开始', 'drafline': None, 'line': '二十年的家终于活明白了。\n\n这房子陪我熬过寒冬酷暑，老了。这次翻新，我就认死理儿：冬天暖气要烫手，夏天凉快得能盖被；阳台必须能种香菜小葱，饭厅得挤得下十个人涮火锅。工头问我选啥瓷砖、啥电线，我摆摆手：“你只管让我推门喊一声‘舒坦’。”\n\n交房那天，师傅把钥匙拍我手里：“两年内，哪儿硌应了，我连夜来修。”回头一算账——自己跑市场讨价还价，怕是工钱都抵不上耽误的工夫。\n\n现在每天进门，拖鞋往地暖上一踩就后悔：这日子，早该这么过啊。', 'linestatus': 'ENABLE', 'subtitle': '二十年的家终于活明白了\n这房子陪我熬过寒冬酷暑 老了\n这次翻新 我就认死理儿冬天暖气要烫手\n夏天凉快得能盖被\n阳台必须能种香菜小葱\n饭厅得挤得下十个人涮火锅\n工头问我选啥瓷砖 啥电线\n我摆摆手 你只管让我推门喊一声 舒坦\n交房那天 师傅把钥匙拍我手里 两年内\n哪儿硌应了 我连夜来修\n回头一算账 自己跑市场讨价还价\n怕是工钱都抵不上耽误的工夫\n现在每天进门 拖鞋往地暖上一踩就后悔这日子\n早该这么过啊\n关注我 我来帮你\n城里有楼 乡下有院', 'reading': '二十年的家终于活明白了\n这房子陪我熬过寒冬酷暑 老了\n这次翻新 我就认死理儿冬天暖气要烫手\n夏天凉快得能盖被\n阳台必须能种香菜小葱\n饭厅得挤得下十个人涮火锅\n工头问我选啥瓷砖 啥电线\n我摆摆手 你只管让我推门喊一声 舒坦\n交房那天 师傅把钥匙拍我手里 两年内\n哪儿硌应了 我连夜来修\n回头一算账 自己跑市场讨价还价\n怕是工钱都抵不上耽误的工夫\n现在每天进门 拖鞋往地暖上一踩就后悔这日子\n早该这么过啊\n关注我 我来帮你\n城里有楼 乡下有院', 'copystatus': 'ENABLE', 'FontId': 1, 'Font': '抖音美好体.otf', 'publishtime': '2025-07-26 11:00:00+00:00', 'TemplateId': '101_92_33_1', 'ReleasePlanId': None, 'operatorId': None, 'ComputerId': 1, 'videoname': None, 'videopath': None, 'videostatus': None, 'MusicId': 9, 'Music': '阳光甚好微风不噪.MP3', 'OverId': 4, 'Over': '第二，移民政策不一样，塞浦路斯1家2代。.MP3', 'speed': 1.2, 'TypeVideoId': 1, 'TypeVideo': '竖屏', 'videoheight': 1280, 'videowidth': 720, 'TypeCoverId': 1, 'TypeCover': '无框黑底', 'fixedtitle': '小院改造', 'TypeSubtitleId': 1, 'TypeSubtitle': '35黑白', 'fontsize': 35, 'fontcolor': '黑白', 'scope': '任丘', 'douyin': '未发布', 'sph': '未发布', 'kuaishou': '无账号', 'xiaohongshu': '无账号', 'status': '视频待制作', 'createdTime': '2025-07-16 06:41:37.923727+00:00', 'updatedTime': '2025-07-26 07:57:57.323399+00:00'}
print("音频",Createwav(Info))
print("片段",ClipSynthesis(Info))
print("封面",CreateVideoCover(Info))
print('字幕',CreateVideoSubtitle(Info))
print("开始",CreateVideo(Info))

# from moviepy import*
# path=r'D:\新媒体大师\素材\视频请放这里\已用视频\142\0\xyq\7月23日 (1)_13.mp4'
# # clips=VideoFileClip(path)
# # print(clips.duration)
# ['D:\\新媒体大师\\素材\\视频请放这里\\已用视频\\142\\0\\xyq\\7月23日 (1)_13.mp4', 'D:\\新媒体大师\\素材\\视频请放这里\\已用视频\\142\\0\\xyq\\7月23日 (1)_24_Mirror.mp4'] 
# # D:\新媒体大师\素材\其他素材\音频\在这新年之际，祝大家新年快乐\欢迎您来看看我爸妈住了二十年的老屋.wav 4.18 D:\新媒体大师\素材\视频请放这里\已用视频\142\0.mp4
# cliplist=['儿推第十二课外劳宫-阳池认识0.mp4', '儿推第十二课外劳宫-阳池认识1']
# output_path=r'D:\新媒体大师\素材\视频请放这里\已用视频\142\17.mp4'
# # duration= 6.78 
# # Overpath=r'D:\新媒体大师\素材\其他素材\音频\在这新年之际，祝大家新年快乐\别总想着大富大贵 老屋亮堂 父母舒坦.wav'
# Merge(cliplist, output_path)
