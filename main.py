import os
import shutil
from typing import List
from pydantic import BaseModel
from src.preview import Preview
from src.eduxtract import EduXtract
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File
from src.session_manager import Session_Manager
from fastapi.responses import FileResponse



app = FastAPI()
os.makedirs("uploads", exist_ok=True)
os.makedirs("previews", exist_ok=True)
os.makedirs("outputs", exist_ok=True)
app.mount("/previews", StaticFiles(directory="previews"), name="previews")

sessions = Session_Manager()


class XtractRequest(BaseModel):
    key_id: str
    read_latex: bool
    threshold: float
    outputs: List[str]

class DownloadRequest(BaseModel):
    key_id: str




@app.get("/")
async def index():
    return {"message":"EduXtract"}


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file to the "uploads" directory
    file_path = f"uploads/{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    key_id = await generate_preview(file_path)
    session = sessions.create_session(key_id)
    session.filepath = file_path
    session.xtract = EduXtract(filename=file_path, output_dir="outputs")
    info = session.xtract.get_info()
    preview_images = [f"/previews/{key_id}/{file}" for file in os.listdir(f"previews/{key_id}")]
    return {
        "key_id": key_id,
        "analysis_data": info,
        "preview_images": preview_images
    }

@app.post('/xtract')
async def xtract(request:XtractRequest):
    # request = {
    #     "key_id": "",
    #     "read_latex": "",
    #     "threshold": "",
    #     "outputs": ["docx", "csv", "excel"]
    # }
    session = sessions.get_session(request.key_id)
    session.xtract.threshold = request.threshold
    session.xtract.write_files(request.outputs)
    session.output_filepath = session.xtract.output_filepath
    session.output_filename = session.xtract.zipfilename
    exists = os.path.exists(session.xtract.output_filepath)

    return {"status": exists}

@app.post("/download")
async def download_file(request: DownloadRequest):
    session = sessions.get_session(request.key_id)
    if os.path.exists(session.output_filepath):
        return FileResponse(session.output_filepath, media_type='application/zip', filename= session.output_filename)




async def generate_preview(file_path:str):
    preview = Preview(filepath=file_path)
    preview.gen_preview()
    filename = preview.preview_file_name
    shutil.move(filename, "previews")
    return filename





