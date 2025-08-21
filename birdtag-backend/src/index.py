# src/index.py (最终健壮版)

import oss2
import json
import os
import uuid
import logging

# 获取一个 logger 实例，用于记录日志
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    # API 网关会将所有请求信息封装在 event 中
    # 我们需要从 event 中解析出 HTTP method
    # event['requestContext']['http']['method'] 是推荐的获取方式
    http_method = event.get('requestContext', {}).get('http', {}).get('method', 'GET').upper()
    
    # 定义通用的跨域响应头
    headers = {
        'Access-Control-Allow-Origin': '*', 
        'Access-Control-Allow-Headers': 'Content-Type,Authorization', # 允许 Content-Type 和未来的 Authorization 头
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
    }

    # 1. 关键：处理浏览器的 OPTIONS 预检请求
    # 如果请求方法是 OPTIONS，我们直接返回一个成功的空响应，表示“允许”
    if http_method == 'OPTIONS':
        logger.info("Handling OPTIONS preflight request.")
        return {
            "statusCode": 204, # 204 No Content 是处理预检请求的标准实践
            "headers": headers
        }

    # 2. 如果不是 OPTIONS，那么就是我们期望的 POST 请求，继续执行业务逻辑
    if http_method == 'POST':
        try:
            # 从环境变量中获取 Bucket 名称
            bucket_name = os.environ.get('BUCKET_NAME')
            if not bucket_name:
                raise ValueError("Server internal error: BUCKET_NAME not configured.")

            # 从 FC 的上下文中获取临时访问凭证
            creds = context.credentials
            auth = oss2.StsAuth(creds.access_key_id, creds.access_key_secret, creds.security_token)
            
            region = context.region
            # 使用内网 endpoint 更快、更省钱
            endpoint = f'https://oss-{region}-internal.aliyuncs.com'
            bucket = oss2.Bucket(auth, endpoint, bucket_name)
            
            # 解析请求体
            body_str = event.get("body", "{}")
            body = json.loads(body_str) if body_str else {}
            file_name = body.get('fileName')
            content_type = body.get('contentType', 'application/octet-stream') # 如果前端没传，给个默认值
            
            if not file_name:
                raise ValueError("fileName is required in the request body.")
            
            # 生成唯一的 object key
            object_key = f"uploads/{uuid.uuid4()}_{file_name}"
            
            # 生成预签名 URL，有效期 300 秒
            # 关键：签名时必须包含 Content-Type header，否则 PUT 上传会 403 Forbidden
            signed_url = bucket.sign_url('PUT', object_key, 300, headers={'Content-Type': content_type})

            logger.info(f"Successfully generated signed URL for {object_key}")
            
            return {
                "statusCode": 200,
                "headers": headers,
                "body": json.dumps({
                    "uploadUrl": signed_url,
                    "fileId": object_key
                })
            }
        
        except json.JSONDecodeError:
            error_message = "Invalid JSON format in request body."
            logger.error(error_message)
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"error": error_message})}
        except ValueError as e:
            error_message = str(e)
            logger.error(f"Value error: {error_message}")
            return {"statusCode": 400, "headers": headers, "body": json.dumps({"error": error_message})}
        except Exception as e:
            error_message = "An unexpected server error occurred."
            logger.error(f"An unexpected error occurred: {str(e)}", exc_info=True)
            return {"statusCode": 500, "headers": headers, "body": json.dumps({"error": error_message})}
    
    # 3. 如果是其他方法 (GET, PUT等)，我们不支持
    logger.warning(f"Unsupported HTTP method: {http_method}")
    return {
        "statusCode": 405, # 405 Method Not Allowed
        "headers": headers,
        "body": json.dumps({"error": "Method Not Allowed"})
    }