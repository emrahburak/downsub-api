````markdown
# DownSub API

A simple FastAPI service that downloads YouTube video subtitles and extracts them as plain text files asynchronously.

---

## Overview

This service accepts a YouTube video URL, downloads its English subtitles (automatic or manual), converts them to plain text, and stores the result in a file linked to a unique task ID. You can query the processing result by task ID later.

---

## API Endpoints

### 1. Health Check

```http
GET /
````

* **Description:** Checks if the service is running.
* **Response:**

```json
{
  "status": "ok",
  "message": "subtitle extractor service running"
}
```

---

### 2. Submit Video for Subtitle Extraction

```http
POST /downsub
Content-Type: application/json
```

* **Request Body:**

```json
{
  "url": "https://www.youtube.com/watch?v=VIDEO_ID"
}
```

* **Response:**

```json
{
  "task_id": "unique_task_id_here",
  "status": "processing",
  "message": "Video processing started: https://www.youtube.com/watch?v=VIDEO_ID"
}
```

* **Description:** Submits a YouTube video URL for subtitle extraction. Returns a unique `task_id` to track progress.

---

### 3. Get Subtitle Extraction Result

```http
GET /downsub/result/{task_id}
```

* **Response (if processing complete):**

```json
{
  "task_id": "unique_task_id_here",
  "content": "Extracted subtitle plain text content ..."
}
```

* **Response (if still processing or not ready):**

```json
{
  "status": "processing"
}
```

* **Description:** Retrieve the extracted subtitle content by providing the `task_id` received at submission.

---

## How to Run

1. Clone the repository.

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

---

## Notes

* The service uses `yt-dlp` to download subtitles; please ensure `ffmpeg` is installed on your system for best results.
* Output subtitle text files are stored in the `output/` directory.
* The subtitle extraction process runs asynchronously in the background.

---

## Example `curl` Requests

### Submit a video:

```bash
curl -X POST "http://localhost:5000/downsub" \
     -H "Content-Type: application/json" \
     -d '{"url":"https://www.youtube.com/watch?v=LnX3B9oaKzw"}'
```

### Get result:

```bash
curl "http://localhost:5000/downsub/result/{task_id}"
```

Replace `{task_id}` with the actual ID returned from the POST request.

---

## License

MIT License


