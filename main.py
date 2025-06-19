from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from services.subtitle_extractor import process_video
from services.utils import clean_old_files, str_to_bool, generate_unique_id, find_txt_file_path_by_task_id
import os
from pathlib import Path

CLEANUP_ENABLED = str_to_bool(os.getenv("DOWNSUB_CLEANUP_ENABLED", "false"))
CLEANUP_AGE = int(os.getenv("DOWNSUB_CLEANUP_AGE", 86400))
RESULT_OPTION = os.getenv("RESULT_OPTION", "json").lower()

app = FastAPI()


@app.get("/")
def read_root():
    """
    TR: Servisin çalışma durumunu kontrol eder.
    EN: Checks the service health status.
    """
    return {"status": "ok", "message": "subtitle extractor service running"}


class VideoRequest(BaseModel):
    url: str
    sub_lang: Optional[str] = "en"


@app.post("/downsub")
async def submit_video(req: VideoRequest, background_tasks: BackgroundTasks):
    """
    TR: YouTube videosu işlenmek üzere kuyruğa alınır.
        Arka planda video işleme görevi başlatılır.
    
    Args:
        req (VideoRequest): İşlenecek video URL'sini içeren istek modeli.
        background_tasks (BackgroundTasks): Arka plan görevleri yönetimi.
    
    Returns:
        dict: task_id, durum ve bilgi mesajı içeren sözlük.
    EN: Queues a YouTube video for processing.
        Starts a background video processing task.
    
    Args:
        req (VideoRequest): Request model containing video URL.
        background_tasks (BackgroundTasks): Background task manager.
    
    Returns:
        dict: Dictionary containing task_id, status and message.
    """

    task_id = generate_unique_id()
    background_tasks.add_task(process_video, task_id, req.url, req.sub_lang)
    return {
        "task_id": task_id,
        "status": "processing",
        "message": f"Video processing started: {req.url}"
    }


@app.get("/downsub/result/{task_id}")
def get_result(task_id: str):
    """
    TR: Verilen task_id için altyazı dosyasını döner.
        Dosya bulunamazsa işlem devam ediyor mesajı verir.
    EN: Returns the subtitle file for the given task_id.
        If file not found, returns a processing status message.
    """

    if CLEANUP_ENABLED:
        clean_old_files(folder_path="output", max_age_seconds=CLEANUP_AGE)

   
    raw_path = find_txt_file_path_by_task_id(task_id, output_dir="output")
    if raw_path is None:
        return JSONResponse({"status": "processing"}, status_code=202)

    file_path = Path(raw_path)

    if not file_path or not os.path.exists(file_path):
        return JSONResponse({"status": "processing"}, status_code=202)


    if RESULT_OPTION == "json":
        with file_path.open("r", encoding="utf-8") as f:
            content = f.read()
        return JSONResponse({
            "task_id": task_id,
            "filename": f"{task_id}.txt",
            "content": content
        })
    else:
        full_path = find_txt_file_path_by_task_id(task_id, output_dir="output")

        if full_path:

            return FileResponse(path=full_path,
                                media_type="text/plain",
                                filename=os.path.basename(full_path))

        else:
            return JSONResponse({"status": "file_missing"}, status_code=404)
