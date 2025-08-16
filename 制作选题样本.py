from src.api.urltext import geturltexts
from src.ExecuteTask.Executeurltext import Executeurltext
from dotenv import load_dotenv
load_dotenv()
while True:
    urltext=geturltexts()
    urltextList = urltext['data']['records']
    if urltextList==[]: break
    Executeurltext(urltextList,2)
