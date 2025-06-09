import os
import uuid
import shutil
from markitdown import MarkItDown

TEMP_DIR = "./temp"

def save_temp_file(file) -> str:
    os.makedirs(TEMP_DIR, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(TEMP_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return file_path

def process_file_to_markdown(file_path: str) -> str:
    md = MarkItDown(enable_plugins=True)
    return md.convert(file_path)

def delete_file(path: str):
    try:
        os.remove(path)
    except FileNotFoundError:
        pass
