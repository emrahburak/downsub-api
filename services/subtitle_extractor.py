from yt_dlp import YoutubeDL
import os
from .utils import clean_vtt_text, sanitize_filename


def process_video(task_id: str, youtube_url: str, sub_lang: str = "en") -> str:
    """
    TR:
    Verilen YouTube linkinden videoyu indirir, altyazıyı çeker,
    bir .txt dosyası olarak output dizinine kaydeder.

    Args:
        task_id (str): İşlem kimliği, çıktı dosyasının adı olarak kullanılır.
        youtube_url (str): İndirilecek videonun URL'si.

    Returns:
        str: Kaydedilen .txt dosyasının tam yolu.

    EN:
    Downloads video from the given YouTube URL, extracts subtitles,
    saves them as a .txt file in the output directory.

    Args:
        task_id (str): Task identifier, used as output filename.
        youtube_url (str): The URL of the video to download.

    Returns:
        str: Full path of the saved .txt file.
    """

    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [sub_lang],
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        video_id = info.get('id')
        safe_title = sanitize_filename(info.get("title", "video"))
        filename = f"{safe_title}-{task_id}.txt"

        vtt_file = os.path.join(output_dir, f"{video_id}.{sub_lang}.vtt")
        txt_file = os.path.join(output_dir, filename)

        if not os.path.exists(vtt_file):
            raise FileNotFoundError(f"Subtitle not found for video {video_id}")

        # 1. VTT içeriğini oku
        with open(vtt_file, 'r', encoding='utf-8') as vf:
            vtt_content = vf.read()

        # 2. Temizle
        cleaned_content = clean_vtt_text(vtt_content)

        # 3. Temizlenmiş içeriği .txt dosyasına yaz
        with open(txt_file, 'w', encoding='utf-8') as tf:
            tf.write(cleaned_content)

        return txt_file
