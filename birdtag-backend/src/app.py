import os
import uuid
import logging
from typing import Optional

from qcloud_cos import CosConfig, CosS3Client
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from dotenv import load_dotenv
load_dotenv()  # 让 .env 生效

log = logging.getLogger("presign")
logging.basicConfig(level=logging.INFO)

COS_BUCKET = os.getenv("COS_BUCKET")
COS_REGION = os.getenv("COS_REGION")
COS_SECRET_ID = os.getenv("COS_SECRET_ID")
COS_SECRET_KEY = os.getenv("COS_SECRET_KEY")

def get_cos_client():
    """获取腾讯云COS客户端"""
    if not all([COS_BUCKET, COS_REGION, COS_SECRET_ID, COS_SECRET_KEY]):
        raise HTTPException(status_code=500, detail="COS credentials not configured")
    
    config = CosConfig(
        Region=COS_REGION,
        SecretId=COS_SECRET_ID,
        SecretKey=COS_SECRET_KEY,
        Scheme='https'
    )
    return CosS3Client(config)


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
    client = get_cos_client()

    object_key = f"uploads/{uuid.uuid4()}_{req.fileName}"
    
    try:
        # 生成预签名上传URL (PUT)
        put_url = client.get_presigned_url(
            Method='PUT',
            Bucket=COS_BUCKET,
            Key=object_key,
            Expired=300,  # 5分钟有效期
            Headers={'Content-Type': content_type}
        )
        
        # 生成预签名下载URL (GET)
        get_url = client.get_presigned_url(
            Method='GET',
            Bucket=COS_BUCKET,
            Key=object_key,
            Expired=300
        )

        log.info(f"Generated presigned URLs for: {object_key}")

        return {
            "uploadUrl": put_url,
            "key": object_key,
            "getUrl": get_url,
            "contentType": content_type,
            "viaSTS": False,  # 腾讯云COS使用密钥认证
        }
    
    except Exception as e:
        log.error(f"Failed to generate presigned URL: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate presigned URL: {str(e)}")
