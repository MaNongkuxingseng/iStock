import asyncio
import pytest
from backend.services.data_source_manager import DataSourceManager

@pytest.mark.asyncio
async def test_data_source_manager_initialization():
    """测试数据源管理器初始化"""
    manager = DataSourceManager()
    
    # 检查初始化状态
    assert len(manager.data_sources) == 4
    assert 'broker' in manager.data_sources
    assert 'sina' in manager.data_sources
    assert 'tencent' in manager.data_sources
    assert 'eastmoney' in manager.data_sources

@pytest.mark.asyncio
async def test_update_data_sources():
    """测试更新数据源"""
    manager = DataSourceManager()
    
    # 更新数据源
    result = await manager.update_data_sources()
    
    # 检查结果
    assert isinstance(result, dict)
    assert len(result) == 4

@pytest.mark.asyncio
async def test_get_primary_source():
    """测试获取主数据源"""
    manager = DataSourceManager()
    
    # 更新数据源
    await manager.update_data_sources()
    
    # 获取主数据源
    primary_source = manager.get_primary_source()
    
    # 检查结果
    assert primary_source in ['broker', 'sina', 'tencent', 'eastmoney']

@pytest.mark.asyncio
async def test_get_health_report():
    """测试获取健康报告"""
    manager = DataSourceManager()
    
    # 更新数据源
    await manager.update_data_sources()
    
    # 获取健康报告
    report = manager.get_health_report()
    
    # 检查报告结构
    assert 'total_sources' in report
    assert 'healthy_sources' in report
    assert 'health_rate' in report
    assert 'primary_source' in report
    assert 'sources' in report
    assert 'timestamp' in report

# 运行测试的示例
if __name__ == "__main__":
    asyncio.run(test_data_source_manager_initialization())
    asyncio.run(test_update_data_sources())
    asyncio.run(test_get_primary_source())
    asyncio.run(test_get_health_report())
    print("✅ 所有测试通过！")