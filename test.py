import requests
import time


BASE_URL = "http://127.0.0.1:5000"



def test_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("[✓] Health check passed.")


def test_submit_video(youtube_url,sub_lang=None):


    payload = {"url":youtube_url}
    if sub_lang:
        payload["sub_lang"] = sub_lang

    response = requests.post(f"{BASE_URL}/downsub",json=payload)


    # check status

    assert response.status_code == 200, f"Beklenmeyen durum : {response.status_code} - {response.text}"


    data = response.json()

    assert "task_id" in data, "Yanıt içinde task_id yok!"
    assert data.get("status") == "processing" , f"Beklenen 'processing', gelen: {data.get('status')}"

    print(f"[✓] Video submitted. Task ID: {data['task_id']}")
    return data["task_id"]  # Bir sonraki adımda kullanılacak


def test_get_result(task_id: str, timeout: int = 60, interval: int = 5):
    print(f"[•] Sonuç bekleniyor (task_id: {task_id})...")
    start = time.time()

    while time.time() - start < timeout:
        response = requests.get(f"{BASE_URL}/downsub/result/{task_id}")
        assert response.status_code in (200, 202), f"Beklenmeyen status: {response.status_code}"

        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            data = response.json()
            if data.get("status") == "processing":
                print("[…] Hala işleniyor, bekleniyor...")
                time.sleep(interval)
            elif "content" in data:
                print("[✓] İçerik (JSON) alındı:")
                print(data["content"][:300], "...")
                return
            else:
                raise Exception(f"Beklenmeyen yanıt yapısı: {data}")
        
        elif "text/plain" in content_type:
            print("[✓] İçerik (TXT dosya) alındı:")
            print(response.text[:300], "...")
            return

        else:
            raise Exception(f"Beklenmeyen içerik türü: {content_type}")

    raise TimeoutError("İşlem belirtilen sürede tamamlanmadı.")


def run_batch_test(videos:list = []):
     for vid in videos:
        task_id = test_submit_video(vid["url"], sub_lang=vid["lang"])
        test_get_result(task_id)


if __name__ == "__main__":
    videos = [
        {"url":"https://www.youtube.com/watch?v=Qa8IfEeBJqk&t=1s", "lang":"en"},
        {"url":"https://www.youtube.com/watch?v=7mEztBsnEuo", "lang":"tr"}
    ]

    test_health_check()    
    run_batch_test(videos=videos)
