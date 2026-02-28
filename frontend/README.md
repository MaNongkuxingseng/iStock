# myStock-AI Frontend

前端应用基于 React + TypeScript + Vite 构建。

## 功能特性

- 🚀 基于 Vite 的快速开发体验
- 📱 响应式设计，支持移动端
- 🎨 Ant Design 组件库
- 📊 ECharts 数据可视化
- 🔄 实时数据更新（WebSocket）
- 🌐 多语言支持（i18n）
- 🧪 完整的测试覆盖

## 开发环境

### 环境要求
- Node.js 18+
- npm 9+ 或 yarn 1.22+

### 安装依赖
```bash
npm install
# 或
yarn install
```

### 启动开发服务器
```bash
npm run dev
# 或
yarn dev
```

### 构建生产版本
```bash
npm run build
# 或
yarn build
```

### 预览生产构建
```bash
npm run preview
# 或
yarn preview
```

## 项目结构

```
frontend/
├── public/              # 静态资源
├── src/
│   ├── assets/         # 图片、字体等资源
│   ├── components/     # 可复用组件
│   ├── pages/         # 页面组件
│   ├── layouts/       # 布局组件
│   ├── hooks/         # 自定义 Hooks
│   ├── utils/         # 工具函数
│   ├── services/      # API 服务
│   ├── stores/        # 状态管理
│   ├── types/         # TypeScript 类型定义
│   ├── styles/        # 样式文件
│   ├── locales/       # 国际化文件
│   ├── router/        # 路由配置
│   └── main.tsx       # 应用入口
├── tests/             # 测试文件
├── .env.example       # 环境变量示例
├── vite.config.ts     # Vite 配置
├── tsconfig.json      # TypeScript 配置
└── package.json       # 依赖配置
```

## 开发指南

### 代码规范
- 使用 TypeScript 严格模式
- 遵循 ESLint 和 Prettier 配置
- 组件使用函数式组件和 Hooks
- 使用 CSS Modules 或 styled-components

### 组件开发
```tsx
// 示例组件
import React from 'react';
import { Card, Typography } from 'antd';

interface StockCardProps {
  code: string;
  name: string;
  price: number;
  change: number;
}

const StockCard: React.FC<StockCardProps> = ({ code, name, price, change }) => {
  return (
    <Card title={`${code} ${name}`}>
      <Typography.Text strong>价格: {price}元</Typography.Text>
      <Typography.Text type={change >= 0 ? 'success' : 'danger'}>
        涨跌: {change >= 0 ? '+' : ''}{change}%
      </Typography.Text>
    </Card>
  );
};

export default StockCard;
```

### API 调用
```tsx
// 使用自定义 Hook
import { useStockData } from '@/hooks/useStockData';

const StockPage = () => {
  const { data, loading, error } = useStockData('603949');
  
  if (loading) return <Spin />;
  if (error) return <Alert message={error.message} type="error" />;
  
  return <StockChart data={data} />;
};
```

### 状态管理
```tsx
// 使用 Zustand
import { create } from 'zustand';

interface StockStore {
  stocks: Stock[];
  selectedStock: Stock | null;
  setStocks: (stocks: Stock[]) => void;
  selectStock: (stock: Stock) => void;
}

const useStockStore = create<StockStore>((set) => ({
  stocks: [],
  selectedStock: null,
  setStocks: (stocks) => set({ stocks }),
  selectStock: (stock) => set({ selectedStock: stock }),
}));
```

## 测试

### 单元测试
```bash
npm run test:unit
```

### 集成测试
```bash
npm run test:integration
```

### E2E 测试
```bash
npm run test:e2e
```

## 部署

### 构建优化
- 代码分割和懒加载
- 图片压缩和优化
- CSS 提取和压缩
- Tree Shaking

### Docker 部署
```bash
# 构建镜像
docker build -t mystock-ai-frontend .

# 运行容器
docker run -p 3000:80 mystock-ai-frontend
```

## 性能优化

### 代码分割
```tsx
// 动态导入
const StockChart = React.lazy(() => import('./StockChart'));

const App = () => (
  <Suspense fallback={<Loading />}>
    <StockChart />
  </Suspense>
);
```

### 图片优化
- 使用 WebP 格式
- 实现懒加载
- 响应式图片

### 缓存策略
- Service Worker 缓存
- 浏览器缓存头
- CDN 缓存

## 国际化

### 添加新语言
1. 在 `src/locales/` 创建语言文件
2. 更新 `src/locales/index.ts`
3. 在组件中使用 `useTranslation`

### 使用示例
```tsx
import { useTranslation } from 'react-i18next';

const Welcome = () => {
  const { t } = useTranslation();
  return <h1>{t('welcome.title')}</h1>;
};
```

## 监控和错误处理

### 错误边界
```tsx
class ErrorBoundary extends React.Component {
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    // 发送错误到监控服务
    logErrorToService(error, errorInfo);
  }
  
  render() {
    return this.props.children;
  }
}
```

### 性能监控
```tsx
// 使用 Web Vitals
import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

getCLS(console.log);
getFID(console.log);
getFCP(console.log);
getLCP(console.log);
getTTFB(console.log);
```

## 贡献指南

1. Fork 仓库
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License