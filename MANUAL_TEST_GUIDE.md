# 🔧 iStock项目手动测试指南

## 🎯 测试目标
验证iStock项目核心功能是否正常工作，识别和修复问题。

## 📋 测试前准备

### 1. 环境检查
```bash
# 打开命令提示符或PowerShell
# 检查当前目录
dir docker-compose.yml

# 应该看到:
# docker-compose.yml
```

### 2. 基础工具检查
```bash
# 检查Docker
docker --version
# 应该输出: Docker version 20.10.x

# 检查Docker Compose
docker-compose --version
# 或者
docker compose version

# 检查Python
python --version
# 应该输出: Python 3.10+
```

## 🚀 分步测试流程

### 步骤1: 验证Docker环境
```bash
# 1.1 检查Docker守护进程
docker info

# 1.2 检查现有容器
docker ps -a

# 1.3 检查现有镜像
docker images
```

### 步骤2: 启动基础服务
```bash
# 2.1 只启动数据库和Redis（最小化测试）
docker-compose up -d postgres redis

# 2.2 检查服务状态
docker-compose ps

# 应该看到:
# postgres   Up (healthy)
# redis      Up (healthy)
```

### 步骤3: 测试数据库连接
```bash
# 3.1 进入PostgreSQL容器
docker-compose exec postgres psql -U mystock_user -d mystock_ai

# 在psql中执行:
\dt  # 查看表
SELECT version();  # 查看版本
\q   # 退出

# 3.2 测试Redis
docker-compose exec redis redis-cli ping
# 应该返回: PONG
```

### 步骤4: 启动后端服务
```bash
# 4.1 启动后端
docker-compose up -d backend

# 4.2 等待后端启动（约30秒）
timeout /t 30

# 4.3 测试健康检查
curl http://localhost:8000/health
# 或者用浏览器访问: http://localhost:8000/health

# 4.4 测试API文档
# 浏览器访问: http://localhost:8000/docs
```

### 步骤5: 测试数据库迁移
```bash
# 5.1 运行数据库迁移
docker-compose exec backend alembic upgrade head

# 5.2 检查迁移状态
docker-compose exec backend alembic current
```

### 步骤6: 测试数据脚本
```bash
# 6.1 测试数据库连接脚本
docker-compose exec backend python backend/scripts/test_database.py --test connection

# 6.2 测试模型导入
docker-compose exec backend python backend/scripts/test_database.py --test models

# 6.3 播种测试数据（可选）
docker-compose exec backend python backend/scripts/seed_data.py --data stocks
```

### 步骤7: 启动前端服务
```bash
# 7.1 启动前端
docker-compose up -d frontend

# 7.2 等待前端启动（约60秒）
timeout /t 60

# 7.3 测试前端
# 浏览器访问: http://localhost:3000
```

### 步骤8: 启动完整服务
```bash
# 8.1 停止现有服务
docker-compose down

# 8.2 启动所有服务
docker-compose up -d

# 8.3 检查所有服务状态
docker-compose ps

# 应该看到所有服务: postgres, redis, backend, frontend, etc.
```

## 🔍 问题诊断

### 常见问题1: Docker命令找不到
```
'docker' 不是内部或外部命令
```
**解决方案:**
1. 确保Docker Desktop已安装并启动
2. 将Docker添加到系统PATH
3. 重启命令行窗口

### 常见问题2: 端口被占用
```
Error: port is already allocated
```
**解决方案:**
1. 修改`docker-compose.yml`中的端口映射
2. 或停止占用端口的程序

### 常见问题3: 数据库连接失败
```
could not connect to server: Connection refused
```
**解决方案:**
1. 检查PostgreSQL容器是否运行: `docker-compose ps`
2. 检查`.env`文件配置
3. 等待数据库完全启动（约30秒）

### 常见问题4: 前端无法访问
```
无法访问此网站
```
**解决方案:**
1. 检查前端容器是否运行: `docker-compose ps frontend`
2. 查看前端日志: `docker-compose logs frontend`
3. 等待更长时间（前端构建可能需要几分钟）

## 📊 验证清单

### 基础验证
- [ ] Docker Desktop已安装并运行
- [ ] Docker Compose可用
- [ ] 项目目录正确
- [ ] `.env`文件存在

### 服务验证
- [ ] PostgreSQL容器运行正常
- [ ] Redis容器运行正常
- [ ] 后端API可访问 (`http://localhost:8000/health`)
- [ ] API文档可访问 (`http://localhost:8000/docs`)
- [ ] 前端应用可访问 (`http://localhost:3000`)

### 功能验证
- [ ] 数据库迁移成功
- [ ] 数据模型可导入
- [ ] 测试数据可播种
- [ ] 健康检查通过

### 集成验证
- [ ] 所有服务同时运行
- [ ] 服务间通信正常
- [ ] 日志无严重错误
- [ ] 资源使用合理

## 🛠️ 快速修复命令

### 重置环境
```bash
# 停止所有服务
docker-compose down

# 删除数据卷（谨慎使用）
docker-compose down -v

# 重新构建镜像
docker-compose build --no-cache

# 重新启动
docker-compose up -d
```

### 查看日志
```bash
# 查看所有日志
docker-compose logs

# 查看特定服务日志
docker-compose logs backend
docker-compose logs frontend
docker-compose logs postgres

# 实时查看日志
docker-compose logs -f backend
```

### 进入容器调试
```bash
# 进入后端容器
docker-compose exec backend bash

# 进入数据库容器
docker-compose exec postgres bash

# 在容器内执行命令
docker-compose exec backend python --version
docker-compose exec postgres psql --version
```

## 📈 性能测试

### 响应时间测试
```bash
# 测试API响应时间
curl -o /dev/null -s -w "Time: %{time_total}s\n" http://localhost:8000/health

# 测试数据库查询
docker-compose exec backend python -c "
import time
from src.database.session import SessionLocal
start = time.time()
db = SessionLocal()
result = db.execute('SELECT 1')
db.close()
print(f'Database connection: {time.time()-start:.3f}s')
"
```

### 资源使用监控
```bash
# 查看容器资源使用
docker stats --no-stream

# 查看系统资源
docker system df
```

## 🎯 成功标准

### 必须通过
- [ ] 所有Docker容器正常运行
- [ ] 数据库连接和迁移成功
- [ ] 后端API响应正常
- [ ] 前端应用可访问

### 应该通过
- [ ] 测试数据可播种
- [ ] API文档完整
- [ ] 服务健康检查通过
- [ ] 日志无错误

### 最好通过
- [ ] 性能指标达标
- [ ] 资源使用合理
- [ ] 用户体验良好
- [ ] 文档完整准确

## 📞 支持信息

### 获取帮助
1. **查看日志**: `docker-compose logs`
2. **检查状态**: `docker-compose ps`
3. **验证配置**: 检查`.env`文件
4. **测试连接**: 使用`curl`或浏览器

### 报告问题
请提供以下信息:
1. 错误消息全文
2. 执行命令
3. 当前目录
4. Docker版本
5. 操作系统版本

### 紧急恢复
```bash
# 完全重置
docker-compose down -v
docker system prune -a -f
docker-compose up -d
```

---

**注意**: 如果遇到无法解决的问题，请运行`test_simple.bat`获取基础诊断信息。