#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学习资料下载功能API路由
"""

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, Form, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse, FileResponse
import os
import uuid

from core.database import get_db_common
from core.security import get_current_user
from core.logger import log_user_action, log_error
from models.learning_materials import MaterialCategory, LearningMaterial, UserDownload, MaterialRating, MaterialComment, UserMaterialFavorite
from models.users import User, UserSubscription

router = APIRouter(tags=["learning_materials"])


# 资料分类相关API

@router.get("/categories", summary="获取资料分类列表")
async def get_material_categories(
    type: Optional[int] = Query(None, description="分类类型：1-考研，2-考公，3-通用"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取资料分类列表"""
    try:
        query = db.query(MaterialCategory)
        
        # 管理员用户可以看到所有分类，不需要过滤
        if not current_user.is_admin:
            # 获取用户订阅信息
            user_subscription = db.query(UserSubscription).filter(
                UserSubscription.user_id == current_user.id
            ).first()
            subscribe_type = user_subscription.subscribe_type if user_subscription else None
            
            # 根据用户类型自动过滤分类
            # vip_type: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP
            # subscribe_type: 1-考研, 2-考公, 3-双赛道
            if current_user.vip_type == 1 or (subscribe_type and subscribe_type == 1):
                # 考研用户只能看到考研分类和通用分类
                query = query.filter(MaterialCategory.type.in_([1, 3]))
            elif current_user.vip_type == 2 or (subscribe_type and subscribe_type == 2):
                # 考公用户只能看到考公分类和通用分类
                query = query.filter(MaterialCategory.type.in_([2, 3]))
            # 双赛道用户（vip_type=3或subscribe_type=3）和非VIP用户可以看到所有分类
        
        if type is not None:
            query = query.filter(MaterialCategory.type == type)
        categories = query.all()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取资料分类列表成功",
                "data": [{
                    "id": c.id,
                    "name": c.name,
                    "type": c.type,
                    "description": c.description,
                    "created_at": c.created_at.isoformat()
                } for c in categories]
            }
        )
    except Exception as e:
        log_error(f"获取资料分类列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"获取资料分类列表失败: {str(e)}"
        )


@router.post("/categories", summary="创建资料分类")
async def create_material_category(
    name: str = Form(..., description="分类名称"),
    type: int = Form(..., description="分类类型：1-考研，2-考公，3-通用"),
    description: Optional[str] = Form(None, description="分类描述"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """创建资料分类"""
    try:
        # 检查分类是否已存在
        existing_category = db.query(MaterialCategory).filter(
            MaterialCategory.name == name,
            MaterialCategory.type == type
        ).first()
        if existing_category:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "分类已存在",
                    "data": None
                }
            )
        
        # 创建分类
        category = MaterialCategory(
            name=name,
            type=type,
            description=description
        )
        db.add(category)
        db.commit()
        db.refresh(category)
        
        log_user_action(current_user.id, "create_material_category", f"创建资料分类: {name}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "创建资料分类成功",
                "data": {
                    "id": category.id,
                    "name": category.name,
                    "type": category.type,
                    "description": category.description,
                    "created_at": category.created_at.isoformat()
                }
            }
        )
    except Exception as e:
        log_error(f"创建资料分类失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="创建资料分类失败"
        )


@router.put("/categories/{category_id}", summary="更新资料分类")
async def update_material_category(
    category_id: int = Path(..., description="分类ID"),
    name: Optional[str] = Form(None, description="分类名称"),
    type: Optional[int] = Form(None, description="分类类型：1-考研，2-考公，3-通用"),
    description: Optional[str] = Form(None, description="分类描述"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """更新资料分类"""
    try:
        # 检查分类是否存在
        category = db.query(MaterialCategory).filter(MaterialCategory.id == category_id).first()
        if not category:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "分类不存在",
                    "data": None
                }
            )
        
        # 更新分类
        if name is not None:
            category.name = name
        if type is not None:
            category.type = type
        if description is not None:
            category.description = description
        
        db.commit()
        db.refresh(category)
        
        log_user_action(current_user.id, "update_material_category", f"更新资料分类: {category.name}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新资料分类成功",
                "data": {
                    "id": category.id,
                    "name": category.name,
                    "type": category.type,
                    "description": category.description,
                    "created_at": category.created_at.isoformat()
                }
            }
        )
    except Exception as e:
        log_error(f"更新资料分类失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="更新资料分类失败"
        )


@router.delete("/categories/{category_id}", summary="删除资料分类")
async def delete_material_category(
    category_id: int = Path(..., description="分类ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除资料分类"""
    try:
        # 检查分类是否存在
        category = db.query(MaterialCategory).filter(MaterialCategory.id == category_id).first()
        if not category:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "分类不存在",
                    "data": None
                }
            )
        
        # 检查是否有资料使用该分类
        materials = db.query(LearningMaterial).filter(LearningMaterial.category_id == category_id).all()
        if materials:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "该分类下有资料，无法删除",
                    "data": None
                }
            )
        
        # 删除分类
        db.delete(category)
        db.commit()
        
        log_user_action(current_user.id, "delete_material_category", f"删除资料分类: {category.name}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除资料分类成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除资料分类失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除资料分类失败"
        )


# 学习资料相关API

@router.get("/materials", summary="获取学习资料列表")
async def get_learning_materials(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    type: Optional[int] = Query(None, description="资料类型：1-考研，2-考公"),
    category_id: Optional[int] = Query(None, description="分类ID"),
    subject: Optional[str] = Query(None, description="科目"),
    keyword: Optional[str] = Query(None, description="关键词"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取学习资料列表"""
    try:
        query = db.query(LearningMaterial).filter(LearningMaterial.is_valid == True)
        
        # 管理员用户可以看到所有资料，不需要过滤
        if not current_user.is_admin:
            # 获取用户订阅信息
            user_subscription = db.query(UserSubscription).filter(
                UserSubscription.user_id == current_user.id
            ).first()
            subscribe_type = user_subscription.subscribe_type if user_subscription else None
            
            # 根据用户类型自动过滤资料类型
            # vip_type: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP
            # subscribe_type: 1-考研, 2-考公, 3-双赛道
            if current_user.vip_type == 1 or (subscribe_type and subscribe_type == 1):
                # 考研用户只能看到考研资料
                query = query.filter(LearningMaterial.type == 1)
            elif current_user.vip_type == 2 or (subscribe_type and subscribe_type == 2):
                # 考公用户只能看到考公资料
                query = query.filter(LearningMaterial.type == 2)
            # 双赛道用户（vip_type=3或subscribe_type=3）和非VIP用户可以看到所有资料
        
        # 过滤条件
        if type is not None:
            query = query.filter(LearningMaterial.type == type)
        if category_id is not None:
            query = query.filter(LearningMaterial.category_id == category_id)
        if subject:
            query = query.filter(LearningMaterial.subject == subject)
        if keyword:
            query = query.filter(
                LearningMaterial.title.contains(keyword) | 
                LearningMaterial.description.contains(keyword)
            )
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        materials = query.order_by(
            LearningMaterial.upload_time.desc()
        ).offset(offset).limit(page_size).all()
        
        # 计算每个资料的平均评分
        material_items = []
        for m in materials:
            # 获取该资料的所有评分
            ratings = db.query(MaterialRating).filter(MaterialRating.material_id == m.id).all()
            average_rating = 0.0
            if ratings:
                total_rating = sum(r.rating for r in ratings)
                average_rating = round(total_rating / len(ratings), 1)
            
            material_items.append({
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "type": m.type,
                "category_id": m.category_id,
                "category_name": m.category.name if m.category else "",
                "subject": m.subject,
                "file_url": m.file_url,
                "file_size": m.file_size,
                "file_extension": m.file_extension,
                "cover_image": m.cover_image,
                "uploader_id": m.uploader_id,
                "uploader_name": m.uploader.username if m.uploader else "",
                "upload_time": m.upload_time.isoformat(),
                "download_count": m.download_count,
                "rating": average_rating
            })
            
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学习资料列表成功",
                "data": {
                    "total": total,
                    "items": material_items
                }
            }
        )
    except Exception as e:
        log_error(f"获取学习资料列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取学习资料列表失败"
        )


@router.get("/materials/{material_id}", summary="获取学习资料详情")
async def get_learning_material_detail(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取学习资料详情"""
    try:
        material = db.query(LearningMaterial).filter(
            LearningMaterial.id == material_id,
            LearningMaterial.is_valid == True
        ).first()
        
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 计算平均评分
        ratings = db.query(MaterialRating).filter(MaterialRating.material_id == material.id).all()
        average_rating = 0.0
        if ratings:
            total_rating = sum(r.rating for r in ratings)
            average_rating = round(total_rating / len(ratings), 1)
            
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学习资料详情成功",
                "data": {
                    "id": material.id,
                    "title": material.title,
                    "description": material.description,
                    "type": material.type,
                    "category_id": material.category_id,
                    "category_name": material.category.name if material.category else "",
                    "subject": material.subject,
                    "file_path": material.file_path,
                    "file_url": material.file_url,
                    "file_size": material.file_size,
                    "file_extension": material.file_extension,
                    "cover_image": material.cover_image,
                    "uploader_id": material.uploader_id,
                    "uploader_name": material.uploader.username if material.uploader else "",
                    "upload_time": material.upload_time.isoformat(),
                    "download_count": material.download_count,
                    "rating": average_rating
                }
            }
        )
    except Exception as e:
        log_error(f"获取学习资料详情失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取学习资料详情失败"
        )


@router.post("/materials", summary="上传学习资料")
async def upload_learning_material(
    title: str = Form(..., description="资料标题"),
    description: str = Form(..., description="资料描述"),
    type: int = Form(..., description="资料类型：1-考研，2-考公"),
    category_id: int = Form(..., description="分类ID"),
    subject: str = Form(..., description="科目"),
    file: UploadFile = File(..., description="资料文件"),
    cover_image: Optional[UploadFile] = File(None, description="封面图片"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """上传学习资料"""
    try:
        # 检查分类是否存在
        category = db.query(MaterialCategory).filter(MaterialCategory.id == category_id).first()
        if not category:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "分类不存在",
                    "data": None
                }
            )
        
        # 创建文件存储目录
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        
        # 保存文件
        file_extension = os.path.splitext(file.filename)[1]
        file_name = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(upload_dir, file_name)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # 保存封面图片（如果有）
        cover_image_url = None
        if cover_image:
            cover_extension = os.path.splitext(cover_image.filename)[1]
            cover_name = f"{uuid.uuid4()}{cover_extension}"
            cover_path = os.path.join(upload_dir, cover_name)
            with open(cover_path, "wb") as f:
                f.write(await cover_image.read())
            cover_image_url = f"/uploads/{cover_name}"
        
        # 创建资料
        material = LearningMaterial(
            title=title,
            description=description,
            type=type,
            category_id=category_id,
            subject=subject,
            file_path=file_path,
            file_url=f"/uploads/{file_name}",
            file_size=os.path.getsize(file_path),
            file_extension=file_extension,
            cover_image=cover_image_url,
            uploader_id=current_user.id,
            upload_time=datetime.now()
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        
        log_user_action(current_user.id, "upload_learning_material", f"上传学习资料: {title}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "上传学习资料成功",
                "data": {
                    "id": material.id,
                    "title": material.title,
                    "file_url": material.file_url
                }
            }
        )
    except Exception as e:
        log_error(f"上传学习资料失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="上传学习资料失败"
        )


@router.put("/materials/{material_id}", summary="更新学习资料")
async def update_learning_material(
    material_id: int = Path(..., description="资料ID"),
    title: Optional[str] = Form(None, description="资料标题"),
    description: Optional[str] = Form(None, description="资料描述"),
    type: Optional[int] = Form(None, description="资料类型：1-考研，2-考公"),
    category_id: Optional[int] = Form(None, description="分类ID"),
    subject: Optional[str] = Form(None, description="科目"),
    file: Optional[UploadFile] = File(None, description="资料文件"),
    cover_image: Optional[UploadFile] = File(None, description="封面图片"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """更新学习资料"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 检查分类是否存在（如果更新分类）
        if category_id is not None:
            category = db.query(MaterialCategory).filter(MaterialCategory.id == category_id).first()
            if not category:
                return JSONResponse(
                    status_code=404,
                    content={
                        "success": False,
                        "code": 404,
                        "message": "分类不存在",
                        "data": None
                    }
                )
        
        # 更新资料信息
        if title is not None:
            material.title = title
        if description is not None:
            material.description = description
        if type is not None:
            material.type = type
        if category_id is not None:
            material.category_id = category_id
        if subject is not None:
            material.subject = subject
        
        # 更新文件（如果有）
        if file:
            # 删除旧文件
            if os.path.exists(material.file_path):
                os.remove(material.file_path)
            
            # 保存新文件
            file_extension = os.path.splitext(file.filename)[1]
            file_name = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join("uploads", file_name)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            
            material.file_path = file_path
            material.file_url = f"/uploads/{file_name}"
            material.file_size = os.path.getsize(file_path)
            material.file_extension = file_extension
        
        # 更新封面图片（如果有）
        if cover_image:
            # 删除旧封面图片
            if material.cover_image and os.path.exists(os.path.join("uploads", os.path.basename(material.cover_image))):
                os.remove(os.path.join("uploads", os.path.basename(material.cover_image)))
            
            # 保存新封面图片
            cover_extension = os.path.splitext(cover_image.filename)[1]
            cover_name = f"{uuid.uuid4()}{cover_extension}"
            cover_path = os.path.join("uploads", cover_name)
            with open(cover_path, "wb") as f:
                f.write(await cover_image.read())
            
            material.cover_image = f"/uploads/{cover_name}"
        
        db.commit()
        db.refresh(material)
        
        log_user_action(current_user.id, "update_learning_material", f"更新学习资料: {material.title}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新学习资料成功",
                "data": {
                    "id": material.id,
                    "title": material.title,
                    "file_url": material.file_url
                }
            }
        )
    except Exception as e:
        log_error(f"更新学习资料失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="更新学习资料失败"
        )


@router.delete("/materials/{material_id}", summary="删除学习资料")
async def delete_learning_material(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除学习资料"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 删除文件
        if os.path.exists(material.file_path):
            os.remove(material.file_path)
        
        # 删除封面图片
        if material.cover_image and os.path.exists(os.path.join("uploads", os.path.basename(material.cover_image))):
            os.remove(os.path.join("uploads", os.path.basename(material.cover_image)))
        
        # 删除资料
        db.delete(material)
        db.commit()
        
        log_user_action(current_user.id, "delete_learning_material", f"删除学习资料: {material.title}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除学习资料成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除学习资料失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除学习资料失败"
        )


@router.get("/materials/{material_id}/download", summary="下载学习资料")
async def download_learning_material(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """下载学习资料"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(
            LearningMaterial.id == material_id,
            LearningMaterial.is_valid == True
        ).first()
        
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        file_path = material.file_path
        if not os.path.isabs(file_path):
            file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), file_path)
        
        if not os.path.exists(file_path):
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "文件不存在",
                    "data": None
                }
            )
        
        # 增加下载次数
        material.download_count += 1
        
        # 记录下载记录
        download_record = UserDownload(
            user_id=current_user.id,
            material_id=material_id,
            download_time=datetime.now()
        )
        db.add(download_record)
        
        db.commit()
        
        log_user_action(current_user.id, "download_learning_material", f"下载学习资料: {material.title}")
        
        return FileResponse(
            path=file_path,
            filename=material.title + material.file_extension,
            media_type="application/octet-stream"
        )
    except Exception as e:
        log_error(f"下载学习资料失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="下载学习资料失败"
        )


# 用户下载记录相关API

@router.post("/materials/{material_id}/favorite", summary="添加收藏")
async def add_material_favorite(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """添加学习资料收藏"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(
            LearningMaterial.id == material_id,
            LearningMaterial.is_valid == True
        ).first()
        
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 检查是否已经收藏过
        existing_favorite = db.query(UserMaterialFavorite).filter(
            UserMaterialFavorite.user_id == current_user.id,
            UserMaterialFavorite.material_id == material_id
        ).first()
        
        if existing_favorite:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "您已收藏过该资料",
                    "data": None
                }
            )
        
        # 添加收藏
        favorite = UserMaterialFavorite(
            user_id=current_user.id,
            material_id=material_id
        )
        
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        
        log_user_action(current_user.id, "add_material_favorite", f"收藏学习资料: {material.title}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "收藏成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"添加收藏失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="添加收藏失败"
        )


@router.delete("/materials/{material_id}/favorite", summary="取消收藏")
async def remove_material_favorite(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """取消学习资料收藏"""
    try:
        # 检查收藏是否存在
        favorite = db.query(UserMaterialFavorite).filter(
            UserMaterialFavorite.user_id == current_user.id,
            UserMaterialFavorite.material_id == material_id
        ).first()
        
        if not favorite:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "收藏不存在",
                    "data": None
                }
            )
        
        # 删除收藏
        db.delete(favorite)
        db.commit()
        
        log_user_action(current_user.id, "remove_material_favorite", f"取消收藏学习资料: {material_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "取消收藏成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"取消收藏失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="取消收藏失败"
        )


@router.get("/favorites", summary="获取用户收藏的学习资料")
async def get_user_material_favorites(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    type: Optional[int] = Query(None, description="资料类型：1-考研，2-考公"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取用户收藏的学习资料"""
    try:
        query = db.query(LearningMaterial).join(
            UserMaterialFavorite,
            LearningMaterial.id == UserMaterialFavorite.material_id
        ).filter(
            UserMaterialFavorite.user_id == current_user.id,
            LearningMaterial.is_valid == True
        )
        
        # 根据用户类型自动过滤资料类型
        if not current_user.is_admin:
            user_subscription = db.query(UserSubscription).filter(
                UserSubscription.user_id == current_user.id
            ).first()
            subscribe_type = user_subscription.subscribe_type if user_subscription else None
            
            if current_user.vip_type == 1 or (subscribe_type and subscribe_type == 1):
                query = query.filter(LearningMaterial.type == 1)
            elif current_user.vip_type == 2 or (subscribe_type and subscribe_type == 2):
                query = query.filter(LearningMaterial.type == 2)
        
        # 按资料类型过滤（如果有明确指定）
        if type is not None:
            query = query.filter(LearningMaterial.type == type)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        materials = query.order_by(
            UserMaterialFavorite.created_at.desc()
        ).offset(offset).limit(page_size).all()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取收藏资料成功",
                "data": {
                    "total": total,
                    "items": [{
                        "id": m.id,
                        "title": m.title,
                        "description": m.description,
                        "type": m.type,
                        "category_id": m.category_id,
                        "category_name": m.category.name if m.category else "",
                        "subject": m.subject,
                        "file_url": m.file_url,
                        "file_size": m.file_size,
                        "file_extension": m.file_extension,
                        "cover_image": m.cover_image,
                        "uploader_id": m.uploader_id,
                        "uploader_name": m.uploader.username if m.uploader else "",
                        "upload_time": m.upload_time.isoformat(),
                        "download_count": m.download_count,
                        "rating": m.rating
                    } for m in materials]
                }
            }
        )
    except Exception as e:
        log_error(f"获取收藏资料失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取收藏资料失败"
        )


@router.get("/materials/{material_id}/favorite", summary="检查是否已收藏")
async def check_material_favorite(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """检查学习资料是否已收藏"""
    try:
        # 检查收藏是否存在
        favorite = db.query(UserMaterialFavorite).filter(
            UserMaterialFavorite.user_id == current_user.id,
            UserMaterialFavorite.material_id == material_id
        ).first()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "检查收藏状态成功",
                "data": {
                    "is_favorite": favorite is not None
                }
            }
        )
    except Exception as e:
        log_error(f"检查收藏状态失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="检查收藏状态失败"
        )


@router.get("/downloads", summary="获取用户下载记录")
async def get_user_downloads(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    type: Optional[int] = Query(None, description="资料类型：1-考研，2-考公"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取用户下载记录"""
    try:
        query = db.query(UserDownload).filter(UserDownload.user_id == current_user.id)
        
        # 获取用户订阅信息
        user_subscription = db.query(UserSubscription).filter(
            UserSubscription.user_id == current_user.id
        ).first()
        subscribe_type = user_subscription.subscribe_type if user_subscription else None
        
        # 根据用户类型自动过滤下载记录
        # vip_type: 0-非VIP, 1-考研VIP, 2-考公VIP, 3-双赛道VIP
        # subscribe_type: 1-考研, 2-考公, 3-双赛道
        if current_user.vip_type == 1 or (subscribe_type and subscribe_type == 1):
            # 考研用户只能看到考研资料的下载记录
            query = query.join(LearningMaterial).filter(LearningMaterial.type == 1)
        elif current_user.vip_type == 2 or (subscribe_type and subscribe_type == 2):
            # 考公用户只能看到考公资料的下载记录
            query = query.join(LearningMaterial).filter(LearningMaterial.type == 2)
        # 双赛道用户（vip_type=3或subscribe_type=3）和非VIP用户可以看到所有下载记录
        
        # 按资料类型过滤（如果有明确指定）
        if type is not None:
            query = query.join(LearningMaterial).filter(LearningMaterial.type == type)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        downloads = query.order_by(
            UserDownload.download_time.desc()
        ).offset(offset).limit(page_size).all()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取用户下载记录成功",
                "data": {
                    "total": total,
                    "items": [{
                        "id": d.id,
                        "material_id": d.material_id,
                        "material_title": d.material.title if d.material else "",
                        "material_type": d.material.type if d.material else 0,
                        "download_time": d.download_time.isoformat()
                    } for d in downloads]
                }
            }
        )
    except Exception as e:
        log_error(f"获取用户下载记录失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取用户下载记录失败"
        )


@router.delete("/downloads/{download_id}", summary="删除下载记录")
async def delete_download_record(
    download_id: int = Path(..., description="下载记录ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除下载记录"""
    try:
        # 检查下载记录是否存在且属于当前用户
        download_record = db.query(UserDownload).filter(
            UserDownload.id == download_id,
            UserDownload.user_id == current_user.id
        ).first()
        
        if not download_record:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "下载记录不存在",
                    "data": None
                }
            )
        
        # 删除下载记录
        db.delete(download_record)
        db.commit()
        
        log_user_action(current_user.id, "delete_download_record", f"删除下载记录: {download_record.id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除下载记录成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除下载记录失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除下载记录失败"
        )


# 资料评分和评论相关API

@router.get("/materials/{material_id}/rating", summary="检查是否已评分")
async def check_material_rating(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """检查学习资料是否已评分"""
    try:
        # 检查评分是否存在
        rating = db.query(MaterialRating).filter(
            MaterialRating.user_id == current_user.id,
            MaterialRating.material_id == material_id
        ).first()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "检查评分状态成功",
                "data": {
                    "has_rated": rating is not None,
                    "rating": rating.rating if rating else None
                }
            }
        )
    except Exception as e:
        log_error(f"检查评分状态失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="检查评分状态失败"
        )


@router.post("/materials/{material_id}/rating", summary="给资料评分")
async def rate_material(
    material_id: int = Path(..., description="资料ID"),
    rating: int = Form(..., ge=1, le=10, description="评分，1-10分"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """给资料评分"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 检查是否已经评分
        existing_rating = db.query(MaterialRating).filter(
            MaterialRating.user_id == current_user.id,
            MaterialRating.material_id == material_id
        ).first()
        
        if existing_rating:
            # 用户已经评价过，返回提示
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "您已经评价过该资料，不能重复评价",
                    "data": None
                }
            )
        else:
            # 创建评分
            new_rating = MaterialRating(
                user_id=current_user.id,
                material_id=material_id,
                rating=rating
            )
            db.add(new_rating)
        
        # 更新资料的平均评分
        ratings = db.query(MaterialRating).filter(MaterialRating.material_id == material_id).all()
        if ratings:
            average_rating = sum(r.rating for r in ratings) / len(ratings)
            material.rating = average_rating
        else:
            material.rating = 0
        
        db.commit()
        
        log_user_action(current_user.id, "rate_material", f"给资料评分: {material.title}, 评分: {rating}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "评分成功",
                "data": {
                    "material_id": material_id,
                    "rating": rating,
                    "average_rating": material.rating
                }
            }
        )
    except Exception as e:
        log_error(f"给资料评分失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="给资料评分失败"
        )


@router.post("/materials/{material_id}/comment", summary="给资料评论")
async def comment_material(
    material_id: int = Path(..., description="资料ID"),
    comment: str = Form(..., description="评论内容"),
    parent_comment_id: Optional[int] = Form(None, description="父评论ID（回复功能）"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """给资料评论"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 检查用户类型和资料类型是否匹配
        # 考研用户只能评论考研资料，考公用户只能评论考公资料
        # 双赛道用户和管理员可以评论所有类型
        if not (current_user.is_admin or current_user.vip_type == 3):
            # 普通用户只能评论对应类型的资料
            if current_user.vip_type == 1 and material.type != 1:
                return JSONResponse(
                    status_code=403,
                    content={
                        "success": False,
                        "code": 403,
                        "message": "考研用户只能评论考研相关的学习资料",
                        "data": None
                    }
                )
            elif current_user.vip_type == 2 and material.type != 2:
                return JSONResponse(
                    status_code=403,
                    content={
                        "success": False,
                        "code": 403,
                        "message": "考公用户只能评论考公相关的学习资料",
                        "data": None
                    }
                )
        
        # 检查是否是回复评论，如果是，检查父评论是否存在
        if parent_comment_id:
            parent_comment = db.query(MaterialComment).filter(
                MaterialComment.id == parent_comment_id,
                MaterialComment.material_id == material_id
            ).first()
            if not parent_comment:
                return JSONResponse(
                    status_code=404,
                    content={
                        "success": False,
                        "code": 404,
                        "message": "父评论不存在",
                        "data": None
                    }
                )
        
        # 创建评论（允许重复评论和回复）
        new_comment = MaterialComment(
            user_id=current_user.id,
            material_id=material_id,
            parent_comment_id=parent_comment_id,
            comment=comment
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        
        log_user_action(current_user.id, "comment_material", f"给资料评论: {material.title}")
        
        from fastapi.responses import JSONResponse
        
        response_data = {
            "success": True,
            "code": 200,
            "message": "评论成功",
            "data": {
                "id": new_comment.id,
                "comment": new_comment.comment,
                "created_at": new_comment.created_at.isoformat()
            }
        }
        
        print(f"响应数据: {response_data}")
        print(f"评论内容类型: {type(new_comment.comment)}")
        
        return JSONResponse(
            status_code=200,
            content=response_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        log_error(f"给资料评论失败: {str(e)}")
        import traceback
        log_error(f"详细错误信息: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"给资料评论失败: {str(e)}"
        )


@router.delete("/materials/{material_id}/comments/{comment_id}", summary="删除资料评论")
async def delete_material_comment(
    material_id: int = Path(..., description="资料ID"),
    comment_id: int = Path(..., description="评论ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除资料评论"""
    try:
        # 检查评论是否存在
        comment = db.query(MaterialComment).filter(
            MaterialComment.id == comment_id,
            MaterialComment.material_id == material_id
        ).first()
        
        if not comment:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "评论不存在",
                    "data": None
                }
            )
        
        # 检查用户是否有权限删除该评论
        if not (current_user.is_admin or comment.user_id == current_user.id):
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "code": 403,
                    "message": "您没有权限删除该评论",
                    "data": None
                }
            )
        
        # 删除该评论及其所有子评论（递归删除）
        def delete_comment_recursive(comment_id):
            # 删除所有子评论
            child_comments = db.query(MaterialComment).filter(
                MaterialComment.parent_comment_id == comment_id
            ).all()
            for child in child_comments:
                delete_comment_recursive(child.id)
            # 删除当前评论
            comment_to_delete = db.query(MaterialComment).filter(
                MaterialComment.id == comment_id
            ).first()
            if comment_to_delete:
                db.delete(comment_to_delete)
        
        # 开始递归删除
        delete_comment_recursive(comment_id)
        db.commit()
        
        log_user_action(current_user.id, "delete_comment", f"删除评论: {material_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除评论成功",
                "data": None
            }
        )
        
    except Exception as e:
        log_error(f"删除评论失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除评论失败"
        )

@router.get("/comments", summary="获取所有评论")
async def get_all_comments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    keyword: Optional[str] = Query(None, description="关键词搜索"),
    type: Optional[int] = Query(None, description="资料类型：1-考研，2-考公"),
    date: Optional[str] = Query(None, description="时间筛选：today/week/month"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取所有评论"""
    try:
        # 检查用户是否是管理员
        if not current_user.is_admin:
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "code": 403,
                    "message": "您没有权限访问此API",
                    "data": None
                }
            )
        
        query = db.query(MaterialComment).join(
            LearningMaterial, MaterialComment.material_id == LearningMaterial.id
        )
        
        # 关键词搜索
        if keyword:
            query = query.filter(
                MaterialComment.comment.contains(keyword) | 
                MaterialComment.user.has(username.contains(keyword))
            )
        
        # 类型筛选
        if type:
            query = query.filter(LearningMaterial.type == type)
        
        # 时间筛选
        if date:
            now = datetime.now()
            if date == "today":
                query = query.filter(MaterialComment.created_at >= now.replace(hour=0, minute=0, second=0, microsecond=0))
            elif date == "week":
                week_ago = now - timedelta(days=7)
                query = query.filter(MaterialComment.created_at >= week_ago)
            elif date == "month":
                month_ago = now - timedelta(days=30)
                query = query.filter(MaterialComment.created_at >= month_ago)
        
        # 计算总数
        total = query.count()
        
        # 分页
        offset = (page - 1) * page_size
        comments = query.order_by(
            MaterialComment.created_at.desc()
        ).offset(offset).limit(page_size).all()
        
        # 构建评论数据
        comment_items = []
        for comment in comments:
            # 获取父评论内容
            parent_comment = None
            if comment.parent_comment_id:
                parent = db.query(MaterialComment).filter(MaterialComment.id == comment.parent_comment_id).first()
                if parent:
                    parent_comment = parent.comment
            
            # 计算评论层级
            depth = 0
            temp_comment = comment
            while temp_comment.parent_comment_id:
                depth += 1
                temp_comment = db.query(MaterialComment).filter(MaterialComment.id == temp_comment.parent_comment_id).first()
            
            comment_items.append({
                "id": comment.id,
                "user_id": comment.user_id,
                "user_name": comment.user.username if comment.user else "",
                "material_id": comment.material_id,
                "material_title": comment.material.title if comment.material else "",
                "material_type": comment.material.type if comment.material else 0,
                "comment": comment.comment,
                "parent_comment_id": comment.parent_comment_id,
                "parent_comment": parent_comment,
                "depth": depth,
                "created_at": comment.created_at.isoformat()
            })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取评论成功",
                "data": {
                    "total": total,
                    "items": comment_items
                }
            }
        )
    except Exception as e:
        log_error(f"获取评论失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取评论失败"
        )


@router.delete("/comments/{comment_id}", summary="删除评论")
async def delete_comment(
    comment_id: int = Path(..., description="评论ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除评论"""
    try:
        # 检查评论是否存在
        comment = db.query(MaterialComment).filter(MaterialComment.id == comment_id).first()
        
        if not comment:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "评论不存在",
                    "data": None
                }
            )
        
        # 检查用户是否有权限删除该评论
        if not current_user.is_admin:
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "code": 403,
                    "message": "您没有权限删除该评论",
                    "data": None
                }
            )
        
        # 删除该评论及其所有子评论（递归删除）
        def delete_comment_recursive(comment_id):
            # 删除所有子评论
            child_comments = db.query(MaterialComment).filter(
                MaterialComment.parent_comment_id == comment_id
            ).all()
            for child in child_comments:
                delete_comment_recursive(child.id)
            # 删除当前评论
            comment_to_delete = db.query(MaterialComment).filter(
                MaterialComment.id == comment_id
            ).first()
            if comment_to_delete:
                db.delete(comment_to_delete)
        
        # 开始递归删除
        delete_comment_recursive(comment_id)
        db.commit()
        
        log_user_action(current_user.id, "delete_comment", f"删除评论: {comment_id}")
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除评论成功",
                "data": None
            }
        )
    except Exception as e:
        log_error(f"删除评论失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除评论失败"
        )


@router.get("/comments/export", summary="导出评论")
async def export_comments(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """导出评论"""
    try:
        # 检查用户是否是管理员
        if not current_user.is_admin:
            return JSONResponse(
                status_code=403,
                content={
                    "success": False,
                    "code": 403,
                    "message": "您没有权限导出评论",
                    "data": None
                }
            )
        
        # 获取所有评论
        comments = db.query(MaterialComment).join(
            LearningMaterial, MaterialComment.material_id == LearningMaterial.id
        ).all()
        
        # 构建评论数据
        comment_data = []
        for comment in comments:
            # 获取父评论内容
            parent_comment = None
            if comment.parent_comment_id:
                parent = db.query(MaterialComment).filter(MaterialComment.id == comment.parent_comment_id).first()
                if parent:
                    parent_comment = parent.comment
            
            # 计算评论层级
            depth = 0
            temp_comment = comment
            while temp_comment.parent_comment_id:
                depth += 1
                temp_comment = db.query(MaterialComment).filter(MaterialComment.id == temp_comment.parent_comment_id).first()
            
            comment_data.append({
                "ID": comment.id,
                "用户名": comment.user.username if comment.user else "",
                "用户ID": comment.user_id,
                "资料标题": comment.material.title if comment.material else "",
                "资料ID": comment.material_id,
                "资料类型": "考研" if comment.material.type == 1 else "考公" if comment.material.type == 2 else "未知",
                "评论内容": comment.comment,
                "父评论ID": comment.parent_comment_id,
                "父评论内容": parent_comment,
                "评论层级": depth,
                "评论时间": comment.created_at.isoformat()
            })
        
        # 导出为CSV
        from io import StringIO
        import csv
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=comment_data[0].keys() if comment_data else [])
        writer.writeheader()
        writer.writerows(comment_data)
        
        output.seek(0)
        
        from fastapi.responses import StreamingResponse
        
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=comments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
    except Exception as e:
        log_error(f"导出评论失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="导出评论失败"
        )


@router.get("/materials/{material_id}/comments", summary="获取资料评论")
async def get_material_comments(
    material_id: int = Path(..., description="资料ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取资料评论"""
    try:
        # 检查资料是否存在
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "资料不存在",
                    "data": None
                }
            )
        
        # 获取该资料的所有评论（不分页，确保嵌套回复结构完整）
        query = db.query(MaterialComment).filter(MaterialComment.material_id == material_id)
        comments = query.order_by(
            MaterialComment.created_at.desc()
        ).all()
        
        # 构建评论树（支持嵌套回复）
        comment_tree = []
        comment_map = {}
        
        # 先将所有评论存入map
        for comment in comments:
            comment_map[comment.id] = {
                "id": comment.id,
                "user_id": comment.user_id,
                "user_name": comment.user.username if comment.user else "",
                "comment": comment.comment,
                "created_at": comment.created_at.isoformat(),
                "parent_comment_id": comment.parent_comment_id,
                "replies": []
            }
        
        # 构建树结构
        for comment in comments:
            if comment.parent_comment_id is None:
                # 顶级评论
                comment_tree.append(comment_map[comment.id])
            else:
                # 回复评论
                if comment.parent_comment_id in comment_map:
                    comment_map[comment.parent_comment_id]["replies"].append(comment_map[comment.id])
        
        from fastapi.responses import JSONResponse
        
        response_data = {
            "success": True,
            "code": 200,
            "message": "获取资料评论成功",
            "data": {
                "total": len(comments),
                "items": comment_tree
            }
        }
        
        return JSONResponse(
            status_code=200,
            content=response_data,
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
    except Exception as e:
        log_error(f"获取资料评论失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取资料评论失败"
        )
