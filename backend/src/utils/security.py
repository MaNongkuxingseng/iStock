"""
安全工具模块
提供JWT认证、密码哈希等安全功能
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import jwt
from passlib.context import CryptContext
import secrets
import uuid

# 密码哈希上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT配置
SECRET_KEY = "your-secret-key-change-in-production"  # 生产环境应该从环境变量读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),  # JWT ID
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """创建刷新令牌"""
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "jti": str(uuid.uuid4()),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """验证令牌"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # 令牌过期
        return None
    except jwt.InvalidTokenError:
        # 无效令牌
        return None


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """解码令牌（不验证过期）"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
        return payload
    except jwt.InvalidTokenError:
        return None


def generate_api_key() -> str:
    """生成API密钥"""
    return secrets.token_urlsafe(32)


def generate_csrf_token() -> str:
    """生成CSRF令牌"""
    return secrets.token_urlsafe(16)


def validate_csrf_token(token: str, stored_token: str) -> bool:
    """验证CSRF令牌"""
    return secrets.compare_digest(token, stored_token)


def sanitize_input(input_string: str) -> str:
    """清理用户输入（基础XSS防护）"""
    if not input_string:
        return ""
    
    # 移除危险字符
    dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '`']
    for char in dangerous_chars:
        input_string = input_string.replace(char, '')
    
    return input_string.strip()


def validate_email(email: str) -> bool:
    """验证邮箱格式"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_password_strength(password: str) -> Dict[str, Any]:
    """验证密码强度"""
    result = {
        "valid": True,
        "errors": [],
        "score": 0
    }
    
    # 检查长度
    if len(password) < 8:
        result["valid"] = False
        result["errors"].append("密码至少需要8个字符")
    
    # 检查复杂度
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    
    if not has_upper:
        result["errors"].append("密码需要包含大写字母")
    if not has_lower:
        result["errors"].append("密码需要包含小写字母")
    if not has_digit:
        result["errors"].append("密码需要包含数字")
    if not has_special:
        result["errors"].append("密码需要包含特殊字符")
    
    # 计算分数
    score = 0
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    
    if has_upper and has_lower:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1
    
    result["score"] = score
    
    # 如果分数低于3，认为密码弱
    if score < 3:
        result["valid"] = False
        result["errors"].append("密码强度不足")
    
    return result


def generate_otp(length: int = 6) -> str:
    """生成OTP验证码"""
    import random
    digits = "0123456789"
    return ''.join(random.choice(digits) for _ in range(length))


def hash_api_key(api_key: str) -> str:
    """哈希API密钥"""
    return pwd_context.hash(api_key)


def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """验证API密钥"""
    return pwd_context.verify(plain_api_key, hashed_api_key)


class RateLimiter:
    """简单的速率限制器"""
    
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}
    
    def is_allowed(self, client_id: str) -> bool:
        """检查是否允许请求"""
        now = datetime.utcnow()
        
        if client_id not in self.requests:
            self.requests[client_id] = []
        
        # 清理过期的请求记录
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if (now - req_time).seconds < self.window_seconds
        ]
        
        # 检查请求数量
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        
        # 记录本次请求
        self.requests[client_id].append(now)
        return True
    
    def get_remaining(self, client_id: str) -> int:
        """获取剩余请求次数"""
        now = datetime.utcnow()
        
        if client_id not in self.requests:
            return self.max_requests
        
        # 清理过期的请求记录
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if (now - req_time).seconds < self.window_seconds
        ]
        
        return self.max_requests - len(self.requests[client_id])


# 全局速率限制器实例
rate_limiter = RateLimiter(max_requests=100, window_seconds=60)