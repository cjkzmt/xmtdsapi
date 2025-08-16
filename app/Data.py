from .models import *
from .db_connector import tortoise_tx
@tortoise_tx()
async def UpDataStatus(id):
    await Data.filter(id=id).update(status='ENABLE')