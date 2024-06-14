from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from fastapi.responses import JSONResponse, FileResponse
import os
import logging
from uuid import uuid4
from app.utils.file_processing import process_file

router = APIRouter()

# 配置日志
logging.basicConfig(level=logging.INFO)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    logging.info("Received file upload request")
    try:
        contents = await file.read()
        filename = file.filename
        logging.info(f"Received file: {filename}")

        # 使用唯一标识符创建临时文件名，避免文件名冲突
        unique_id = uuid4().hex
        temp_file_path = f"/tmp/{unique_id}_{filename}"
        with open(temp_file_path, 'wb') as f:
            f.write(contents)
        logging.info(f"Saved file to disk: {temp_file_path}")

        try:
            processed_file_path = process_file(temp_file_path, filename)
            logging.info(f"Processed file saved to: {processed_file_path}")

            return JSONResponse(content={"message": "文件上传和处理成功", "processed_file_url": f"/download/{os.path.basename(processed_file_path)}"}, status_code=200)

        except Exception as e:
            logging.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail="Error processing file")

    except Exception as e:
        logging.error(f"Error processing file: {e}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/download/{file_name}")
async def download_file(file_name: str):
    file_path = f"/tmp/{file_name}"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=file_name)
    else:
        raise HTTPException(status_code=404, detail="File not found")