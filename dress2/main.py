from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
import clip
import torch
from PIL import Image
import io

app = FastAPI()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ 設定 CORS，允許來自 http://127.0.0.1:5500 的請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🚀 或者改成 ["http://127.0.0.1:5500"]
    allow_credentials=True,
    allow_methods=["*"],  # 允許所有請求方法 (GET, POST, etc.)
    allow_headers=["*"],  # 允許所有 Headers
)

@app.get("/")
async def root():
    return {"message": "FastAPI 服務運行中 🚀"}


# ✅ 定義回應格式
class PredictionResponse(BaseModel):
    prediction: str
    temperature_range: str

# ✅ 設定裝置 (GPU or CPU)
device = "cuda" if torch.cuda.is_available() else "cpu"

# ✅ 載入 CLIP 模型
model, preprocess = clip.load("ViT-B/32", device=device)

# ✅ 定義衣服類別標籤
clothing_labels = [
    "heavy coat", "down jacket", "wool coat", "leather jacket", "fur coat", "parka",
    "bomber jacket", "denim jacket", "windbreaker", "blazer", "hoodie", "sweater",
    "cardigan", "long sleeve shirt", "t-shirt", "short sleeve shirt", "tank top",
    "crop top", "jeans", "trousers", "sweatpants", "shorts", "skirt", "dress",
    "jumpsuit", "scarf", "gloves", "beanie", "hat"
]

# ✅ 定義對應的溫度區間
clothing_temp_map = {
    "heavy coat": "0-10°C", "down jacket": "0-10°C", "wool coat": "0-10°C",
    "leather jacket": "0-10°C", "fur coat": "0-10°C", "parka": "0-10°C",
    "bomber jacket": "11-20°C", "denim jacket": "11-20°C", "windbreaker": "11-20°C",
    "blazer": "11-20°C", "hoodie": "11-20°C", "sweater": "11-20°C",
    "cardigan": "11-20°C", "long sleeve shirt": "11-20°C",
    "t-shirt": "21-30°C", "short sleeve shirt": "21-30°C", "tank top": "21-30°C",
    "crop top": "21-30°C", "jeans": "11-20°C", "trousers": "11-20°C",
    "sweatpants": "11-20°C", "shorts": "21-30°C", "skirt": "21-30°C",
    "dress": "21-30°C", "jumpsuit": "21-30°C", "scarf": "0-10°C",
    "gloves": "0-10°C", "beanie": "0-10°C", "hat": "21-30°C"
}

@app.post("/predict", response_model=PredictionResponse)
async def predict_clothing(file: UploadFile = File(...), description: str = Form(None)):
    try:
        # 讀取圖片
        image_bytes = await file.read()
        print(f"📸 收到圖片: {file.filename}, 大小: {len(image_bytes)} bytes")  # Debug 訊息

        # 確保圖片成功讀取
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # 預處理圖片
        image = preprocess(image).unsqueeze(0).to(device)

        # 轉換標籤為 CLIP 向量
        text_inputs = clip.tokenize(clothing_labels).to(device)

        # 預測圖片類別
        with torch.no_grad():
            image_features = model.encode_image(image)
            text_features = model.encode_text(text_inputs)
            similarities = (image_features @ text_features.T).softmax(dim=-1)
            best_match_idx = similarities.argmax().item()

        # 獲取最接近的標籤
        predicted_label = clothing_labels[best_match_idx]
        predicted_temp = clothing_temp_map.get(predicted_label, "未知")

        print(f"✅ 預測結果: {predicted_label}, 適合溫度: {predicted_temp}")  # Debug 訊息

        return PredictionResponse(
            prediction=predicted_label,
            temperature_range=predicted_temp
        )

    except Exception as e:
        print(f"❌ 錯誤: {str(e)}")  # Debug 訊息
        return {"error": str(e)}

@app.get("/")
async def root():
    return {"message": "FastAPI 服務運行中 🚀"}
