"""
投资组合API
提供用户投资组合管理接口
"""

from fastapi import APIRouter

router = APIRouter(prefix="/portfolio", tags=["portfolio"])


@router.get("/")
async def get_portfolio():
    """获取投资组合（占位）"""
    return {
        "message": "投资组合API开发中",
        "portfolio": [
            {"symbol": "000001", "name": "平安银行", "quantity": 1000, "current_value": 15420},
            {"symbol": "000002", "name": "万科A", "quantity": 500, "current_value": 6425}
        ]
    }


@router.get("/{portfolio_id}")
async def get_portfolio_detail(portfolio_id: int):
    """获取投资组合详情（占位）"""
    return {"message": f"获取投资组合 {portfolio_id} 详情"}


@router.post("/")
async def create_portfolio():
    """创建投资组合（占位）"""
    return {"message": "创建投资组合"}


@router.put("/{portfolio_id}")
async def update_portfolio(portfolio_id: int):
    """更新投资组合（占位）"""
    return {"message": f"更新投资组合 {portfolio_id}"}


@router.delete("/{portfolio_id}")
async def delete_portfolio(portfolio_id: int):
    """删除投资组合（占位）"""
    return {"message": f"删除投资组合 {portfolio_id}"}


@router.get("/performance")
async def get_portfolio_performance():
    """获取投资组合表现（占位）"""
    return {
        "total_value": 21845,
        "total_profit": 1245,
        "profit_percent": 6.03,
        "daily_change": 215,
        "daily_change_percent": 1.02
    }


@router.get("/holdings")
async def get_holdings():
    """获取持仓列表（占位）"""
    return {
        "holdings": [
            {
                "symbol": "000001",
                "name": "平安银行",
                "quantity": 1000,
                "avg_cost": 14.50,
                "current_price": 15.42,
                "current_value": 15420,
                "profit": 920,
                "profit_percent": 6.34
            }
        ]
    }