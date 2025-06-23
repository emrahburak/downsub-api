from yt_dlp import YoutubeDL
import os
from .utils import clean_vtt_text, sanitize_filename,find_matching_subtitle_lang
from .config import OUTPUT_DIR
import logging


logging.basicConfig(level=logging.DEBUG)



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
    logging.info(f"Processing video: {youtube_url} with task_id: {task_id}")


    output_dir = OUTPUT_DIR
    os.makedirs(output_dir, exist_ok=True)

    probe_opts = {
        'skip_download': True,
        'quiet': True
    }

    with YoutubeDL(probe_opts) as probe_ydl:
        info_dict = probe_ydl.extract_info(youtube_url, download=False)
        logging.debug(f"Available subtitles: {list(info_dict.get('subtitles', {}).keys())}")
        matched_lang = find_matching_subtitle_lang(info_dict, sub_lang)
        if not matched_lang:
            raise FileNotFoundError(f"No matching subtitle language found for '{sub_lang}' in video {info_dict.get('id')}")
        logging.info(f"Using subtitle language: {matched_lang}")



        ydl_opts = {
            'skip_download': True,
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [matched_lang],
            'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
            'quiet': True,
        }

    logging.debug(f"yt-dlp options: {ydl_opts}")


    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=True)
        logging.info(f"Extracted video info: id={info.get('id')}, title={info.get('title')}")

        video_id = info.get('id')
        safe_title = sanitize_filename(info.get("title", "video"))
        filename = f"{safe_title}-{task_id}.txt"

        vtt_file = os.path.join(output_dir, f"{video_id}.{matched_lang}.vtt")
        txt_file = os.path.join(output_dir, filename)
        logging.debug(f"Expected subtitle file path: {vtt_file}")


        if not os.path.exists(vtt_file):
            logging.error(f"Subtitle file not found at expected path: {vtt_file}")
            raise FileNotFoundError(f"Subtitle not found for video {video_id}")

        # 1. VTT içeriğini oku
        with open(vtt_file, 'r', encoding='utf-8') as vf:
            vtt_content = vf.read()
            logging.debug(f"Read {len(vtt_content)} characters from subtitle file")


        # 2. Temizle
        cleaned_content = clean_vtt_text(vtt_content)
        logging.debug(f"Cleaned subtitle content length: {len(cleaned_content)}")


        # 3. Temizlenmiş içeriği .txt dosyasına yaz
        with open(txt_file, 'w', encoding='utf-8') as tf:
            tf.write(cleaned_content)
            logging.info(f"Written cleaned subtitles to: {txt_file}")


        return txt_file
