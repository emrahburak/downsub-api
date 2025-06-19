from yt_dlp import YoutubeDL
import os
import re


def sanitize_filename(name: str) -> str:
    # Sadece harf, rakam, boşluk ve tireye izin ver, kalanları kaldır
    return re.sub(r'[^a-zA-Z0-9\-_\s]', '', name).strip().replace(' ', '_')


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

        with open(vtt_file, 'r',
                  encoding='utf-8') as vf, open(txt_file,
                                                'w',
                                                encoding='utf-8') as tf:
            skip_header_lines = {"WEBVTT", "Kind: captions"}

            for line in vf:
                line_stripped = line.strip()
                # Zaman damgalarını ve boş satırları atla
                if not line_stripped or "-->" in line_stripped:
                    continue
                # Başlık satırlarını atla
                if line_stripped in skip_header_lines:
                    continue
                if line_stripped.startswith("Language: "):
                    continue
                tf.write(line_stripped + "\n")

            return txt_file
