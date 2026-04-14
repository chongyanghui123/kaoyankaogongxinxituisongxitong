from fastapi import APIRouter, Depends, HTTPException, Query, Body
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from core.database import get_db_common
from core.models.school import School
from core.security import get_current_admin

router = APIRouter()

@router.get("/schools")
async def get_all_schools(
    province: str = Query(None, description="省份筛选"),
    skip: int = Query(0, description="跳过条数"),
    limit: int = Query(100, description="限制条数"),
    db: Session = Depends(get_db_common),
    current_admin = Depends(get_current_admin)
):
    """
    获取所有学校列表（管理员）
    """
    try:
        query = db.query(School)
        if province:
            query = query.filter(School.province == province)
        
        schools = query.offset(skip).limit(limit).all()
        total = query.count()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "获取学校列表成功",
                "data": {
                    "items": [
                        {
                            "id": school.id,
                            "province": school.province,
                            "name": school.name,
                            "has_master": school.has_master,
                            "created_at": school.created_at.isoformat() if school.created_at else None
                        }
                        for school in schools
                    ],
                    "total": total
                }
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"获取学校列表失败: {str(e)}",
                "data": {}
            }
        )

@router.post("/schools")
async def add_school(
    province: str = Body(..., description="省份"),
    name: str = Body(..., description="学校名称"),
    db: Session = Depends(get_db_common),
    current_admin = Depends(get_current_admin)
):
    """
    添加学校（管理员）
    """
    try:
        # 检查是否已存在
        existing = db.query(School).filter(
            School.province == province,
            School.name == name
        ).first()
        if existing:
            return JSONResponse(
                status_code=400,
                content={
                    "success": False,
                    "code": 400,
                    "message": "学校已存在",
                    "data": {}
                }
            )
        
        # 创建新学校
        school = School(
            province=province,
            name=name,
            has_master=True
        )
        db.add(school)
        db.commit()
        db.refresh(school)
        
        return JSONResponse(
            status_code=201,
            content={
                "success": True,
                "code": 201,
                "message": "添加学校成功",
                "data": {
                    "id": school.id,
                    "province": school.province,
                    "name": school.name,
                    "has_master": school.has_master
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
                "message": f"添加学校失败: {str(e)}",
                "data": {}
            }
        )

@router.put("/schools/{school_id}")
async def update_school(
    school_id: int,
    province: str = Body(None, description="省份"),
    name: str = Body(None, description="学校名称"),
    db: Session = Depends(get_db_common),
    current_admin = Depends(get_current_admin)
):
    """
    更新学校信息（管理员）
    """
    try:
        school = db.query(School).filter(School.id == school_id).first()
        if not school:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "学校不存在",
                    "data": {}
                }
            )
        
        # 更新字段
        if province is not None:
            school.province = province
        if name is not None:
            school.name = name
        
        db.commit()
        db.refresh(school)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "更新学校成功",
                "data": {
                    "id": school.id,
                    "province": school.province,
                    "name": school.name,
                    "has_master": school.has_master
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
                "message": f"更新学校失败: {str(e)}",
                "data": {}
            }
        )

@router.delete("/schools/{school_id}")
async def delete_school(
    school_id: int,
    db: Session = Depends(get_db_common),
    current_admin = Depends(get_current_admin)
):
    """
    删除学校（管理员）
    """
    try:
        school = db.query(School).filter(School.id == school_id).first()
        if not school:
            return JSONResponse(
                status_code=404,
                content={
                    "success": False,
                    "code": 404,
                    "message": "学校不存在",
                    "data": {}
                }
            )
        
        db.delete(school)
        db.commit()
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "code": 200,
                "message": "删除学校成功",
                "data": {}
            }
        )
    except Exception as e:
        db.rollback()
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "code": 500,
                "message": f"删除学校失败: {str(e)}",
                "data": {}
            }
        )
