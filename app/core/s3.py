from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from app.config import get_settings

settings = get_settings()

class S3Client:
    def __init__(self):
        self.config = {
            "aws_access_key_id": settings.s3_access_key,
            "aws_secret_access_key": settings.s3_secret_key,
            "endpoint_url": settings.s3_endpoint,
            "region_name": settings.s3_region,
        }
        self.bucket_name = settings.s3_bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(self, file_data, object_name: str, content_type: str):
        async with self.get_client() as client:
            # Проверяем, существует ли бакет, если нет - создаем (только для локальной разработки)
            # В продакшене бакет должен быть создан заранее
            try:
                await client.head_bucket(Bucket=self.bucket_name)
            except Exception:
                # Если бакета нет, создаем его
                await client.create_bucket(Bucket=self.bucket_name)

            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_data,
                ContentType=content_type
            )
            return object_name

    async def get_file_url(self, object_name: str):
        """Генерация временной ссылки (Presigned URL) для скачивания"""
        async with self.get_client() as client:
            try:
                url = await client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': self.bucket_name, 'Key': object_name},
                    ExpiresIn=3600 # Ссылка живет 1 час
                )
                return url
            except Exception as e:
                print(f"Error generating presigned URL: {e}")
                return None

    async def delete_file(self, object_name: str):
        async with self.get_client() as client:
            await client.delete_object(Bucket=self.bucket_name, Key=object_name)

s3_client = S3Client()
