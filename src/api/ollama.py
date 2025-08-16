
from src.utils.request import *

def getOllama(data):
    result = request(Request(
        method='POST',
        url='/api/ollama/getPages',
        data=data
    ))
    return result

def Updateollama(data):
    result = request(Request(
        method='POST',
        url='/api/ollama/saveOrUpdate',
        data=data
    ))
    return result

def Updatesollama():
    result = request(Request(
        method='get',
        url='/api/ollama/Updates',
    ))
    return result











# 示例用法
def getollama():
    result = request(Request(
        method='GET',
        url='/api/ollama/getAll',
    ))
    return result


def getAllUrl():
    result = request(Request(
        method='GET',
        url='/api/ollama/getAllUrl',
    ))
    return result

def UpdateollamaUrl(data):
    result = request(Request(
        method='POST',
        url='/api/ollama/saveOrUpdate',
        data=data
    ))
    return result
def deleteollama(id):
    result = request(Request(
        method='DELETE',
        url=f'/api/ollama/{id}',
    ))
    return result

def UpdateUrl(data):
    result = request(Request(
        method='POST',
        url='/api/ollama/UpdateUrl',
        data=data
    ))
    return result
def ollama(id):
    result = request(Request(
        method='POST',
        url='/api/ollama/deleteoUrl',
    ))
    return result


