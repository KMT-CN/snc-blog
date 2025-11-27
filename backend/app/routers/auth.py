from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from typing import List
from pydantic import BaseModel
from ..schemas import (
    AdminCreate, AdminLogin, TokenResponse, AdminResponse, MessageResponse
)
from ..core.database import get_database
from ..core.security import get_password_hash, verify_password, create_access_token
from ..middleware.auth import get_current_user

router = APIRouter()


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str


@router.get("/check-setup", response_model=dict)
async def check_setup():
    """检查是否已有管理员账号"""
    db = get_database()
    admin_count = await db.admins.count_documents({})
    return {"needsSetup": admin_count == 0}


@router.post("/setup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def setup_admin(admin: AdminCreate):
    """首次设置管理员账号"""
    db = get_database()
    
    # 检查是否已有管理员
    admin_count = await db.admins.count_documents({})
    if admin_count > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="管理员账号已存在"
        )
    
    # 创建管理员
    admin_dict = {
        "username": admin.username,
        "email": admin.email,
        "hashed_password": get_password_hash(admin.password),
        "is_first_login": False,
        "created_at": None
    }
    
    result = await db.admins.insert_one(admin_dict)
    
    # 生成令牌
    token = create_access_token({"id": str(result.inserted_id), "username": admin.username})
    
    return TokenResponse(
        message="管理员账号创建成功",
        token=token,
        admin=AdminResponse(id=str(result.inserted_id), username=admin.username, email=admin.email)
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: AdminLogin):
    """登录"""
    db = get_database()
    
    # 查找管理员
    admin = await db.admins.find_one({"username": credentials.username})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if not verify_password(credentials.password, admin["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 生成令牌
    token = create_access_token({"id": str(admin["_id"]), "username": admin["username"]})
    
    return TokenResponse(
        message="登录成功",
        token=token,
        admin=AdminResponse(id=str(admin["_id"]), username=admin["username"], email=admin["email"])
    )


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user)
):
    """修改密码（需要登录）"""
    db = get_database()
    
    # 获取当前用户
    admin = await db.admins.find_one({"_id": ObjectId(current_user["id"])})
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 验证当前密码
    if not verify_password(request.current_password, admin["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 验证新密码长度
    if len(request.new_password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="新密码长度至少6位"
        )
    
    # 更新密码
    await db.admins.update_one(
        {"_id": ObjectId(current_user["id"])},
        {"$set": {"hashed_password": get_password_hash(request.new_password)}}
    )
    
    return MessageResponse(message="密码修改成功")
