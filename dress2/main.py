from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 解決 CORS 問題
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 模擬天氣 API 回應
@app.get("/weather")
def get_weather(location: str):
    return {"temperature": 20, "weather_condition": "晴天"}

# 模擬服裝推薦 API
@app.get("/recommend")
def recommend_outfit(location: str, occasion: str):
    return {
        "top": "T-shirt",
        "bottom": "牛仔褲",
        "shoes": "運動鞋"
    }
