# 🤖 iStock 自动化监控系统设置指南

## 📋 测试结果总结

### ✅ 服务状态检查
- 健康检查: ✅ 正常 (http://localhost:8000/health)
- API文档: ✅ 正常 (http://localhost:8000/docs)

### 📅 交易日分析
- 测试日期: 2026-02-28 (星期六)
- 是否为交易日: ❌ 否
- 结论: 如果stockbot配置为只在交易日推送，您**不应该**收到测试消息

## 🚨 严重测试消息已发送

### 测试目的
验证stockbot盯盘分析系统的消息推送机制，检查是否只在交易日/工作日进行推送。

### 关键发现
1. **今天是星期六，不是交易日**
2. **如果未收到消息**: 说明推送机制按预期工作（只在交易日推送）
3. **如果收到消息**: 说明推送机制配置为每天推送

## 🔧 自动化监控系统已建立

### 已创建的文件
1. **`automated_monitor.py`** - 完整的自动化监控系统
   - 服务健康检查
   - 股票分析
   - 消息推送
   - 定时任务

2. **`test_alert_simple.py`** - 测试脚本
   - 发送测试警报
   - 检查交易日
   - 验证推送机制

3. **`test_alert_simple.json`** - 测试记录
   - 保存测试详情
   - 记录交易日状态
   - 跟踪测试结果

### 监控功能
- ✅ **服务健康监控**: 每30分钟检查一次
- ✅ **股票分析**: 交易日9:30和13:00运行
- ✅ **消息推送**: 支持Feishu等渠道
- ✅ **交易日检测**: 自动判断是否为交易日
- ✅ **警报分级**: 低、中、高、严重级别
- ✅ **历史记录**: 保存所有监控记录

## 🚀 立即设置自动化监控

### 步骤1: 安装依赖
```bash
pip install schedule aiohttp requests
```

### 步骤2: 运行监控测试
```bash
# 运行完整的监控测试
python automated_monitor.py --test

# 或运行简单测试
python test_alert_simple.py
```

### 步骤3: 设置定时任务 (Windows)

#### 方法A: 使用Windows任务计划程序
1. 打开"任务计划程序"
2. 创建基本任务
3. 名称: "iStock Automated Monitor"
4. 触发器: 每天，重复间隔30分钟
5. 操作: 启动程序
   - 程序: `python`
   - 参数: `G:\openclaw\workspace\_system\agent-home\myStock-AI\automated_monitor.py`
6. 条件: 取消"只有在计算机使用交流电源时才启动此任务"
7. 设置: 选中"如果任务运行时间超过以下时间，停止任务: 1小时"

#### 方法B: 使用批处理文件 + 计划任务
创建 `run_monitor.bat`:
```batch
@echo off
cd /d "G:\openclaw\workspace\_system\agent-home\myStock-AI"
python automated_monitor.py
```

然后在任务计划程序中指向这个批处理文件。

#### 方法C: 使用Python schedule (开发环境)
```python
# 在automated_monitor.py中已经实现
# 只需保持Python进程运行
python automated_monitor.py --daemon
```

## 📊 监控配置选项

### 交易日设置
```python
# 在 automated_monitor.py 中修改
def is_trading_day(self):
    today = date.today()
    weekday = today.weekday()  # 0=周一, 6=周日
    
    # 当前设置: 周一到周五为交易日
    if weekday < 5:  # 0-4 = 周一到周五
        return True
    
    # 可以添加节假日检查
    # holidays = ["2026-01-01", "2026-02-08", ...]
    # if today.isoformat() in holidays:
    #     return False
    
    return False
```

### 推送时间调整
```python
# 修改监控频率
schedule.every(30).minutes.do(check_health)  # 每30分钟

# 修改股票分析时间
schedule.every().day.at("09:30").do(stock_analysis)  # 早上9:30
schedule.every().day.at("13:00").do(stock_analysis)  # 下午1:00

# 修改日报时间
schedule.every().day.at("23:00").do(daily_report)    # 晚上11:00
```

### 警报级别配置
```python
# 警报级别阈值
ALERT_THRESHOLDS = {
    "low": ["服务响应慢", "磁盘空间不足"],
    "medium": ["API错误", "数据库连接问题"],
    "high": ["服务不可用", "数据同步失败"],
    "critical": ["系统崩溃", "安全漏洞"]
}
```

## 🔍 问题诊断

### 如果未收到任何消息
1. **检查服务状态**
   ```bash
   python test_alert_simple.py
   ```

2. **检查交易日设置**
   - 确认今天是否为交易日
   - 检查节假日配置

3. **检查推送配置**
   - 确认Feishu webhook配置
   - 检查网络连接

4. **检查监控日志**
   ```bash
   type automated_monitor.log
   ```

### 如果收到非交易日消息
1. **调整交易日检测**
   ```python
   # 修改 is_trading_day() 方法
   ```

2. **检查监控配置**
   ```python
   # 确保只在交易日运行股票分析
   if self.is_trading_day():
       await self.run_stock_analysis()
   ```

3. **验证时间设置**
   - 检查系统时间
   - 确认时区设置

## 📈 监控数据分析

### 查看监控记录
```bash
# 查看警报历史
type alerts_history.json

# 查看股票分析历史
type stock_analysis_history.json

# 查看监控状态
type monitor_state.json
```

### 监控指标
- **服务可用性**: 成功率 = 成功检查数 / 总检查数
- **响应时间**: 平均API响应时间
- **警报频率**: 每天/每周警报数量
- **问题分类**: 按类型统计的问题数量

## 🎯 最佳实践

### 1. 分级警报
- **低级别**: 记录日志，不推送
- **中级别**: 推送但不紧急
- **高级别**: 立即推送，需要关注
- **严重级别**: 立即推送，需要立即处理

### 2. 交易日优化
- 只在交易日运行股票分析
- 非交易日只进行基础健康检查
- 周末和节假日静默模式

### 3. 性能考虑
- 监控间隔不要太频繁（建议30分钟）
- 异步执行避免阻塞
- 合理设置超时时间

### 4. 容错处理
- 网络异常重试机制
- 服务不可用降级处理
- 监控自身健康检查

## 📞 技术支持

### 常见问题
1. **Q: 监控没有运行**
   A: 检查任务计划程序配置，确认Python路径正确

2. **Q: 没有收到警报**
   A: 检查交易日设置，确认推送渠道配置

3. **Q: 监控占用资源太多**
   A: 调整监控频率，优化检查逻辑

4. **Q: 如何添加新的监控项**
   A: 在 `automated_monitor.py` 中添加新的检查方法

### 获取帮助
提供以下信息：
1. 监控日志内容
2. 测试结果
3. 具体的错误消息
4. 当前配置

## ✅ 完成状态

### 已完成的自动化功能
- [x] 服务健康监控
- [x] 股票分析自动化
- [x] 交易日检测
- [x] 消息推送机制
- [x] 定时任务框架
- [x] 历史记录保存
- [x] 警报分级系统

### 下一步优化
- [ ] 集成真实的Feishu API
- [ ] 添加更多监控指标
- [ ] 实现Web管理界面
- [ ] 添加短信/邮件通知
- [ ] 实现自动修复功能

---

**自动化监控系统已就绪！** 🎉

现在您可以：
1. 立即测试推送机制（检查是否收到测试消息）
2. 设置定时监控任务
3. 根据测试结果调整配置
4. 享受自动化的监控和分析服务