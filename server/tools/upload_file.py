# # main.py
# from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
# from fastapi.responses import JSONResponse
# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from pydantic import BaseModel
# import httpx
# import os
# from datetime import datetime
# from typing import Optional

# # ────────────────────────────────────────────────
# #  CONFIG
# # ────────────────────────────────────────────────

# # IMAGEKIT_PRIVATE_KEY = os.getenv("IMAGEKIT_PRIVATE_KEY")      # ← your private key
# # IMAGEKIT_PUBLIC_KEY  = os.getenv("IMAGEKIT_PUBLIC_KEY")       # ← usually not needed for upload
# # IMAGEKIT_URL_ENDPOINT = "https://upload.imagekit.io/api/v1/files/upload"

# # DATABASE_URL = "sqlite:///./images.db"   # change to postgresql/mysql/etc in production

# # app = FastAPI(title="Image Upload → ImageKit → DB")

# # SQLAlchemy setup
# # engine = create_engine(DATABASE_URL, echo=False)
# # SessionLocal = sessionmaker(bind=engine)
# # Base = declarative_base()

# # class UploadedImage(Base):
# #     __tablename__ = "uploaded_images"

# #     id = Column(Integer, primary_key=True, index=True)
# #     original_filename = Column(String, nullable=False)
# #     imagekit_url = Column(String, nullable=False, index=True)
# #     file_id = Column(String, nullable=True)           # ImageKit fileId
# #     created_at = Column(DateTime, default=datetime.utcnow)

# # Base.metadata.create_all(bind=engine)

# # Pydantic response models



# # Dependency
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()

# # ────────────────────────────────────────────────
# #  IMAGEKIT UPLOAD FUNCTION
# # ────────────────────────────────────────────────

# async def upload_to_imagekit(file: UploadFile) -> dict:
#     if IMAGEKIT_PRIVATE_KEY is None:
#         raise HTTPException(500, "ImageKit private key not configured")

#     files = {
#         "file": (file.filename, await file.read(), file.content_type)
#     }

#     data = {
#         "fileName": file.filename,           # optional - can be overridden
#         # "folder": "/users/avatars/",       # optional
#         # "tags": "profile,2025",            # optional
#         # "useUniqueFileName": "true",
#     }

#     headers = {
#         "Authorization": f"Basic {IMAGEKIT_PRIVATE_KEY}"
#         # ImageKit uses private key in Basic Auth (username = private_key, password = empty)
#     }

#     async with httpx.AsyncClient() as client:
#         try:
#             resp = await client.post(
#                 IMAGEKIT_URL_ENDPOINT,
#                 files=files,
#                 data=data,
#                 headers=headers,
#                 timeout=25.0
#             )
#             resp.raise_for_status()
#             return resp.json()
#         except httpx.HTTPStatusError as e:
#             detail = e.response.json().get("message", "ImageKit upload failed")
#             raise HTTPException(status_code=e.response.status_code, detail=detail)
#         except Exception as e:
#             raise HTTPException(500, f"Upload error: {str(e)}")

# # ────────────────────────────────────────────────
# #  ENDPOINT
# # ────────────────────────────────────────────────

# @app.post("/upload-image/", response_model=ImageResponse)
# async def upload_image(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     # Optional: basic validation
#     allowed_types = {"image/jpeg", "image/png", "image/webp", "image/gif"}
#     if file.content_type not in allowed_types:
#         raise HTTPException(400, detail="Only JPEG, PNG, WebP, GIF allowed")

#     # 1. Upload to ImageKit
#     imagekit_response = await upload_to_imagekit(file)

#     # 2. Extract important fields
#     url = imagekit_response.get("url")
#     file_id = imagekit_response.get("fileId")

#     if not url:
#         raise HTTPException(500, "ImageKit did not return valid URL")

#     # 3. Save to database
#     db_image = UploadedImage(
#         original_filename=file.filename,
#         imagekit_url=url,
#         file_id=file_id,
#     )
#     db.add(db_image)
#     db.commit()
#     db.refresh(db_image)

#     return db_image


# @app.get("/images/{image_id}", response_model=ImageResponse)
# def get_image(image_id: int, db: Session = Depends(get_db)):
#     image = db.query(UploadedImage).filter(UploadedImage.id == image_id).first()
#     if not image:
#         raise HTTPException(404, "Image not found")
#     return image