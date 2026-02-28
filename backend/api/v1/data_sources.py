from fastapi import APIRouter, Depends
from backend.services.data_source_manager import DataSourceManager

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])

data_source_manager = DataSourceManager()

@router.get("/status")
async def get_data_source_status():
    """
    获取数据源状态和健康报告
    
    Returns:
        dict: 数据源健康报告
    """
    # 更新数据源状态
    await data_source_manager.update_data_sources()
    
    # 获取健康报告
    report = data_source_manager.get_health_report()
    
    return {
        "status": "success",
        "data": report,
        "message": "数据源状态获取成功"
    }

@router.get("/primary")
async def get_primary_data_source():
    """
    获取主数据源
    
    Returns:
        dict: 主数据源信息
    """
    # 更新数据源状态
    await data_source_manager.update_data_sources()
    
    primary_source = data_source_manager.get_primary_source()
    
    return {
        "status": "success",
        "data": {
            "primary_source": primary_source,
            "source_info": data_source_manager.data_sources[primary_source]
        },
        "message": "主数据源获取成功"
    }