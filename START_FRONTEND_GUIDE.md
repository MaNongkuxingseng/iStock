# 🎨 启动iStock前端服务指南

## 📋 前端服务状态
根据测试结果，前端React开发服务器**未启动**。需要手动启动。

## 🚀 启动步骤

### 前提条件
1. **Node.js** 已安装 (版本 14+)
2. **npm** 或 **yarn** 已安装

### 步骤1: 检查Node.js环境
```bash
node --version
npm --version
```

### 步骤2: 安装前端依赖
```bash
cd frontend
npm install
# 或使用 yarn
yarn install
```

### 步骤3: 启动开发服务器
```bash
npm start
# 或使用 yarn
yarn start
```

### 步骤4: 验证启动
打开浏览器访问: http://localhost:3000

## 🔧 故障排除

### 问题1: Node.js未安装
**解决方案**:
1. 下载并安装Node.js: https://nodejs.org/
2. 选择LTS版本
3. 安装后重启命令行

### 问题2: npm install失败
**解决方案**:
```bash
# 清理缓存
npm cache clean --force

# 删除node_modules
rm -rf node_modules
rm -f package-lock.json

# 重新安装
npm install
```

### 问题3: 端口3000被占用
**解决方案**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :3000

# 终止进程 (替换PID为实际进程ID)
taskkill /PID <PID> /F

# 或修改启动端口
npm start -- --port 3001
```

### 问题4: 缺少依赖包
**解决方案**:
```bash
# 安装缺失的包
npm install react react-dom react-scripts

# 或重新安装所有依赖
npm install --force
```

## 📱 前端功能验证

启动后验证以下功能:

### 1. 基础页面
- [ ] 首页: http://localhost:3000
- [ ] 股票页面: http://localhost:3000/stocks
- [ ] 仪表盘: http://localhost:3000/dashboard

### 2. API连接
- [ ] 检查控制台无错误
- [ ] 网络请求正常
- [ ] 数据加载成功

### 3. 用户界面
- [ ] 导航菜单正常
- [ ] 响应式布局
- [ ] 交互功能正常

## 🐳 Docker方式启动 (备选)

如果本地环境有问题，可以使用Docker:

### 使用Docker Compose
```bash
# 启动所有服务 (包括前端)
docker-compose up -d

# 或只启动前端
docker-compose up frontend
```

### 直接使用Docker
```bash
# 构建前端镜像
docker build -f Dockerfile.frontend -t istock-frontend .

# 运行容器
docker run -p 3000:3000 istock-frontend
```

## 📊 前端架构

### 技术栈
- **框架**: React 18
- **语言**: JavaScript/TypeScript
- **状态管理**: Context API
- **UI组件**: 自定义组件 + CSS
- **路由**: React Router
- **HTTP客户端**: Fetch API

### 项目结构
```
frontend/
├── public/           # 静态资源
├── src/
│   ├── components/   # 可复用组件
│   ├── pages/        # 页面组件
│   ├── services/     # API服务
│   ├── contexts/     # React上下文
│   ├── App.js        # 主应用组件
│   └── index.js      # 入口文件
└── package.json      # 依赖配置
```

### 核心组件
1. **Header** - 顶部导航栏
2. **StockTable** - 股票数据表格
3. **Dashboard** - 仪表盘页面
4. **Stocks** - 股票列表页面

## 🔗 与后端集成

### API端点
```javascript
// API服务配置 (src/services/api.js)
const API_BASE = 'http://localhost:8000/api/v1';

// 主要端点
- GET /stocks          # 获取股票列表
- GET /stocks/{id}     # 获取单个股票
- POST /auth/login     # 用户登录
- GET /portfolio       # 获取投资组合
```

### 环境配置
创建 `.env` 文件:
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## 🧪 测试前端

### 开发测试
```bash
# 运行测试
npm test

# 运行特定测试
npm test -- --testNamePattern="StockTable"

# 覆盖率报告
npm test -- --coverage
```

### 构建生产版本
```bash
# 构建
npm run build

# 预览构建结果
npm install -g serve
serve -s build
```

## 📈 下一步开发

### 待完成功能
1. **股票图表组件** - 添加价格走势图
2. **筛选器组件** - 股票筛选功能
3. **投资组合组件** - 持仓管理界面
4. **用户设置页面** - 个性化配置

### 优化计划
1. **性能优化** - 代码分割、懒加载
2. **用户体验** - 加载状态、错误处理
3. **移动端适配** - 响应式设计优化
4. **可访问性** - ARIA标签、键盘导航

## 📞 技术支持

### 常见问题
1. **Q: 启动后显示空白页面**
   A: 检查控制台错误，可能是路由配置问题

2. **Q: API请求失败**
   A: 检查后端服务是否运行，CORS配置是否正确

3. **Q: 热重载不工作**
   A: 检查文件监视器配置，可能需要调整系统设置

### 获取帮助
提供以下信息:
1. 错误消息截图
2. 控制台输出
3. 系统环境信息
4. 复现步骤

---

**前端服务启动后，iStock将提供完整的Web界面，可以进行功能测试和用户体验验证！**