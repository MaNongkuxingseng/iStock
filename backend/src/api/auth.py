"""
用户认证API
提供登录、注册、令牌管理等接口
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login():
    """用户登录（占位）"""
    return {"message": "登录API开发中", "token": "dummy_token"}


@router.post("/register")
async def register():
    """用户注册（占位）"""
    return {"message": "注册API开发中"}


@router.post("/logout")
async def logout():
    """用户登出（占位）"""
    return {"message": "登出成功"}


@router.post("/refresh")
async def refresh_token():
    """刷新访问令牌（占位）"""
    return {"message": "令牌刷新API开发中", "new_token": "dummy_refresh_token"}


@router.get("/me")
async def get_current_user():
    """获取当前用户信息（占位）"""
    return {
        "user": {
            "id": 1,
            "username": "demo_user",
            "email": "demo@istock.com",
            "full_name": "演示用户"
        }
    }