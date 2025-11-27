from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from datetime import datetime
from ..core.database import get_database
from ..middleware.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=Dict[str, Any])
async def get_about():
    """获取关于我们页面数据（公开接口）"""
    db = get_database()
    
    about = await db.about.find_one({})
    
    if not about:
        # 返回默认数据
        return {
            "team_members": [],
            "timeline": [],
            "values": [],
            "stats": [],
            "mission": {"title": "", "content": ""},
            "contact": {}
        }
    
    # 移除 MongoDB 的 _id 字段
    about.pop("_id", None)
    return about


@router.put("/", response_model=Dict[str, Any])
async def update_about(
    about_data: Dict[str, Any],
    current_user: dict = Depends(get_current_user)
):
    """更新关于我们页面数据（需要管理员权限）"""
    db = get_database()
    
    about_data["updated_at"] = datetime.now()
    
    # 查找现有数据
    existing = await db.about.find_one({})
    
    if existing:
        await db.about.update_one(
            {"_id": existing["_id"]},
            {"$set": about_data}
        )
    else:
        await db.about.insert_one(about_data)
    
    # 返回更新后的数据
    updated = await db.about.find_one({})
    updated.pop("_id", None)
    
    return updated


@router.get("/team", response_model=list)
async def get_team_members():
    """获取团队成员列表"""
    db = get_database()
    about = await db.about.find_one({})
    
    if about and "team_members" in about:
        return about["team_members"]
    return []


@router.put("/team", response_model=list)
async def update_team_members(
    team_members: list,
    current_user: dict = Depends(get_current_user)
):
    """更新团队成员列表"""
    db = get_database()
    
    await db.about.update_one(
        {},
        {"$set": {"team_members": team_members, "updated_at": datetime.now()}},
        upsert=True
    )
    
    return team_members


@router.get("/timeline", response_model=list)
async def get_timeline():
    """获取发展历程"""
    db = get_database()
    about = await db.about.find_one({})
    
    if about and "timeline" in about:
        return about["timeline"]
    return []


@router.put("/timeline", response_model=list)
async def update_timeline(
    timeline: list,
    current_user: dict = Depends(get_current_user)
):
    """更新发展历程"""
    db = get_database()
    
    await db.about.update_one(
        {},
        {"$set": {"timeline": timeline, "updated_at": datetime.now()}},
        upsert=True
    )
    
    return timeline


@router.get("/values", response_model=list)
async def get_values():
    """获取核心价值观"""
    db = get_database()
    about = await db.about.find_one({})
    
    if about and "values" in about:
        return about["values"]
    return []


@router.put("/values", response_model=list)
async def update_values(
    values: list,
    current_user: dict = Depends(get_current_user)
):
    """更新核心价值观"""
    db = get_database()
    
    await db.about.update_one(
        {},
        {"$set": {"values": values, "updated_at": datetime.now()}},
        upsert=True
    )
    
    return values


@router.get("/stats", response_model=list)
async def get_stats():
    """获取统计数据"""
    db = get_database()
    about = await db.about.find_one({})
    
    if about and "stats" in about:
        return about["stats"]
    return []


@router.put("/stats", response_model=list)
async def update_stats(
    stats: list,
    current_user: dict = Depends(get_current_user)
):
    """更新统计数据"""
    db = get_database()
    
    await db.about.update_one(
        {},
        {"$set": {"stats": stats, "updated_at": datetime.now()}},
        upsert=True
    )
    
    return stats
