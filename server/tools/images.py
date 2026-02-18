from fastapi import UploadFile
from imagekitio import ImageKit
from core.config import settings

imagekit = ImageKit(
    private_key=settings.IMAGEKIT_PRIVATE_KEY
)
PUBLIC_ENDPOINT = settings.IMAGEKIT_PUBLIC_KEY,
URL_ENDPOINT = settings.IMAGEKIT_URL_ENDPOINT
# class ImageService:
#     @staticmethod
#     def upload_image(file:UploadFile, folder:str):
#         content = file.file.read()