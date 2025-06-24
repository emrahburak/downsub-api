import time
import os
import shortuuid
import re


def get_subtitle_languages(info: dict) -> list[str]:
    """
    TR:
    Video info'dan mevcut altyazı dillerinin tam listesini döner.
    Hem 'subtitles' hem de 'automatic_captions' içindeki dilleri alır.

    Args:
        info (dict): yt-dlp extract_info sonucu

    Returns:
        list[str]: Mevcut altyazı dil kodlarının listesi


    EN:
    Returns the full list of available subtitle languages from video info.
    Retrieves languages from both 'subtitles' and 'automatic_captions'.

    Args:
        info (dict): The result dictionary from yt-dlp's extract_info

    Returns:
        list[str]: List of available subtitle language codes
    """
    subs = info.get('subtitles', {})
    auto_subs = info.get('automatic_captions', {})
    all_langs = set(subs.keys()) | set(auto_subs.keys())
    return sorted(all_langs)


def find_matching_subtitle_lang(info_dict: dict,
                                desired_lang: str) -> str | None:
    """
    TR:
    Aranan dile en yakın uygun altyazı dilini döner.
    Örneğin, 'en' verildiğinde mevcutsa 'en-GB' gibi benzer dil kodunu bulur.

    Args:
        info_dict (dict): yt-dlp'den alınan video bilgi sözlüğü
        desired_lang (str): Kullanıcının istediği altyazı dili

    Returns:
        str | None: Eşleşen altyazı dili kodu veya bulunamazsa None


    EN:
    Returns the closest matching subtitle language for the requested language.
    For example, if 'en' is requested and 'en-GB' exists, it will return 'en-GB'.

    Args:
        info_dict (dict): Video info dictionary from yt-dlp
        desired_lang (str): Desired subtitle language code

    Returns:
        str | None: Matching subtitle language code or None if no match found
    """
    available_langs = get_subtitle_languages(info_dict)

    # 1. Tam eşleşme
    if desired_lang in available_langs:
        return desired_lang

    # 2. Prefix eşleşmesi (örnek: 'en' => 'en-GB')
    for lang in available_langs:
        if lang.startswith(desired_lang + "-"):
            return lang

    return None


def sanitize_filename(name: str) -> str:
    """
    TR:
    Verilen dosya adındaki geçersiz karakterleri temizler.
    Yalnızca harfler (a-z, A-Z), rakamlar (0-9), tire (-), alt çizgi (_) ve boşluk karakterlerine izin verir.
    Diğer tüm karakterleri kaldırır ve boşlukları alt çizgi (_) ile değiştirir.
    Sonuç, dosya sistemi tarafından güvenle kullanılabilecek bir dosya adıdır.

    Args:
        name (str): Temizlenecek orijinal dosya adı.

    Returns:
        str: Geçersiz karakterlerden arındırılmış ve boşlukları alt çizgi ile değiştirilmiş dosya adı.

    EN:
    Cleans the given filename by removing invalid characters.
    Allows only letters (a-z, A-Z), digits (0-9), hyphens (-), underscores (_), and spaces.
    Removes all other characters and replaces spaces with underscores (_).
    The result is a filename safe to use in file systems.

    Args:
        name (str): The original filename to sanitize.

    Returns:
        str: Sanitized filename with invalid characters removed and spaces replaced by underscores.
    """

    return re.sub(r'[^a-zA-Z0-9\-_\s]', '', name).strip().replace(' ', '_')


def clean_vtt_text(vtt_content: str, group_size: int = 3) -> str:
    """
    TR:
    Verilen VTT (WebVTT) formatındaki altyazı içeriğini temizler ve yalnızca düz metin olarak anlamlı satırları döner.
    İşlemler şunları içerir:
    - Zaman kodlarını atlar.
    - Köşeli parantez içindeki açıklama satırlarını atlar (örneğin, [Müzik]).
    - WEBVTT ve Kind: captions gibi başlık satırlarını atlar.
    - Language: ile başlayan satırları atlar.
    - Satırlardaki HTML benzeri etiketleri temizler.
    - Ardışık aynı satırların tekrarını engeller.
    Sonuç olarak, altyazıdaki sadece okunabilir ve tekrarsız metin satırları elde edilir.

    Args:
        vtt_content (str): VTT formatındaki altyazı içeriği.

    Returns:
        str: Temizlenmiş ve tekrarsızlaştırılmış düz metin altyazı.

    EN:
    Cleans the provided VTT (WebVTT) subtitle content and returns only meaningful plain text lines.
    The process includes:
    - Skipping timestamp lines.
    - Ignoring lines with comments enclosed in square brackets (e.g., [Music]).
    - Skipping header lines like WEBVTT and Kind: captions.
    - Skipping lines starting with Language:.
    - Removing HTML-like tags from lines.
    - Filtering out consecutive duplicate lines.
    The result is a clean, deduplicated plain text subtitle.

    Args:
        vtt_content (str): Subtitle content in VTT format.

    Returns:
        str: Cleaned and deduplicated plain text subtitle.
    """

    lines = vtt_content.splitlines()
    cleaned_lines = []
    previous_line = None

    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}',
                    line):
            continue
        if line.startswith('[') and line.endswith(']'):
            continue
        if line in {"WEBVTT", "Kind: captions"}:
            continue
        if line.startswith("Language:"):
            continue

        clean_line = re.sub(r'<.*?>', '', line)

        # ✅ sadece arka arkaya aynı olan satırları atlar
        if clean_line != previous_line:
            cleaned_lines.append(clean_line)
            previous_line = clean_line

    # Satırları gruplar halinde birleştir
    paragraphs = []
    buffer = []
    for i, line in enumerate(cleaned_lines):
        buffer.append(line)
        if len(buffer) >= 3:  # Her 3 satırda bir paragraf yap
            paragraphs.append(" ".join(buffer))
            buffer = []
    if buffer:
        paragraphs.append(" ".join(buffer))  # Kalanları ekle

    return "\n\n".join(paragraphs).strip()


def generate_unique_id():
    """
    TR: Benzersiz bir ID üretir.
    EN: Generates a unique ID.
    """
    return shortuuid.uuid()


def str_to_bool(value: str) -> bool:
    """
    TR:
        Verilen string değeri boolean'a dönüştürür.
        Aşağıdaki değerler True olarak değerlendirilir:
        "true", "1", "yes", "on" (büyük/küçük harf duyarsız).
        Diğer tüm değerler False olarak kabul edilir.

    EN:
        Converts a given string value to a boolean.
        The following values are interpreted as True:
        "true", "1", "yes", "on" (case-insensitive).
        All other values are considered False.

    Args:
        value (str): Dönüştürülecek string değer.

    Returns:
        bool: Boolean karşılığı (True veya False).
    """
    return str(value).strip().lower() in ("true", "1", "yes", "on")


def clean_old_files(folder_path: str, max_age_seconds: int = 86400):
    """
    TR:
        Belirtilen klasördeki dosyaları tarar ve 
        son değişiklik tarihi belirlenen süreden (varsayılan: 1 gün) eski olan dosyaları siler.

        Bu işlem genellikle geçici çıktıların temizlenmesi veya disk alanının yönetimi için kullanılır.
        Silinemeyen dosyalar hakkında hata mesajı verilir.

    EN:
        Scans the specified folder and removes files older than the given age 
        (default: 1 day) based on their last modified time.

        Useful for cleaning up temporary outputs or managing disk usage.
        If a file cannot be removed, an error message is printed.

    Args:
        folder_path (str): İşlem yapılacak klasörün yolu / Path of the target folder.
        max_age_seconds (int): Maksimum izin verilen dosya yaşı (saniye cinsinden) / Maximum allowed file age in seconds.

    Returns:
        None
    """

    now = time.time()
    for fname in os.listdir(folder_path):
        fpath = os.path.join(folder_path, fname)
        if os.path.isfile(fpath):
            file_age = now - os.path.getmtime(fpath)
            if file_age > max_age_seconds:
                print(f"Removing {fname} (age: {file_age} sec)")
                try:
                    os.remove(fpath)
                except Exception as e:
                    print(f"Error removing file {fpath}: {e}")


def find_txt_file_path_by_task_id(task_id: str,
                                  output_dir: str = "output") -> str | None:
    """
    Verilen task_id'yi içeren .txt uzantılı dosyayı output klasöründe arar.
    Bulursa tam dosya yolunu (full path) döner, bulamazsa None döner.
    """
    output_path = os.path.join(os.getcwd(), output_dir)

    for file in os.listdir(output_path):
        if file.endswith(".txt") and task_id in file:
            return os.path.join(output_path, file)

    return None
