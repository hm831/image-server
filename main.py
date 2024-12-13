from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import os
import uuid

app = FastAPI()

IMAGE_DIR = "/Users/yoru/Pictures/images"
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_image(file_path: str, file_name: str, file: UploadFile = File(...)):
    root_path = IMAGE_DIR + file_path
    os.makedirs(root_path, exist_ok=True)
    local_file_path = root_path + "/" + file_name
    with open(local_file_path, "wb") as f:
        f.write(await file.read())
    return {"filename": file_name, "url": f"/images{file_path}/{file_name}"}

@app.get("/images/{file_path:path}")
async def get_image(file_path: str):
    file_path = os.path.join(IMAGE_DIR, file_path)
    if not os.path.exists(file_path):
        return {"error": "File not found"}
    return FileResponse(file_path)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Image Server!"}
