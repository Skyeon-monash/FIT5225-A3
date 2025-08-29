#!/usr/bin/env python3
"""
配置腾讯云COS的CORS规则
"""
import os
from qcloud_cos import CosConfig, CosS3Client
from dotenv import load_dotenv

load_dotenv()

def setup_cors():
    # 获取环境变量
    bucket = os.getenv("COS_BUCKET")
    region = os.getenv("COS_REGION")
    secret_id = os.getenv("COS_SECRET_ID")
    secret_key = os.getenv("COS_SECRET_KEY")
    
    if not all([bucket, region, secret_id, secret_key]):
        print("错误: 请先配置环境变量")
        return
    
    # 配置客户端
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key,
        Scheme='https'
    )
    client = CosS3Client(config)
    
    # CORS配置
    cors_config = {
        'CORSRule': [
            {
                'ID': 'birdtag-cors',
                'AllowedOrigin': [
                    'http://localhost:5173',
                    'http://localhost:5174',
                    'http://127.0.0.1:5173',
                    'http://127.0.0.1:5174'
                ],
                'AllowedMethod': [
                    'PUT',
                    'GET',
                    'POST',
                    'DELETE',
                    'HEAD'
                ],
                'AllowedHeader': ['*'],
                'ExposeHeader': [
                    'ETag',
                    'x-cos-request-id'
                ],
                'MaxAgeSeconds': 300
            }
        ]
    }
    
    try:
        # 设置CORS配置
        response = client.put_bucket_cors(
            Bucket=bucket,
            CORSConfiguration=cors_config
        )
        print(f"CORS配置成功! Bucket: {bucket}")
        print(f"RequestId: {response.get('RequestId', 'N/A')}")
        
        # 验证配置
        cors_result = client.get_bucket_cors(Bucket=bucket)
        print("\n当前CORS配置:")
        for rule in cors_result['CORSRule']:
            print(f"- ID: {rule['ID']}")
            print(f"  允许的源: {rule['AllowedOrigin']}")
            print(f"  允许的方法: {rule['AllowedMethod']}")
            
    except Exception as e:
        print(f"CORS配置失败: {str(e)}")

if __name__ == "__main__":
    setup_cors()