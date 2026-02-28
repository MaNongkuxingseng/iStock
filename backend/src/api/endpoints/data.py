"""
数据源和同步API端点
"""

from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from datetime import datetime
import uuid

from src.database.session import SessionLocal
from src.database.models import DataSource, DataSyncLog

# 创建路由器
router = APIRouter()

# 数据模型
class DataSourceBase(BaseModel):
    name: str
    source_type: str  # sina/tencent/eastmoney
    base_url: Optional[str] = None
    api_key: Optional[str] = None
    rate_limit: int = 10
    is_active: bool = True

class DataSourceCreate(DataSourceBase):
    pass

class DataSourceResponse(DataSourceBase):
    id: int
    last_sync: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True

class DataSyncLogBase(BaseModel):
    data_source_id: int
    sync_type: str  # realtime/historical/financial
    status: str  # success/failed/partial
    records_fetched: Optional[int] = None
    records_processed: Optional[int] = None
    error_message: Optional[str] = None

class DataSyncLogResponse(DataSyncLogBase):
    id: int
    start_time: str
    end_time: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True

class SyncRequest(BaseModel):
    data_source_id: Optional[int] = None
    sync_type: str = "realtime"
    symbols: Optional[List[str]] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class SyncResponse(BaseModel):
    task_id: str
    status: str
    message: str
    data_source_id: Optional[int] = None
    sync_type: str

# 依赖注入：数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 获取数据源列表
@router.get("/sources", response_model=List[DataSourceResponse])
async def list_data_sources(
    active_only: bool = True,
    db = Depends(get_db)
):
    """获取数据源列表"""
    query = db.query(DataSource)
    
    if active_only:
        query = query.filter(DataSource.is_active == True)
    
    sources = query.order_by(DataSource.name).all()
    return sources

# 获取单个数据源
@router.get("/sources/{source_id}", response_model=DataSourceResponse)
async def get_data_source(source_id: int, db = Depends(get_db)):
    """获取单个数据源信息"""
    source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    return source

# 创建数据源
@router.post("/sources", response_model=DataSourceResponse)
async def create_data_source(source: DataSourceCreate, db = Depends(get_db)):
    """创建新数据源"""
    # 检查是否已存在
    existing = db.query(DataSource).filter(DataSource.name == source.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Data source with this name already exists")
    
    db_source = DataSource(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    
    return db_source

# 更新数据源
@router.put("/sources/{source_id}", response_model=DataSourceResponse)
async def update_data_source(
    source_id: int, 
    source_update: DataSourceCreate, 
    db = Depends(get_db)
):
    """更新数据源信息"""
    source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    # 更新字段
    update_data = source_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(source, field, value)
    
    db.commit()
    db.refresh(source)
    
    return source

# 删除数据源
@router.delete("/sources/{source_id}")
async def delete_data_source(source_id: int, db = Depends(get_db)):
    """删除数据源"""
    source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    db.delete(source)
    db.commit()
    
    return {"message": "Data source deleted successfully"}

# 触发数据同步
@router.post("/sync", response_model=SyncResponse)
async def trigger_sync(
    sync_request: SyncRequest,
    background_tasks: BackgroundTasks,
    db = Depends(get_db)
):
    """触发数据同步"""
    task_id = str(uuid.uuid4())
    
    if sync_request.data_source_id:
        # 验证数据源存在
        source = db.query(DataSource).filter(
            DataSource.id == sync_request.data_source_id
        ).first()
        
        if not source:
            raise HTTPException(status_code=404, detail="Data source not found")
        
        if not source.is_active:
            raise HTTPException(status_code=400, detail="Data source is not active")
    
    # 创建同步日志记录
    sync_log = DataSyncLog(
        data_source_id=sync_request.data_source_id,
        sync_type=sync_request.sync_type,
        start_time=datetime.utcnow(),
        status="started",
        records_fetched=0,
        records_processed=0
    )
    
    db.add(sync_log)
    db.commit()
    db.refresh(sync_log)
    
    # 在后台执行同步任务
    background_tasks.add_task(
        execute_sync_task,
        task_id=task_id,
        sync_log_id=sync_log.id,
        sync_request=sync_request.dict()
    )
    
    # 更新数据源的最后同步时间
    if sync_request.data_source_id:
        source = db.query(DataSource).filter(
            DataSource.id == sync_request.data_source_id
        ).first()
        
        if source:
            source.last_sync = datetime.utcnow()
            db.commit()
    
    return SyncResponse(
        task_id=task_id,
        status="started",
        message=f"Data sync started in background. Task ID: {task_id}",
        data_source_id=sync_request.data_source_id,
        sync_type=sync_request.sync_type
    )

# 获取同步日志
@router.get("/sync/logs", response_model=List[DataSyncLogResponse])
async def get_sync_logs(
    data_source_id: Optional[int] = None,
    sync_type: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 100,
    db = Depends(get_db)
):
    """获取数据同步日志"""
    query = db.query(DataSyncLog)
    
    if data_source_id:
        query = query.filter(DataSyncLog.data_source_id == data_source_id)
    
    if sync_type:
        query = query.filter(DataSyncLog.sync_type == sync_type)
    
    if status:
        query = query.filter(DataSyncLog.status == status)
    
    logs = query.order_by(DataSyncLog.start_time.desc()).limit(limit).all()
    return logs

# 获取同步状态
@router.get("/sync/status/{task_id}")
async def get_sync_status(task_id: str, db = Depends(get_db)):
    """获取同步任务状态"""
    # 在实际实现中，这里应该查询任务队列的状态
    # 这里返回模拟状态
    
    return {
        "task_id": task_id,
        "status": "completed",  # 模拟状态
        "progress": 100,
        "message": "Sync task completed successfully",
        "timestamp": datetime.utcnow().isoformat()
    }

# 获取数据源统计
@router.get("/sources/{source_id}/stats")
async def get_data_source_stats(source_id: int, db = Depends(get_db)):
    """获取数据源统计信息"""
    source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    # 获取同步日志统计
    logs = db.query(DataSyncLog).filter(
        DataSyncLog.data_source_id == source_id
    ).all()
    
    total_syncs = len(logs)
    successful_syncs = len([log for log in logs if log.status == "success"])
    failed_syncs = len([log for log in logs if log.status == "failed"])
    
    # 计算平均记录数
    if logs:
        avg_fetched = sum(log.records_fetched or 0 for log in logs) / len(logs)
        avg_processed = sum(log.records_processed or 0 for log in logs) / len(logs)
    else:
        avg_fetched = 0
        avg_processed = 0
    
    # 最近同步
    recent_sync = None
    if logs:
        recent = max(logs, key=lambda x: x.start_time)
        recent_sync = {
            "time": recent.start_time.isoformat(),
            "type": recent.sync_type,
            "status": recent.status,
            "records": recent.records_fetched or 0
        }
    
    return {
        "data_source": {
            "id": source.id,
            "name": source.name,
            "type": source.source_type,
            "is_active": source.is_active,
            "last_sync": source.last_sync.isoformat() if source.last_sync else None
        },
        "statistics": {
            "total_syncs": total_syncs,
            "successful_syncs": successful_syncs,
            "failed_syncs": failed_syncs,
            "success_rate": (successful_syncs / total_syncs * 100) if total_syncs > 0 else 0,
            "avg_records_fetched": avg_fetched,
            "avg_records_processed": avg_processed
        },
        "recent_sync": recent_sync
    }

# 获取系统数据统计
@router.get("/stats/overview")
async def get_data_stats_overview(db = Depends(get_db)):
    """获取系统数据统计概览"""
    # 数据源统计
    total_sources = db.query(DataSource).count()
    active_sources = db.query(DataSource).filter(DataSource.is_active == True).count()
    
    # 同步日志统计
    total_syncs = db.query(DataSyncLog).count()
    today = datetime.utcnow().date()
    today_syncs = db.query(DataSyncLog).filter(
        db.func.date(DataSyncLog.start_time) == today
    ).count()
    
    # 按类型统计
    sync_types = {}
    for sync_type in ["realtime", "historical", "financial"]:
        count = db.query(DataSyncLog).filter(DataSyncLog.sync_type == sync_type).count()
        sync_types[sync_type] = count
    
    # 按状态统计
    status_stats = {}
    for status in ["success", "failed", "partial", "started"]:
        count = db.query(DataSyncLog).filter(DataSyncLog.status == status).count()
        status_stats[status] = count
    
    # 总记录数统计
    total_fetched = db.query(db.func.sum(DataSyncLog.records_fetched)).scalar() or 0
    total_processed = db.query(db.func.sum(DataSyncLog.records_processed)).scalar() or 0
    
    return {
        "data_sources": {
            "total": total_sources,
            "active": active_sources,
            "inactive": total_sources - active_sources
        },
        "sync_operations": {
            "total": total_syncs,
            "today": today_syncs,
            "by_type": sync_types,
            "by_status": status_stats
        },
        "records": {
            "total_fetched": total_fetched,
            "total_processed": total_processed,
            "processing_rate": (total_processed / total_fetched * 100) if total_fetched > 0 else 0
        },
        "last_updated": datetime.utcnow().isoformat()
    }

# 测试数据源连接
@router.post("/sources/{source_id}/test")
async def test_data_source_connection(source_id: int, db = Depends(get_db)):
    """测试数据源连接"""
    source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    # 模拟连接测试
    # 在实际实现中，这里应该尝试连接数据源API
    
    test_result = {
        "data_source_id": source_id,
        "name": source.name,
        "type": source.source_type,
        "base_url": source.base_url,
        "test_time": datetime.utcnow().isoformat(),
        "status": "success",  # 模拟成功
        "response_time_ms": 150,  # 模拟响应时间
        "message": f"Successfully connected to {source.name}"
    }
    
    return test_result

# 后台同步任务（模拟）
async def execute_sync_task(task_id: str, sync_log_id: int, sync_request: dict):
    """执行