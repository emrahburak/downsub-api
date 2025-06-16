from yt_dlp import YoutubeDL
import os


def process_video(task_id: str, youtube_url: str) -> str:
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
    if output_dir is None:
        os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'quiet': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        video_id = info.get('id')

    vtt_file = os.path.join(output_dir, f"{video_id}.en.vtt")
    txt_file = os.path.join(output_dir, f"{task_id}.txt")

    if not os.path.exists(vtt_file):
        raise FileNotFoundError(f"Subtitle not found for video {video_id}")

    with open(vtt_file,
              'r', encoding='utf-8') as vf, open(txt_file,
                                                 'w',
                                                 encoding='utf-8') as tf:
        for line in vf:
            # Zaman damgalarını ve boş satırları atla
            if "-->" in line or line.strip() == "":
                continue
            tf.write(line)

    return txt_file
