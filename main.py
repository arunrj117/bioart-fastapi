from fastapi import FastAPI, UploadFile, File, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uvicorn
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

uploads = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/analysis/upload-skin")
async def upload_skin(
    images: List[UploadFile] = File(...),
    x_user_token: str = Header(...)
):
    upload_id = str(uuid.uuid4())
    uploads[upload_id] = {
        "token": x_user_token,
        "image_count": len(images),
        "filenames": [img.filename for img in images]
    }
    return {"uploadId": upload_id, "received": len(images)}

@app.post("/analysis/analyze-skin")
async def analyze_skin(
    body: dict,
    x_user_token: str = Header(...)
):
    upload_id = body.get("uploadId")
    if not upload_id or upload_id not in uploads:
        raise HTTPException(status_code=404, detail="Upload not found")

    return {
        "uploadId": upload_id,
        "skinType": "Combination",
        "concerns": ["Mild dryness", "Uneven tone"],
        "recommendations": [
            "Use a gentle hydrating cleanser",
            "Apply SPF 30+ daily",
            "Consider a Vitamin C serum"
        ],
        "score": 78
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
