"""
用户管理API
提供用户注册、登录、信息管理等接口
"""

from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
async def get_users():
    """获取用户列表（占位）"""
    return {"message": "用户API开发中"}


@router.get("/{user_id}")
async def get_user(user_id: int):
    """获取用户信息（占位）"""
    return {"message": f"获取用户 {user_id} 信息"}


@router.post("/")
async def create_user():
    """创建用户（占位）"""
    return {"message": "创建用户"}


@router.put("/{user_id}")
async def update_user(user_id: int):
    """更新用户信息（占位）"""
    return {"message": f"更新用户 {user_id}"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    """删除用户（占位）"""
    return {"message": f"删除用户 {user_id}"}