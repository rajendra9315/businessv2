from fastapi import FastAPI, UploadFile, File
import shutil
import os

from services.analysis_service import analyze_file

app = FastAPI(title="Smart Business Analytics API")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/")
def root():
    return {"message": "Backend is running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_file(file_path)

    return result
