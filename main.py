from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from utils import save_temp_file, process_file_to_markdown, delete_file

app = FastAPI()

@app.post("/parse")
async def parse_file(file: UploadFile = File(...)):
    file_path = save_temp_file(file)

    try:
        markdown_output = process_file_to_markdown(file_path)
        response = JSONResponse(content={"markdown": markdown_output})
    except Exception as e:
        delete_file(file_path)
        raise HTTPException(status_code=500, detail=f"Error parsing file: {str(e)}")

    @response.call_on_close
    def cleanup():
        delete_file(file_path)

    return response
