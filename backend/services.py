from pathlib import Path
import random
import string

from settings import IMAGE_FOLDER, STATIC_ROOT


BASE = Path(__file__).resolve().parent

IMAGE_FOLDER_PATH = Path(BASE, STATIC_ROOT, IMAGE_FOLDER)

def save_file(file: bytes, filename: str):
    salt = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    name_parts = filename.split('.')
    basename = '.'.join(name_parts[:-1])
    ext = name_parts[-1]
    filename = f'{basename}_{salt}.{ext}'
    with open(Path(IMAGE_FOLDER_PATH, filename), 'wb') as f:
        f.write(file)

    return filename
