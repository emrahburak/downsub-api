import time
import os
import shortuuid


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




def find_txt_file_path_by_task_id(task_id: str, output_dir: str = "output") -> str | None:
    """
    Verilen task_id'yi içeren .txt uzantılı dosyayı output klasöründe arar.
    Bulursa tam dosya yolunu (full path) döner, bulamazsa None döner.
    """
    output_path = os.path.join(os.getcwd(), output_dir)

    for file in os.listdir(output_path):
        if file.endswith(".txt") and task_id in file:
            return os.path.join(output_path, file)

    return None
