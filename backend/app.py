from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
from PIL import Image
import io
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# ✅ CORS (VERY IMPORTANT for React connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 If Tesseract not working, uncomment this and set path
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Request model
class ImageData(BaseModel):
    image: str


@app.get("/")
def home():
    return {"message": "Backend is running 🚀"}


@app.post("/analyze")
async def analyze(data: ImageData):
    try:
        print("📥 Request received")

        # 1. Decode base64 image
        img_data = data.image.split(",")[1]
        image = Image.open(io.BytesIO(base64.b64decode(img_data)))

        print("🖼️ Image decoded")

        # 2. OCR (extract text)
        extracted_text = pytesseract.image_to_string(image)

        print("📝 Extracted Text:", extracted_text[:100])

        # 3. Analyze code
        result = analyze_code(extracted_text)

        return {"result": result}

    except Exception as e:
        print("❌ ERROR:", str(e))
        return {"result": f"Error: {str(e)}"}


# 🔍 Simple AI logic
def analyze_code(code):
    code = code.strip()

    if not code:
        return "No text detected. Try capturing a clearer screen."

    # Common mistakes
    if "srcobject" in code.lower():
        return "Error: 'srcobject' should be 'srcObject' (case-sensitive)."

    if "usestate" in code.lower() and "import" not in code.lower():
        return "Error: You used useState but forgot to import React."

    if "fetch(" in code and "await" not in code:
        return "Suggestion: You might need 'await' with fetch()."

    # Default response
    return f"Extracted Text:\n\n{code[:500]}"

try:
    text = pytesseract.image_to_string(image)
except:
    text = "OCR not supported in deployed environment"