from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import shutil
import os
from extract import extract_lab_tests

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data = extract_lab_tests(temp_file)
        os.remove(temp_file)

        return JSONResponse(content={"is_success": True, "data": data})
    except Exception as e:
        return JSONResponse(content={"is_success": False, "data": [], "error": str(e)})
