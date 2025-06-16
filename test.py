import requests
import time


BASE_URL = "http://127.0.0.1:5000"



def test_health_check():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    print("[✓] Health check passed.")


def test_submit_video(youtube_url):


    payload = {"url":youtube_url}

    response = requests.post(f"{BASE_URL}/downsub",json=payload)


    # check status

    assert response.status_code == 200, f"Beklenmeyen durum : {response.status_code} - {response.text}"


    data = response.json()

    assert "task_id" in data, "Yanıt içinde task_id yok!"
    assert data.get("status") == "processing" , f"Beklenen 'processing', gelen: {data.get('status')}"

    print(f"[✓] Video submitted. Task ID: {data['task_id']}")
    return data["task_id"]  # Bir sonraki adımda kullanılacak


def test_get_result(task_id: str, timeout: int = 60, interval: int = 5):
    """
    task_id ile belirli aralıklarla sonucu sorgular.
    Belirtilen timeout süresince "processing" durumunda kalırsa başarısız sayılır.
    """
    print(f"[•] Sonuç bekleniyor (task_id: {task_id})...")
    start = time.time()

    while time.time() - start < timeout:
        response = requests.get(f"{BASE_URL}/downsub/result/{task_id}")
        assert response.status_code == 200, "GET isteği başarısız oldu"
        data = response.json()

        if data.get("status") == "processing":
            print("[…] Hala işleniyor, bekleniyor...")
            time.sleep(interval)
        elif "content" in data:
            print("[✓] İçerik alındı:")
            print(data["content"][:300], "...")  # İlk 300 karakteri yaz
            return
        else:
            raise Exception(f"Beklenmeyen yanıt yapısı: {data}")

    raise TimeoutError("İşlem belirtilen sürede tamamlanmadı.")



if __name__ == "__main__":
    test_health_check()    
    test_url = "https://www.youtube.com/watch?v=D0Zh0bT8OuM"
    test_url_2 = "https://www.youtube.com/watch?v=LnX3B9oaKzw"
    task_id = test_submit_video(test_url_2)
    test_get_result(task_id)

