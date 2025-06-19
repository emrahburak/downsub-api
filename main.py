from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import JSONResponse
from starlette.responses import FileResponse
from pydantic import BaseModel
import shortuuid
import os
from services.subtitle_extractor import process_video
from services.utils import clean_old_files
from typing import Optional


def str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1", "yes", "on")


CLEANUP_ENABLED = str_to_bool(os.getenv("DOWNSUB_CLEANUP_ENABLED", "false"))
CLEANUP_AGE = int(os.getenv("DOWNSUB_CLEANUP_AGE", 86400))
RESULT_OPTION = os.getenv("RESULT_OPTION", "file").lower()


def generate_unique_id():
    """
    TR: Benzersiz bir ID üretir.
    EN: Generates a unique ID.
    """
    return shortuuid.uuid()


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
    
    Args:
        task_id (str): İşlem kimliği.
    
    Returns:
        dict: task_id ve içerik veya işlem durum mesajı.
    EN: Returns the subtitle file for the given task_id.
        If file not found, returns processing status message.
    
    Args:
        task_id (str): Task identifier.
    
    Returns:
        dict: task_id and content or processing status message.
    """

    if CLEANUP_ENABLED:
        clean_old_files(folder_path="output", max_age_seconds=CLEANUP_AGE)

    file_path = f"output/{task_id}.txt"

    if not os.path.exists(file_path):
        return JSONResponse({"status": "processing"}, status_code=202)

    if RESULT_OPTION == "json":
        with open(file_path) as f:
            content = f.read()
        return JSONResponse({
            "task_id": task_id,
            "filename": f"{task_id}.txt",
            "content": content
        })
    else:
        return FileResponse(path=file_path,
                            media_type="text/plain",
                            filename=f"{task_id}.txt")
