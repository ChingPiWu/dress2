from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# 設定 MySQL 資料庫連接（你可以選擇使用雲端資料庫，例如 Amazon RDS 或 Google Cloud SQL）
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:rabbit1928@localhost/dress"

# 建立資料庫引擎
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# 建立基礎模型
Base = declarative_base()

# 設定資料庫的表格
class WardrobeItem(Base):
    __tablename__ = "wardrobe_items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String)
    added_at = Column(DateTime, default=datetime.utcnow)

# 創建 Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 創建 FastAPI 實例
app = FastAPI()

# 創建資料庫
Base.metadata.create_all(bind=engine)

# 取得資料庫 Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API: 獲取衣櫥項目
@app.get("/wardrobe/")
def get_wardrobe_items(db: Session = Depends(get_db)):
    items = db.query(WardrobeItem).all()
    return items

# API: 新增衣櫥項目
@app.post("/wardrobe/")
def add_wardrobe_item(name: str, category: str, db: Session = Depends(get_db)):
    new_item = WardrobeItem(name=name, category=category)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item
