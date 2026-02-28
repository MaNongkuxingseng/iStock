"""
用户服务
提供用户管理相关的业务逻辑
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
import bcrypt

from src.database.models import User
from src.database.session import SessionLocal


class UserService:
    """用户服务类"""
    
    def __init__(self, db: Session = None):
        """初始化服务"""
        self.db = db or SessionLocal()
    
    def hash_password(self, password: str) -> str:
        """哈希密码"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    def get_user_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """根据ID获取用户"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return self.db.query(User).filter(User.email == email).first()
    
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """创建新用户"""
        # 检查用户名是否已存在
        existing_username = self.get_user_by_username(user_data.get("username", ""))
        if existing_username:
            raise ValueError(f"Username {user_data['username']} already exists")
        
        # 检查邮箱是否已存在
        existing_email = self.get_user_by_email(user_data.get("email", ""))
        if existing_email:
            raise ValueError(f"Email {user_data['email']} already registered")
        
        # 哈希密码
        if "password" in user_data:
            user_data["hashed_password"] = self.hash_password(user_data.pop("password"))
        
        # 设置默认值
        user_data.setdefault("id", uuid.uuid4())
        user_data.setdefault("is_active", True)
        user_data.setdefault("risk_tolerance", "medium")
        user_data.setdefault("investment_experience", "beginner")
        
        user = User(**user_data)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def update_user(self, user_id: uuid.UUID, update_data: Dict[str, Any]) -> Optional[User]:
        """更新用户信息"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # 不允许更新某些字段
        restricted_fields = ["id", "created_at", "hashed_password"]
        for field in restricted_fields:
            update_data.pop(field, None)
        
        # 如果需要更新密码
        if "password" in update_data:
            update_data["hashed_password"] = self.hash_password(update_data.pop("password"))
        
        # 更新字段
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def delete_user(self, user_id: uuid.UUID) -> bool:
        """删除用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        self.db.delete(user)
        self.db.commit()
        
        return True
    
    def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """用户认证"""
        user = self.get_user_by_username(username)
        if not user:
            # 尝试使用邮箱登录
            user = self.get_user_by_email(username)
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    def list_users(
        self, 
        skip: int = 0, 
        limit: int = 100,
        active_only: bool = True
    ) -> List[User]:
        """获取用户列表"""
        query = self.db.query(User)
        
        if active_only:
            query = query.filter(User.is_active == True)
        
        return query.offset(skip).limit(limit).all()
    
    def activate_user(self, user_id: uuid.UUID) -> bool:
        """激活用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = True
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def deactivate_user(self, user_id: uuid.UUID) -> bool:
        """停用用户"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.is_active = False
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def change_password(self, user_id: uuid.UUID, old_password: str, new_password: str) -> bool:
        """修改密码"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        if not self.verify_password(old_password, user.hashed_password):
            return False
        
        user.hashed_password = self.hash_password(new_password)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def reset_password(self, user_id: uuid.UUID, new_password: str) -> bool:
        """重置密码（管理员功能）"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        
        user.hashed_password = self.hash_password(new_password)
        user.updated_at = datetime.utcnow()
        self.db.commit()
        
        return True
    
    def get_user_statistics(self) -> Dict[str, Any]:
        """获取用户统计信息"""
        total_users = self.db.query(User).count()
        active_users = self.db.query(User).filter(User.is_active == True).count()
        
        # 按风险偏好统计
        risk_stats = {}
        for risk in ["low", "medium", "high"]:
            count = self.db.query(User).filter(User.risk_tolerance == risk).count()
            risk_stats[risk] = count
        
        # 按投资经验统计
        experience_stats = {}
        for exp in ["beginner", "intermediate", "expert"]:
            count = self.db.query(User).filter(User.investment_experience == exp).count()
            experience_stats[exp] = count
        
        # 最近注册的用户
        recent_users = self.db.query(User).order_by(
            User.created_at.desc()
        ).limit(5).all()
        
        recent_users_data = [
            {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in recent_users
        ]
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "inactive_users": total_users - active_users,
            "risk_tolerance": risk_stats,
            "investment_experience": experience_stats,
            "recent_users": recent_users_data,
            "calculated_at": datetime.utcnow().isoformat()
        }
    
    def search_users(self, query: str, limit: int = 20) -> List[User]:
        """搜索用户"""
        return self.db.query(User).filter(
            (User.username.contains(query)) | 
            (User.email.contains(query)) |
            (User.full_name.contains(query))
        ).limit(limit).all()
    
    def check_username_availability(self, username: str) -> bool:
        """检查用户名是否可用"""
        existing = self.get_user_by_username(username)
        return existing is None
    
    def check_email_availability(self, email: str) -> bool:
        """检查邮箱是否可用"""
        existing = self.get_user_by_email(email)
        return existing is None
    
    def update_user_preferences(
        self, 
        user_id: uuid.UUID, 
        preferences: Dict[str, Any]
    ) -> Optional[User]:
        """更新用户偏好设置"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        
        # 允许更新的偏好字段
        allowed_fields = ["risk_tolerance", "investment_experience", "notification_settings"]
        
        for field in allowed_fields:
            if field in preferences:
                setattr(user, field, preferences[field])
        
        user.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(user)
        
        return user
    
    def get_user_activity_log(self, user_id: uuid.UUID, limit: int = 50) -> List[Dict[str, Any]]:
        """获取用户活动日志（模拟）"""
        # 在实际实现中，这里应该查询活动日志表
        # 这里返回模拟数据
        
        activities = [
            {
                "id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "activity_type": "login",
                "description": "用户登录",
                "timestamp": datetime.utcnow().isoformat(),
                "ip_address": "192.168.1.100",
                "user_agent": "Mozilla/5.0"
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "activity_type": "portfolio_view",
                "description": "查看投资组合",
                "timestamp": (datetime.utcnow().replace(hour=10, minute=30)).isoformat(),
                "details": {"portfolio_id": "123"}
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "activity_type": "stock_search",
                "description": "搜索股票",
                "timestamp": (datetime.utcnow().replace(hour=9, minute=15)).isoformat(),
                "details": {"query": "AAPL"}
            }
        ]
        
        return activities[:limit]
    
    def close(self):
        """关闭数据库会话"""
        if self.db:
            self.db.close()