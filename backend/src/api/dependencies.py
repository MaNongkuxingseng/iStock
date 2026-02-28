"""
API依赖注入模块
提供认证、授权等依赖
"""

from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.session import SessionLocal
from src.database.models import User
from src.utils.security import verify_token
from src.services.user_service import UserService

# HTTP Bearer认证方案
security = HTTPBearer()


def get_db():
    """获取数据库会话依赖"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """获取当前认证用户依赖"""
    token = credentials.credentials
    
    # 验证令牌
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效或过期的令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 获取用户ID
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的令牌载荷",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 查询用户
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已停用",
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前活跃用户依赖"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户账户已停用",
        )
    return current_user


def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """获取当前管理员用户依赖"""
    # 在实际实现中，这里应该检查用户角色
    # 这里暂时假设所有用户都是普通用户，需要扩展User模型添加角色字段
    
    # 模拟管理员检查
    if current_user.username != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限",
        )
    
    return current_user


def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """获取可选用户依赖（用户可能未登录）"""
    if credentials is None:
        return None
    
    token = credentials.credentials
    
    try:
        payload = verify_token(token)
        if payload is None:
            return None
        
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        
        if user and user.is_active:
            return user
        
        return None
        
    except Exception:
        return None


def require_permission(permission: str):
    """权限检查装饰器"""
    def permission_dependency(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ) -> User:
        # 在实际实现中，这里应该检查用户权限
        # 需要扩展权限系统
        
        # 暂时返回用户，实际应该检查权限
        return current_user
    
    return permission_dependency


def rate_limit(max_requests: int = 100, window_seconds: int = 60):
    """速率限制装饰器"""
    from src.utils.security import rate_limiter
    from fastapi import Request
    
    def rate_limit_dependency(request: Request):
        # 使用客户端IP作为标识
        client_id = request.client.host
        
        if not rate_limiter.is_allowed(client_id):
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="请求过于频繁，请稍后再试",
                headers={
                    "Retry-After": str(window_seconds),
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(window_seconds)
                }
            )
        
        remaining = rate_limiter.get_remaining(client_id)
        request.state.rate_limit_remaining = remaining
        
        return True
    
    return rate_limit_dependency


def validate_api_key(api_key: Optional[str] = None):
    """API密钥验证"""
    from src.utils.security import verify_api_key
    
    def api_key_dependency(
        db: Session = Depends(get_db),
        x_api_key: Optional[str] = None
    ):
        # 优先使用参数中的API密钥，然后使用请求头
        key_to_validate = api_key or x_api_key
        
        if not key_to_validate:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="需要API密钥",
                headers={"WWW-Authenticate": "ApiKey"},
            )
        
        # 在实际实现中，这里应该查询数据库验证API密钥
        # 暂时返回True，实际应该验证
        
        # 模拟验证
        if key_to_validate != "valid-api-key":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的API密钥",
            )
        
        return True
    
    return api_key_dependency


class PaginationParams:
    """分页参数依赖"""
    
    def __init__(
        self,
        skip: int = 0,
        limit: int = 100,
        max_limit: int = 1000
    ):
        self.skip = max(skip, 0)
        self.limit = min(max(limit, 1), max_limit)


class FilterParams:
    """过滤参数依赖"""
    
    def __init__(
        self,
        search: Optional[str] = None,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        filters: Optional[str] = None
    ):
        self.search = search
        self.sort_by = sort_by
        self.sort_order = sort_order if sort_order in ["asc", "desc"] else "desc"
        self.filters = self._parse_filters(filters) if filters else {}
    
    def _parse_filters(self, filters_str: str) -> dict:
        """解析过滤字符串"""
        filters = {}
        try:
            # 简单解析 key=value,key2=value2 格式
            for pair in filters_str.split(','):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    filters[key.strip()] = value.strip()
        except Exception:
            pass
        return filters


def get_pagination_params(
    skip: int = 0,
    limit: int = 100
) -> PaginationParams:
    """获取分页参数依赖"""
    return PaginationParams(skip=skip, limit=limit)


def get_filter_params(
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
    filters: Optional[str] = None
) -> FilterParams:
    """获取过滤参数依赖"""
    return FilterParams(
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        filters=filters
    )