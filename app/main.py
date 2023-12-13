from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from app.micro_qr_extractor import process_micro_qr_file

app = FastAPI()
MAX_FILE_SIZE = 10 * 1024 * 1024
MAX_FILES_COUNT = 5

def check_file_limitations(files_count):
    if files_count > MAX_FILES_COUNT:
        raise HTTPException(status_code=400, detail=f"Maximum number of files ({MAX_FILES_COUNT}) exceeded.")

@app.post("/micro-qrs/decode")
async def upload_multiple_files(files: List[UploadFile] = None):
    """
    Handles the POST request for decoding micro QR codes from multiple files.

    Parameters:
    - files (List[UploadFile]): List of uploaded files.

    Returns:
    - JSONResponse: JSON response containing the results of processing micro QR codes.
    - [
        {
            "filename": "mda1-second.png",
            "status": "ok",
            "results": [
                {
                    "decoded": "1000000000553531",
                    "bounds": "Polygon2D( (318.906359181835,902.4339247801383) (386.0880409267389,903.668952557007) (385.64719511149076,971.2244383204787) (317.6544971334475,971.332342732513) )"
                }
            ]
        },
    ]
    """
    try:
        if not files or not files[0]:
            raise HTTPException(status_code=400, detail="No files provided")
        check_file_limitations(len(files))
        results = [await process_micro_qr_file(file) for file in files]
        return JSONResponse(content=results)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")