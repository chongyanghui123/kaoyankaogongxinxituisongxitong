import os
import uuid
from typing import Optional
import oss2
from config import settings


class OSSUploader:
    """阿里云OSS文件上传工具类"""
    
    def __init__(self):
        self.enabled = getattr(settings, 'OSS_ENABLED', False) and os.environ.get('OSS_ENABLED', '').lower() == 'true'
        
        if self.enabled:
            self.access_key_id = getattr(settings, 'OSS_ACCESS_KEY_ID', None) or os.environ.get('OSS_ACCESS_KEY_ID', '')
            self.access_key_secret = getattr(settings, 'OSS_ACCESS_KEY_SECRET', None) or os.environ.get('OSS_ACCESS_KEY_SECRET', '')
            self.bucket_name = getattr(settings, 'OSS_BUCKET_NAME', None) or os.environ.get('OSS_BUCKET_NAME', '')
            self.endpoint = getattr(settings, 'OSS_ENDPOINT', None) or os.environ.get('OSS_ENDPOINT', '')
            self.region = getattr(settings, 'OSS_REGION', None) or os.environ.get('OSS_REGION', '')
            
            if self.access_key_id and self.bucket_name and self.endpoint:
                auth = oss2.Auth(self.access_key_id, self.access_key_secret)
                self.bucket = oss2.Bucket(auth, self.endpoint, self.bucket_name)
            else:
                self.enabled = False
    
    def upload_file(self, file_data: bytes, file_name: str, content_type: str = 'application/octet-stream') -> Optional[str]:
        """
        上传文件到OSS
        
        Args:
            file_data: 文件二进制数据
            file_name: 文件名（不含路径）
            content_type: 文件MIME类型
            
        Returns:
            OSS上的文件URL，失败返回None
        """
        if not self.enabled:
            return None
        
        try:
            # 生成唯一文件名
            ext = os.path.splitext(file_name)[1]
            unique_name = f"{uuid.uuid4()}{ext}"
            
            # 上传文件
            self.bucket.put_object(unique_name, file_data, headers={'Content-Type': content_type})
            
            # 返回文件URL
            return f"https://{self.bucket_name}.{self.endpoint}/{unique_name}"
            
        except Exception as e:
            print(f"OSS上传失败: {str(e)}")
            return None
    
    def delete_file(self, file_url: str) -> bool:
        """
        删除OSS上的文件
        
        Args:
            file_url: 文件URL
            
        Returns:
            是否删除成功
        """
        if not self.enabled:
            return False
        
        try:
            # 从URL中提取文件名
            file_name = file_url.split(f"https://{self.bucket_name}.{self.endpoint}/")[-1]
            if file_name:
                self.bucket.delete_object(file_name)
                return True
            return False
            
        except Exception as e:
            print(f"OSS删除失败: {str(e)}")
            return False


# 创建全局OSS上传实例
oss_uploader = OSSUploader()
