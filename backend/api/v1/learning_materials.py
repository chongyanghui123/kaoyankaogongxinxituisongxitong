from fastapi import APIRouter, Depends, HTTPException, Query, Path, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from sqlalchemy import desc, or_

from core.database import get_db_common
from core.security import get_current_user
from models.learning_materials import (
    ExamSchedule, Carousel, MaterialCategory, LearningMaterial,
    UserDownload, MaterialRating, MaterialComment
)
from models.users import UserFavorite
from models.users import User
from schemas.learning_materials import (
    ExamScheduleCreate, ExamScheduleUpdate, ExamScheduleResponse, 
    ExamScheduleWithCountdown, ExamScheduleList,
    CarouselCreate, CarouselUpdate, CarouselResponse, CarouselList
)

router = APIRouter(tags=["learning_materials"])


@router.get("/categories")
async def get_categories(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        categories = db.query(MaterialCategory).order_by(MaterialCategory.id).all()
        result = []
        for cat in categories:
            result.append({
                "id": cat.id,
                "name": cat.name,
                "type": cat.type,
                "description": cat.description,
                "created_at": cat.created_at.isoformat() if cat.created_at else None
            })
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取资料分类列表成功",
                "data": result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取资料分类列表失败: {str(e)}",
                "data": None
            }
        )


@router.get("/materials/{material_id}")
async def get_material(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取单个学习资料"""
    try:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "学习资料不存在", "data": None}
            )
        
        # 检查用户是否有访问权限
        if material.is_vip and not current_user.is_vip:
            return JSONResponse(
                status_code=403,
                content={"success": False, "code": 403, "message": "该资料仅VIP用户可见", "data": None}
            )
        
        # 根据用户类型过滤资料
        if current_user.is_vip:
            if current_user.vip_type == 1 and material.type != 1:
                return JSONResponse(
                    status_code=403,
                    content={"success": False, "code": 403, "message": "该资料仅考研VIP用户可见", "data": None}
                )
            elif current_user.vip_type == 2 and material.type != 2:
                return JSONResponse(
                    status_code=403,
                    content={"success": False, "code": 403, "message": "该资料仅考公VIP用户可见", "data": None}
                )
        
        category_name = None
        if material.category:
            category_name = material.category.name
        
        result = {
            "id": material.id,
            "title": material.title,
            "description": material.description,
            "category_id": material.category_id,
            "category_name": category_name,
            "type": material.type,
            "subject": material.subject,
            "file_url": material.file_url,
            "cover_image": material.cover_image,
            "file_size": material.file_size,
            "file_extension": material.file_extension,
            "download_count": material.download_count,
            "rating": material.rating,
            "is_valid": material.is_valid,
            "is_vip": material.is_vip,
            "created_at": material.created_at.isoformat() if material.created_at else None,
            "updated_at": material.updated_at.isoformat() if material.updated_at else None
        }
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学习资料成功",
                "data": result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取学习资料失败: {str(e)}",
                "data": None
            }
        )


@router.get("/materials")
async def get_materials(
    db: Session = Depends(get_db_common),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    category_id: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user)
):
    try:
        query = db.query(LearningMaterial)

        if keyword:
            query = query.filter(LearningMaterial.title.contains(keyword))
        if type:
            try:
                type_int = int(type)
                query = query.filter(LearningMaterial.type == type_int)
            except (ValueError, TypeError):
                pass
        if category_id:
            try:
                cat_id = int(category_id)
                query = query.filter(LearningMaterial.category_id == cat_id)
            except (ValueError, TypeError):
                pass

        query = query.filter(LearningMaterial.is_valid == True)
        
        # 根据用户VIP状态和类型过滤资料
        if not current_user.is_vip:
            query = query.filter(LearningMaterial.is_vip == False)
        else:
            # 考研VIP用户只能看到考研类型的资料
            if current_user.vip_type == 1:
                query = query.filter(LearningMaterial.type == 1)
            # 考公VIP用户只能看到考公类型的资料
            elif current_user.vip_type == 2:
                query = query.filter(LearningMaterial.type == 2)
            # 双赛道VIP用户可以看到所有类型的资料
            elif current_user.vip_type == 3:
                pass
            
        query = query.order_by(desc(LearningMaterial.created_at))

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for item in items:
            category_name = None
            if item.category:
                category_name = item.category.name
            result.append({
                "id": item.id,
                "title": item.title,
                "description": item.description,
                "category_id": item.category_id,
                "category_name": category_name,
                "type": item.type,
                "subject": item.subject,
                "file_url": item.file_url,
                "cover_image": item.cover_image,
                "file_size": item.file_size,
                "file_extension": item.file_extension,
                "download_count": item.download_count,
                "rating": item.rating,
                "is_valid": item.is_valid,
                "is_vip": item.is_vip,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学习资料列表成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取学习资料列表失败: {str(e)}",
                "data": None
            }
        )


@router.post("/materials")
async def create_material(
    title: str = Form(...),
    description: str = Form(...),
    type: str = Form(...),
    category_id: str = Form(...),
    subject: str = Form(None),
    is_vip: str = Form("false"),
    file: UploadFile = File(None),
    cover_image: UploadFile = File(None),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        file_url = None
        if file:
            import os
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "materials")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            file_url = f"/uploads/materials/{file.filename}"

        cover_image_url = None
        if cover_image:
            import os
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "covers")
            os.makedirs(upload_dir, exist_ok=True)
            cover_path = os.path.join(upload_dir, cover_image.filename)
            with open(cover_path, "wb") as f:
                content = await cover_image.read()
                f.write(content)
            cover_image_url = f"/uploads/covers/{cover_image.filename}"

        try:
            cat_id = int(category_id)
        except (ValueError, TypeError):
            cat_id = None

        try:
            type_int = int(type)
        except (ValueError, TypeError):
            type_int = 0

        material = LearningMaterial(
            title=title,
            description=description,
            type=type_int,
            category_id=cat_id,
            subject=subject,
            is_vip=is_vip.lower() == "true",
            file_url=file_url,
            cover_image=cover_image_url,
            uploader_id=current_user.id,
            upload_time=datetime.now(),
            is_valid=True
        )
        db.add(material)
        db.commit()
        db.refresh(material)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "创建学习资料成功",
                "data": {
                    "id": material.id,
                    "title": material.title,
                    "description": material.description,
                    "category_id": material.category_id,
                    "type": material.type,
                    "file_url": material.file_url,
                    "cover_image": material.cover_image,
                    "is_valid": material.is_valid,
                    "created_at": material.created_at.isoformat() if material.created_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"创建学习资料失败: {str(e)}",
                "data": None
            }
        )


@router.put("/materials/{material_id}")
async def update_material(
    material_id: int,
    title: str = Form(None),
    description: str = Form(None),
    type: str = Form(None),
    category_id: str = Form(None),
    subject: str = Form(None),
    is_vip: str = Form(None),
    file: UploadFile = File(None),
    cover_image: UploadFile = File(None),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "学习资料不存在", "data": None}
            )

        if title is not None:
            material.title = title
        if description is not None:
            material.description = description
        if type is not None:
            try:
                material.type = int(type)
            except (ValueError, TypeError):
                pass
        if category_id is not None:
            try:
                material.category_id = int(category_id)
            except (ValueError, TypeError):
                pass
        if subject is not None:
            material.subject = subject
        if is_vip is not None:
            material.is_vip = is_vip.lower() == "true"

        if file:
            import os
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "materials")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as f:
                content = await file.read()
                f.write(content)
            material.file_url = f"/uploads/materials/{file.filename}"

        if cover_image:
            import os
            upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "covers")
            os.makedirs(upload_dir, exist_ok=True)
            cover_path = os.path.join(upload_dir, cover_image.filename)
            with open(cover_path, "wb") as f:
                content = await cover_image.read()
                f.write(content)
            material.cover_image = f"/uploads/covers/{cover_image.filename}"

        db.commit()
        db.refresh(material)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新学习资料成功",
                "data": {
                    "id": material.id,
                    "title": material.title,
                    "description": material.description,
                    "category_id": material.category_id,
                    "type": material.type,
                    "file_url": material.file_url,
                    "cover_image": material.cover_image,
                    "is_valid": material.is_valid,
                    "updated_at": material.updated_at.isoformat() if material.updated_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"更新学习资料失败: {str(e)}", "data": None}
        )


@router.delete("/materials/{material_id}")
async def delete_material(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "学习资料不存在", "data": None}
            )
        material.is_valid = False
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除学习资料成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除学习资料失败: {str(e)}", "data": None}
        )


@router.get("/materials/{material_id}/download")
async def download_material(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "学习资料不存在", "data": None}
            )

        material.download_count = (material.download_count or 0) + 1

        download_record = UserDownload(
            user_id=current_user.id,
            material_id=material_id,
            download_time=datetime.now()
        )
        db.add(download_record)
        db.commit()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取下载链接成功",
                "data": {
                    "id": material.id,
                    "title": material.title,
                    "file_url": material.file_url,
                    "file_size": material.file_size,
                    "download_count": material.download_count
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"下载学习资料失败: {str(e)}", "data": None}
        )


@router.post("/materials/{material_id}/rating")
async def rate_material(
    material_id: int,
    rating_data: dict,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "学习资料不存在", "data": None}
            )

        rating_value = rating_data.get("rating", 0)
        existing_rating = db.query(MaterialRating).filter(
            MaterialRating.user_id == current_user.id,
            MaterialRating.material_id == material_id
        ).first()

        if existing_rating:
            existing_rating.rating = rating_value
        else:
            new_rating = MaterialRating(
                user_id=current_user.id,
                material_id=material_id,
                rating=rating_value
            )
            db.add(new_rating)

        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "评分成功", "data": {"rating": rating_value}}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"评分失败: {str(e)}", "data": None}
        )


@router.get("/materials/{material_id}/comments")
async def get_material_comments(
    material_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        query = db.query(MaterialComment).filter(MaterialComment.material_id == material_id)
        query = query.order_by(desc(MaterialComment.created_at))

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for item in items:
            user = db.query(User).filter(User.id == item.user_id).first()
            result.append({
                "id": item.id,
                "material_id": item.material_id,
                "user_id": item.user_id,
                "username": user.username if user else "未知用户",
                "avatar": user.avatar if user else None,
                "content": item.comment,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取评论列表成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取评论列表失败: {str(e)}", "data": None}
        )


@router.post("/materials/{material_id}/comment")
async def add_material_comment(
    material_id: int,
    comment_data: dict,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        material = db.query(LearningMaterial).filter(LearningMaterial.id == material_id).first()
        if not material:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "学习资料不存在", "data": None}
            )

        content = comment_data.get("comment", "")
        if not content:
            return JSONResponse(
                status_code=400,
                content={"success": False, "code": 400, "message": "评论内容不能为空", "data": None}
            )

        comment = MaterialComment(
            user_id=current_user.id,
            material_id=material_id,
            comment=content
        )
        db.add(comment)
        db.commit()
        db.refresh(comment)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "评论成功",
                "data": {
                    "id": comment.id,
                    "material_id": comment.material_id,
                    "user_id": comment.user_id,
                    "username": current_user.username,
                    "content": comment.comment,
                    "created_at": comment.created_at.isoformat() if comment.created_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"评论失败: {str(e)}", "data": None}
        )


@router.get("/comments")
async def get_comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        query = db.query(MaterialComment)

        if keyword:
            query = query.filter(MaterialComment.comment.contains(keyword))
        if date:
            try:
                filter_date = datetime.strptime(date, "%Y-%m-%d")
                next_date = filter_date + timedelta(days=1)
                query = query.filter(
                    MaterialComment.created_at >= filter_date,
                    MaterialComment.created_at < next_date
                )
            except ValueError:
                pass

        query = query.order_by(desc(MaterialComment.created_at))

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for item in items:
            user = db.query(User).filter(User.id == item.user_id).first()
            material = db.query(LearningMaterial).filter(LearningMaterial.id == item.material_id).first()
            result.append({
                "id": item.id,
                "material_id": item.material_id,
                "material_title": material.title if material else "未知资料",
                "material_type": material.type if material else None,
                "user_id": item.user_id,
                "username": user.username if user else "未知用户",
                "avatar": user.avatar if user else None,
                "content": item.comment,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取评论列表成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取评论列表失败: {str(e)}", "data": None}
        )


@router.delete("/comments/{comment_id}")
async def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        comment = db.query(MaterialComment).filter(MaterialComment.id == comment_id).first()
        if not comment:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "评论不存在", "data": None}
            )
        db.delete(comment)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除评论成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除评论失败: {str(e)}", "data": None}
        )


@router.get("/comments/export")
async def export_comments(
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        comments = db.query(MaterialComment).order_by(desc(MaterialComment.created_at)).all()

        result = []
        for item in comments:
            user = db.query(User).filter(User.id == item.user_id).first()
            material = db.query(LearningMaterial).filter(LearningMaterial.id == item.material_id).first()
            result.append({
                "id": item.id,
                "material_title": material.title if material else "未知资料",
                "username": user.username if user else "未知用户",
                "content": item.comment,
                "created_at": item.created_at.isoformat() if item.created_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "导出评论成功",
                "data": result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"导出评论失败: {str(e)}", "data": None}
        )


@router.get("/downloads")
async def get_downloads(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        query = db.query(UserDownload).filter(UserDownload.user_id == current_user.id)
        query = query.order_by(desc(UserDownload.download_time))

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for item in items:
            material = db.query(LearningMaterial).filter(LearningMaterial.id == item.material_id).first()
            result.append({
                "id": item.id,
                "material_id": item.material_id,
                "material_title": material.title if material else "未知资料",
                "download_time": item.download_time.isoformat() if item.download_time else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取下载记录成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取下载记录失败: {str(e)}", "data": None}
        )


@router.get("/exam-schedules")
async def get_exam_schedules(
    db: Session = Depends(get_db_common),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    name: Optional[str] = Query(None, description="考试名称搜索"),
    exam_type: Optional[str] = Query(None, description="考试类型"),
    is_active: Optional[str] = Query(None, description="是否启用")
):
    try:
        query = db.query(ExamSchedule)

        if name:
            query = query.filter(ExamSchedule.name.contains(name))

        if exam_type:
            try:
                exam_type_int = int(exam_type)
                query = query.filter(ExamSchedule.exam_type == exam_type_int)
            except (ValueError, TypeError):
                pass

        if is_active is not None and is_active != "":
            if is_active.lower() in ("true", "1", "yes"):
                query = query.filter(ExamSchedule.is_active == True)
            elif is_active.lower() in ("false", "0", "no"):
                query = query.filter(ExamSchedule.is_active == False)

        query = query.order_by(desc(ExamSchedule.exam_date))

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for item in items:
            result.append({
                "id": item.id,
                "name": item.name,
                "exam_type": item.exam_type,
                "exam_date": item.exam_date.isoformat() if item.exam_date else None,
                "description": item.description,
                "is_active": item.is_active,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取考试日程列表成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取考试日程列表失败: {str(e)}", "data": None}
        )


@router.get("/exam-schedules/active")
async def get_active_exam_schedules(
    db: Session = Depends(get_db_common)
):
    try:
        query = db.query(ExamSchedule).filter(
            ExamSchedule.is_active == True
        ).order_by(desc(ExamSchedule.exam_date))

        schedules = query.all()

        now = datetime.now()
        result = []
        for schedule in schedules:
            countdown = {}
            if schedule.exam_date > now:
                delta = schedule.exam_date - now
                countdown = {
                    "days": delta.days,
                    "hours": delta.seconds // 3600,
                    "minutes": (delta.seconds % 3600) // 60,
                    "seconds": delta.seconds % 60
                }

            result.append({
                "id": schedule.id,
                "name": schedule.name,
                "exam_type": schedule.exam_type,
                "exam_date": schedule.exam_date.isoformat() if schedule.exam_date else None,
                "description": schedule.description,
                "is_active": schedule.is_active,
                "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
                "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None,
                "countdown": countdown
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取启用的考试日程成功",
                "data": result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取启用的考试日程失败: {str(e)}", "data": None}
        )


@router.get("/exam-schedules/{id}")
async def get_exam_schedule(
    id: int = Path(..., description="考试日程ID"),
    db: Session = Depends(get_db_common)
):
    try:
        schedule = db.query(ExamSchedule).filter(ExamSchedule.id == id).first()
        if not schedule:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "考试日程不存在", "data": None}
            )
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取考试日程详情成功",
                "data": {
                    "id": schedule.id,
                    "name": schedule.name,
                    "exam_type": schedule.exam_type,
                    "exam_date": schedule.exam_date.isoformat() if schedule.exam_date else None,
                    "description": schedule.description,
                    "is_active": schedule.is_active,
                    "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
                    "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取考试日程详情失败: {str(e)}", "data": None}
        )


@router.post("/exam-schedules")
async def create_exam_schedule(
    schedule_data: ExamScheduleCreate,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        schedule = ExamSchedule(**schedule_data.dict())
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "创建考试日程成功",
                "data": {
                    "id": schedule.id,
                    "name": schedule.name,
                    "exam_type": schedule.exam_type,
                    "exam_date": schedule.exam_date.isoformat() if schedule.exam_date else None,
                    "description": schedule.description,
                    "is_active": schedule.is_active,
                    "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
                    "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"创建考试日程失败: {str(e)}", "data": None}
        )


@router.put("/exam-schedules/{id}")
async def update_exam_schedule(
    id: int = Path(..., description="考试日程ID"),
    update_data: ExamScheduleUpdate = None,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        schedule = db.query(ExamSchedule).filter(ExamSchedule.id == id).first()
        if not schedule:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "考试日程不存在", "data": None}
            )

        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(schedule, key, value)

        db.commit()
        db.refresh(schedule)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新考试日程成功",
                "data": {
                    "id": schedule.id,
                    "name": schedule.name,
                    "exam_type": schedule.exam_type,
                    "exam_date": schedule.exam_date.isoformat() if schedule.exam_date else None,
                    "description": schedule.description,
                    "is_active": schedule.is_active,
                    "created_at": schedule.created_at.isoformat() if schedule.created_at else None,
                    "updated_at": schedule.updated_at.isoformat() if schedule.updated_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"更新考试日程失败: {str(e)}", "data": None}
        )


@router.delete("/exam-schedules/{id}")
async def delete_exam_schedule(
    id: int = Path(..., description="考试日程ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        schedule = db.query(ExamSchedule).filter(ExamSchedule.id == id).first()
        if not schedule:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "考试日程不存在", "data": None}
            )
        db.delete(schedule)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除考试日程成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除考试日程失败: {str(e)}", "data": None}
        )


@router.get("/carousels")
async def get_carousels(
    db: Session = Depends(get_db_common),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    title: Optional[str] = Query(None, description="标题搜索"),
    is_active: Optional[str] = Query(None, description="是否启用")
):
    try:
        query = db.query(Carousel)

        if title:
            query = query.filter(Carousel.title.contains(title))

        if is_active is not None and is_active != "":
            if is_active.lower() in ("true", "1", "yes"):
                query = query.filter(Carousel.is_active == True)
            elif is_active.lower() in ("false", "0", "no"):
                query = query.filter(Carousel.is_active == False)

        query = query.order_by(Carousel.sort_order, desc(Carousel.created_at))

        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()

        result = []
        for item in items:
            result.append({
                "id": item.id,
                "title": item.title,
                "subtitle": item.subtitle,
                "image_url": item.image_url,
                "link_url": item.link_url,
                "sort_order": item.sort_order,
                "is_active": item.is_active,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取轮播图列表成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取轮播图列表失败: {str(e)}", "data": None}
        )


@router.get("/carousels/active")
async def get_active_carousels(
    db: Session = Depends(get_db_common)
):
    try:
        carousels = db.query(Carousel).filter(
            Carousel.is_active == True
        ).order_by(Carousel.sort_order, desc(Carousel.created_at)).all()

        result = []
        for item in carousels:
            result.append({
                "id": item.id,
                "title": item.title,
                "subtitle": item.subtitle,
                "image_url": item.image_url,
                "link_url": item.link_url,
                "sort_order": item.sort_order,
                "is_active": item.is_active,
                "created_at": item.created_at.isoformat() if item.created_at else None,
                "updated_at": item.updated_at.isoformat() if item.updated_at else None
            })

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取启用的轮播图成功",
                "data": result
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取启用的轮播图失败: {str(e)}", "data": None}
        )


@router.get("/carousels/{id}")
async def get_carousel(
    id: int = Path(..., description="轮播图ID"),
    db: Session = Depends(get_db_common)
):
    try:
        carousel = db.query(Carousel).filter(Carousel.id == id).first()
        if not carousel:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "轮播图不存在", "data": None}
            )
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取轮播图详情成功",
                "data": {
                    "id": carousel.id,
                    "title": carousel.title,
                    "subtitle": carousel.subtitle,
                    "image_url": carousel.image_url,
                    "link_url": carousel.link_url,
                    "sort_order": carousel.sort_order,
                    "is_active": carousel.is_active,
                    "created_at": carousel.created_at.isoformat() if carousel.created_at else None,
                    "updated_at": carousel.updated_at.isoformat() if carousel.updated_at else None
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取轮播图详情失败: {str(e)}", "data": None}
        )


@router.post("/carousels")
async def create_carousel(
    carousel_data: CarouselCreate,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        carousel = Carousel(**carousel_data.dict())
        db.add(carousel)
        db.commit()
        db.refresh(carousel)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "创建轮播图成功",
                "data": {
                    "id": carousel.id,
                    "title": carousel.title,
                    "subtitle": carousel.subtitle,
                    "image_url": carousel.image_url,
                    "link_url": carousel.link_url,
                    "sort_order": carousel.sort_order,
                    "is_active": carousel.is_active,
                    "created_at": carousel.created_at.isoformat() if carousel.created_at else None,
                    "updated_at": carousel.updated_at.isoformat() if carousel.updated_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"创建轮播图失败: {str(e)}", "data": None}
        )


@router.put("/carousels/{id}")
async def update_carousel(
    update_data: CarouselUpdate,
    id: int = Path(..., description="轮播图ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        carousel = db.query(Carousel).filter(Carousel.id == id).first()
        if not carousel:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "轮播图不存在", "data": None}
            )

        update_dict = update_data.dict(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(carousel, key, value)

        db.commit()
        db.refresh(carousel)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新轮播图成功",
                "data": {
                    "id": carousel.id,
                    "title": carousel.title,
                    "subtitle": carousel.subtitle,
                    "image_url": carousel.image_url,
                    "link_url": carousel.link_url,
                    "sort_order": carousel.sort_order,
                    "is_active": carousel.is_active,
                    "created_at": carousel.created_at.isoformat() if carousel.created_at else None,
                    "updated_at": carousel.updated_at.isoformat() if carousel.updated_at else None
                }
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"更新轮播图失败: {str(e)}", "data": None}
        )


@router.get("/materials/{material_id}/favorite")
async def check_favorite(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """检查学习资料是否已收藏"""
    try:
        favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.info_id == material_id,
            UserFavorite.category == 3
        ).first()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取收藏状态成功",
                "data": {
                    "is_favorited": favorite is not None
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取收藏状态失败: {str(e)}", "data": None}
        )


@router.get("/materials/{material_id}/rating")
async def check_rating(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """检查学习资料评分状态"""
    try:
        rating = db.query(MaterialRating).filter(
            MaterialRating.user_id == current_user.id,
            MaterialRating.material_id == material_id
        ).first()

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取评分状态成功",
                "data": {
                    "is_rated": rating is not None,
                    "rating": rating.rating if rating else 0
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"获取评分状态失败: {str(e)}", "data": None}
        )


@router.delete("/materials/{material_id}/comments/{comment_id}")
async def delete_material_comment(
    material_id: int,
    comment_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除学习资料评论"""
    try:
        comment = db.query(MaterialComment).filter(
            MaterialComment.id == comment_id,
            MaterialComment.material_id == material_id
        ).first()
        if not comment:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "评论不存在", "data": None}
            )
        if comment.user_id != current_user.id and not current_user.is_admin:
            return JSONResponse(
                status_code=403,
                content={"success": False, "code": 403, "message": "无权删除此评论", "data": None}
            )
        db.delete(comment)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除评论成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除评论失败: {str(e)}", "data": None}
        )


@router.delete("/downloads/{download_id}")
async def delete_download(
    download_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """删除下载记录"""
    try:
        download = db.query(UserDownload).filter(
            UserDownload.id == download_id,
            UserDownload.user_id == current_user.id
        ).first()
        if not download:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "下载记录不存在", "data": None}
            )
        db.delete(download)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除下载记录成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除下载记录失败: {str(e)}", "data": None}
        )


@router.post("/materials/{material_id}/favorite")
async def add_favorite(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """添加学习资料收藏"""
    try:
        # 检查是否已经收藏
        existing_favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.info_id == material_id,
            UserFavorite.category == 3  # 3-学习资料
        ).first()
        
        if existing_favorite:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "已收藏",
                    "data": None
                }
            )
        
        # 添加收藏
        new_favorite = UserFavorite(
            user_id=current_user.id,
            info_id=material_id,
            category=3
        )
        
        db.add(new_favorite)
        db.commit()
        
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
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"收藏失败: {str(e)}",
                "data": None
            }
        )


@router.delete("/materials/{material_id}/favorite")
async def remove_favorite(
    material_id: int,
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """取消学习资料收藏"""
    try:
        favorite = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.info_id == material_id,
            UserFavorite.category == 3  # 3-学习资料
        ).first()
        
        if not favorite:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "未找到收藏",
                    "data": None
                }
            )
        
        db.delete(favorite)
        db.commit()
        
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
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"取消收藏失败: {str(e)}",
                "data": None
            }
        )


@router.get("/favorites")
async def get_favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    """获取用户收藏的学习资料列表"""
    try:
        query = db.query(UserFavorite).filter(
            UserFavorite.user_id == current_user.id,
            UserFavorite.category == 3  # 3-学习资料
        )
        
        total = query.count()
        items = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 获取学习资料详情
        result = []
        for item in items:
            material = db.query(LearningMaterial).filter(LearningMaterial.id == item.info_id).first()
            if material:
                category_name = None
                if material.category:
                    category_name = material.category.name
                
                result.append({
                    "id": material.id,
                    "title": material.title,
                    "description": material.description,
                    "category_id": material.category_id,
                    "category_name": category_name,
                    "type": material.type,
                    "subject": material.subject,
                    "file_url": material.file_url,
                    "cover_image": material.cover_image,
                    "file_size": material.file_size,
                    "file_extension": material.file_extension,
                    "download_count": material.download_count,
                    "rating": material.rating,
                    "is_valid": material.is_valid,
                    "is_vip": material.is_vip,
                    "created_at": material.created_at.isoformat() if material.created_at else None,
                    "updated_at": material.updated_at.isoformat() if material.updated_at else None
                })
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取收藏列表成功",
                "data": {
                    "total": total,
                    "items": result,
                    "page": page,
                    "page_size": page_size
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取收藏列表失败: {str(e)}",
                "data": None
            }
        )


@router.delete("/carousels/{id}")
async def delete_carousel(
    id: int = Path(..., description="轮播图ID"),
    db: Session = Depends(get_db_common),
    current_user: User = Depends(get_current_user)
):
    try:
        carousel = db.query(Carousel).filter(Carousel.id == id).first()
        if not carousel:
            return JSONResponse(
                status_code=404,
                content={"success": False, "code": 404, "message": "轮播图不存在", "data": None}
            )
        db.delete(carousel)
        db.commit()
        return JSONResponse(
            status_code=200,
            content={"success": True, "code": 200, "message": "删除轮播图成功", "data": None}
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={"success": False, "code": 500, "message": f"删除轮播图失败: {str(e)}", "data": None}
        )
