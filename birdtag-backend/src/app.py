import os
import uuid
import json
import logging
from typing import Optional

import oss2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from urllib.request import Request, urlopen

from dotenv import load_dotenv
load_dotenv()  # 让 .env 生效

log = logging.getLogger("presign")
logging.basicConfig(level=logging.INFO)

OSS_BUCKET   = os.getenv("OSS_BUCKET")
OSS_ENDPOINT = os.getenv("OSS_ENDPOINT")
# -------------------------------------------

# 生产环境强烈建议：后端运行在绑定了 RAM 角色/STS 的环境
# 这里提供：环境变量 -> 元数据服务(100.100.100.200) 的兜底链
def get_sts():
    ak  = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")     or os.getenv("OSS_AK")
    sk  = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET") or os.getenv("OSS_SK")
    tok = os.getenv("ALIBABA_CLOUD_SECURITY_TOKEN")    or os.getenv("OSS_TOKEN")

    if not (ak and sk and tok):
        # ECS/函数计算/ACK 等拥有实例元数据服务时可自动取到 STS
        try:
            role_base = "http://100.100.100.200/latest/meta-data/ram/security-credentials/"
            role_name = urlopen(Request(role_base), timeout=1).read().decode().strip()
            resp = urlopen(Request(role_base + role_name), timeout=1).read().decode()
            j = json.loads(resp)
            ak, sk, tok = j["AccessKeyId"], j["AccessKeySecret"], j["SecurityToken"]
            log.info("STS fetched from metadata.")
        except Exception as e:
            log.warning("No metadata STS: %s", e)

    # 若仍然没有 token，则用长 AK/SK（仅本地开发可用，不要放前端）
    if ak and sk and not tok:
        log.warning("Using long AK/SK without token (dev only). Consider STS in prod.")
        auth = oss2.Auth(ak, sk)
        return auth, False

    if not (ak and sk and tok):
        raise HTTPException(status_code=500, detail="STS credentials not available")

    auth = oss2.StsAuth(ak, sk, tok)
    return auth, True


class PresignReq(BaseModel):
    fileName: str
    contentType: Optional[str] = "application/octet-stream"


app = FastAPI(title="OSS Presign Service")
# CORS：开发期允许本地站点，生产改成你的域名白名单
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/presign")
def presign(req: PresignReq):
    if not req.fileName:
        raise HTTPException(400, "fileName required")

    content_type = req.contentType or "application/octet-stream"
    auth, is_sts = get_sts()
    bucket = oss2.Bucket(auth, OSS_ENDPOINT, OSS_BUCKET)

    object_key = f"uploads/{uuid.uuid4()}_{req.fileName}"
    # 方案A：把 Content-Type 纳入签名，前端 PUT 必须同值
    put_url = bucket.sign_url("PUT", object_key, 300, headers={"Content-Type": content_type})
    # 给前端一个 GET 预览（可选）
    get_url = bucket.sign_url("GET", object_key, 300)

    return {
        "uploadUrl": put_url,
        "key": object_key,
        "getUrl": get_url,
        "contentType": content_type,
        "viaSTS": is_sts,
    }
