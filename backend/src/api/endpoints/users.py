"""
用户管理API端点
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import uuid

from src.database.session import SessionLocal
from src.database.models import User

# 创建路由器
router = APIRouter()

# 数据模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    risk_tolerance: Optional[str] = "medium"
    investment_experience: Optional[str] = "beginner"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    risk_tolerance: Optional[str] = None
    investment_experience: Optional[str] = None
    is_active: Optional[bool] = None

# 依赖注入：数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 用户注册
@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # 检查邮箱是否已存在
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 创建用户（实际应该哈希密码）
    db_user = User(
        id=uuid.uuid4(),
        username=user.username,
        email=user.email,
        hashed_password=f"hashed_{user.password}",  # 实际应该使用密码哈希
        full_name=user.full_name,
        risk_tolerance=user.risk_tolerance,
        investment_experience=user.investment_experience,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

# 获取用户信息
@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: uuid.UUID, db = Depends(get_db)):
    """获取用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# 更新用户信息
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID, 
    user_update: UserUpdate, 
    db = Depends(get_db)
):
    """更新用户信息"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 更新允许修改的字段
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    
    return user

# 用户登录（简化版）
@router.post("/login")
async def login(username: str, password: str, db = Depends(get_db)):
    """用户登录"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # 简化密码验证（实际应该验证哈希）
    if user.hashed_password != f"hashed_{password}":
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not user.is_active:
        raise HTTPException(status_code=403, detail="User account is inactive")
    
    # 返回用户信息和模拟token
    return {
        "access_token": f"mock_token_{user.id}",
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name
        }
    }

# 获取用户列表（管理员功能）
@router.get("/")
async def list_users(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db = Depends(get_db)
):
    """获取用户列表（需要管理员权限）"""
    query = db.query(User)
    
    if active_only:
        query = query.filter(User.is_active == True)
    
    users = query.offset(skip).limit(limit).all()
    
    return [
        {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
        for user in users
    ]

# 停用用户
@router.post("/{user_id}/deactivate")
async def deactivate_user(user_id: uuid.UUID, db = Depends(get_db)):
    """停用用户账户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = False
    db.commit()
    
    return {"message": "User deactivated successfully"}

# 激活用户
@router.post("/{user_id}/activate")
async def activate_user(user_id: uuid.UUID, db = Depends(get_db)):
    """激活用户账户"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    
    return {"message": "User activated successfully"}

# 用户统计
@router.get("/stats/summary")
async def user_stats_summary(db = Depends(get_db)):
    """用户统计摘要"""
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    
    # 风险偏好统计
    risk_stats = {}
    for risk in ["low", "medium", "high"]:
        count = db.query(User).filter(User.risk_tolerance == risk).count()
        risk_stats[risk] = count
    
    # 投资经验统计
    experience_stats = {}
    for exp in ["beginner", "intermediate", "expert"]:
        count = db.query(User).filter(User.investment_experience == exp).count()
        experience_stats[exp] = count
    
    return {
        "total_users": total_users,
        "active_users": active_users,
        "inactive_users": total_users - active_users,
        "risk_tolerance": risk_stats,
        "investment_experience": experience_stats
    }

# 检查用户名可用性
@router.get("/check/username/{username}")
async def check_username_availability(username: str, db = Depends(get_db)):
    """检查用户名是否可用"""
    existing = db.query(User).filter(User.username == username).first()
    
    return {
        "username": username,
        "available": existing is None
    }

# 检查邮箱可用性
@router.get("/check/email/{email}")
async def check_email_availability(email: str, db = Depends(get_db)):
    """检查邮箱是否可用"""
    existing = db.query(User).filter(User.email == email).first()
    
    return {
        "email": email,
        "available": existing is None
    }