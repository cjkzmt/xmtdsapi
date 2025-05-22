
import jwt
import json
from datetime import datetime, timedelta,timezone
import os
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import DecodeError, InvalidTokenError

outh2_scheme=OAuth2PasswordBearer(tokenUrl="token")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15"))
ALGORITHM=os.getenv("ALGORITHM", "HS256")
SECRET_KEY=os.getenv("SECRET_KEY", "dac0dae442692f77885fd9ff411a8cc2c822c9ac065a47439e3364c66d81cf54")
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))  # 默认 7 天

def create_user_token(data: dict):
    # 复制原始数据
    to_encode = data.copy()
    
    # 设置 access_token 的过期时间
    access_token_expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({
        "exp": access_token_expire_time,
        "token_type": "Bearer",
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 转换为秒
    })

    # 设置 refresh_token 的过期时间（更长）
    refresh_token_expire_time = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token_payload = {
        "user_id": data["user_id"],
        "exp": refresh_token_expire_time,
        "token_type": "refresh"
    }
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # 生成 access_token
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # 返回结构化的 token 响应
    return json.dumps({
        "access_token": access_token,
        "token_type": to_encode["token_type"],
        "refresh_token": refresh_token,
        "expires_in": to_encode["expires_in"],
        "user_id": to_encode.get("user_id")  # 假设 user_id 在 data 中已提供
    })
def get_user_token(token:str):
    try:
        payload=jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
            )
        return payload
    except jwt.DecodeError:
        raise ValueError("无法解码 token，请提供有效的 token")
    except jwt.ExpiredSignatureError:
        raise ValueError("token 已过期")
    except jwt.InvalidTokenError:
        raise ValueError("无效的 token 签名")
    except Exception as e:
        raise ValueError(f"token 解析失败: {str(e)}")


def verify_refresh_token(refresh_token: str):
    try:
        # 解码 refresh_token
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # refresh_token 过期
        return None
    except jwt.InvalidTokenError:
        # refresh_token 无效
        return None

def get_new_access_token(refresh_token: str):
    # 验证 refresh_token
    try:
        # print(refresh_token)
        payload = verify_refresh_token(refresh_token)
        if payload is None:
            raise ValueError("无效的 refresh_token 或 refresh_token 已过期")
        
        # 从 payload 中提取必要的数据，但不包括 refresh_token
        # print(payload)
        id = payload.get("user_id")
        
        # 生成新的 access_token
        new_access_token = create_user_token(data={"user_id": id})
        
        # 将 JSON 字符串转换为字典返回
        return json.loads(new_access_token)
    except Exception as e:
        raise ValueError(f"无法生成新的 access_token: {str(e)}")


if __name__ == "__main__":
    # 测试
    
    # access_token = create_user_token(data={"user_id": "1"})
    # token_data = json.loads(access_token)
    # refresh_token=token_data.get("refresh_token")
    # print(refresh_token)
    # print(token_data.get("expires_in"))

    print(get_new_access_token("refresh_token"))
