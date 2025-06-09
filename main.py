from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from utils import save_temp_file, process_file_to_markdown, delete_file
import os

app = FastAPI()

@app.post("/parse")
async def parse_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    file_path = save_temp_file(file)

    try:
        markdown_text = process_file_to_markdown(file_path)
        base_name = os.path.splitext(os.path.basename(file.filename))[0]
        markdown_filename = f"{base_name}.md"
        markdown_path = os.path.join(os.path.dirname(file_path), markdown_filename)

        with open(markdown_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)
    except Exception as e:
        delete_file(file_path)
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

    background_tasks.add_task(delete_file, file_path)
    background_tasks.add_task(delete_file, markdown_path)

    return FileResponse(
        markdown_path,
        media_type="text/markdown",
        filename=markdown_filename
    )
