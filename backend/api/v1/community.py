#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双赛道情报通 - 社区API
"""

from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile, File, Body
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from datetime import datetime
import os
import shutil

from core.database import get_db_common
from models.users import User, UserLoginRecord
from models.community import (
    Group, GroupMember, GroupPost, GroupPostComment,
    Question, Answer, AnswerComment, Like, Report, GroupMessage
)
from schemas.community import (
    GroupCreate, GroupUpdate, GroupResponse, GroupMemberResponse,
    QuestionCreate, QuestionUpdate, QuestionResponse, AnswerCreate, 
    AnswerUpdate, AnswerResponse, CommentCreate, CommentResponse,
    LikeResponse
)
from core.security import get_current_user

router = APIRouter(prefix="/community", tags=["community"])

# 学习小组相关接口

@router.get("/groups", response_model=List[GroupResponse])
async def get_groups(
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    db: Session = Depends(get_db_common)
):
    """获取小组列表"""
    from datetime import date
    
    groups = db.query(Group).filter(Group.status == 1).order_by(desc(Group.member_count)).offset(skip).limit(limit).all()
    
    # 为每个小组添加今日活跃用户数
    result = []
    today = date.today()
    
    for group in groups:
        # 获取小组成员的用户ID列表
        member_ids = [member.user_id for member in db.query(GroupMember).filter(
            GroupMember.group_id == group.id,
            GroupMember.status == 1
        ).all()]
        
        # 统计今日登录过的成员数量
        active_today = db.query(UserLoginRecord).filter(
            UserLoginRecord.user_id.in_(member_ids),
            UserLoginRecord.login_date == today
        ).count() if member_ids else 0
        
        # 构建返回数据
        group_dict = {
            "id": group.id,
            "name": group.name,
            "description": group.description,
            "avatar": group.avatar,
            "cover": group.cover,
            "creator_id": group.creator_id,
            "status": group.status,
            "member_count": group.member_count,
            "join_type": group.join_type,
            "tags": group.tags,
            "created_at": group.created_at,
            "updated_at": group.updated_at,
            "active_today": active_today
        }
        result.append(group_dict)
    
    return result

@router.get("/groups/{id}", response_model=GroupResponse)
async def get_group(
    id: int = Path(..., description="小组ID"),
    db: Session = Depends(get_db_common)
):
    """获取小组详情"""
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    return group

@router.post("/groups", response_model=GroupResponse)
async def create_group(
    group: GroupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """创建小组"""
    # 检查小组名称是否已存在
    existing_group = db.query(Group).filter(Group.name == group.name).first()
    if existing_group:
        raise HTTPException(status_code=400, detail="小组名称已存在")
    
    # 创建小组
    db_group = Group(
        name=group.name,
        description=group.description,
        avatar=group.avatar,
        cover=group.cover,
        creator_id=current_user.id,
        join_type=group.join_type,
        tags=group.tags
    )
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    
    # 添加创建者为小组成员
    member = GroupMember(
        group_id=db_group.id,
        user_id=current_user.id,
        role=2,  # 创建者
        status=1,
        join_time=datetime.now()
    )
    db.add(member)
    db_group.member_count = 1
    db.commit()
    
    return db_group

@router.put("/groups/{id}", response_model=GroupResponse)
async def update_group(
    group: GroupUpdate,
    id: int = Path(..., description="小组ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """更新小组信息"""
    db_group = db.query(Group).filter(Group.id == id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 检查权限（只有创建者或管理员可以更新）
    member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == 1,
        GroupMember.role.in_([1, 2])  # 管理员或创建者
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="无权限更新小组信息")
    
    # 更新小组信息
    update_data = group.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_group, key, value)
    
    db.commit()
    db.refresh(db_group)
    return db_group

@router.delete("/groups/{id}")
async def delete_group(
    id: int = Path(..., description="小组ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """删除小组"""
    db_group = db.query(Group).filter(Group.id == id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 检查权限（只有创建者可以删除）
    member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == 1,
        GroupMember.role == 2  # 只有创建者
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="无权限删除小组")
    
    # 软删除小组
    db_group.status = 0
    db.commit()
    
    return {"message": "小组删除成功"}

@router.post("/groups/{id}/join")
async def join_group(
    id: int = Path(..., description="小组ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """加入小组"""
    # 检查小组是否存在
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 检查是否已经是成员
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id
    ).first()
    if existing_member:
        if existing_member.status == 1:
            raise HTTPException(status_code=400, detail="已经是小组成员")
        elif existing_member.status == 0:
            raise HTTPException(status_code=400, detail="申请已提交，等待审核")
        elif existing_member.status == 2:
            # 如果之前被拒绝，允许重新申请
            existing_member.status = 1 if group.join_type == 1 else 0
            existing_member.join_time = datetime.now()
            if group.join_type == 1:
                group.member_count += 1
            db.commit()
            return {"message": "加入小组成功" if group.join_type == 1 else "申请已提交，等待审核"}
    
    # 创建成员记录
    member = GroupMember(
        group_id=id,
        user_id=current_user.id,
        role=0,  # 普通成员
        status=1 if group.join_type == 1 else 0,  # 自由加入直接通过，否则待审核
        join_time=datetime.now()
    )
    db.add(member)
    
    # 如果是自由加入，更新成员数量
    if group.join_type == 1:
        group.member_count += 1
    
    db.commit()
    
    return {"message": "加入小组成功" if group.join_type == 1 else "申请已提交，等待审核"}

@router.post("/groups/{id}/leave")
async def leave_group(
    id: int = Path(..., description="小组ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """退出小组"""
    # 检查是否是成员
    member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == 1
    ).first()
    if not member:
        raise HTTPException(status_code=400, detail="不是小组成员")
    
    # 检查是否是创建者（创建者不能退出，只能删除小组）
    if member.role == 2:
        raise HTTPException(status_code=400, detail="创建者不能退出小组")
    
    # 删除成员记录
    db.delete(member)
    
    # 更新成员数量
    group = db.query(Group).filter(Group.id == id).first()
    if group:
        group.member_count = max(0, group.member_count - 1)
    
    db.commit()
    
    return {"message": "退出小组成功"}

@router.get("/groups/{id}/members", response_model=List[GroupMemberResponse])
async def get_group_members(
    id: int = Path(..., description="小组ID"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    db: Session = Depends(get_db_common)
):
    """获取小组成员列表"""
    # 检查小组是否存在
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 获取成员列表
    members = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.status == 1
    ).offset(skip).limit(limit).all()
    
    return members

@router.get("/groups/{id}/posts")
async def get_group_posts(
    id: int = Path(..., description="小组ID"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    db: Session = Depends(get_db_common)
):
    """获取小组帖子列表"""
    # 检查小组是否存在
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 获取帖子列表
    posts = db.query(GroupPost).filter(
        GroupPost.group_id == id,
        GroupPost.status == 1
    ).order_by(desc(GroupPost.created_at)).offset(skip).limit(limit).all()
    
    # 构建返回数据
    result = []
    for post in posts:
        author = db.query(User).filter(User.id == post.user_id).first()
        result.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "author_id": post.user_id,
            "author_name": author.username if author else "未知用户",
            "author_avatar": author.avatar if author else None,
            "like_count": post.like_count,
            "comment_count": post.comment_count,
            "created_at": post.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return result

@router.post("/groups/{id}/posts")
async def create_group_post(
    id: int = Path(..., description="小组ID"),
    title: str = Query(..., description="帖子标题"),
    content: str = Query(..., description="帖子内容"),
    image_urls: Optional[str] = Query(None, description="图片URL，逗号分隔"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """创建小组帖子"""
    # 检查小组是否存在
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 检查用户是否是小组成员
    member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == 1
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="您不是小组成员，无法发帖")
    
    # 创建帖子
    db_post = GroupPost(
        group_id=id,
        user_id=current_user.id,
        title=title,
        content=content,
        image_urls=image_urls
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    return {"message": "帖子创建成功", "post_id": db_post.id}

# 问答板块相关接口

@router.get("/questions", response_model=List[QuestionResponse])
async def get_questions(
    category: Optional[str] = Query(None, description="问题分类"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    db: Session = Depends(get_db_common)
):
    """获取问题列表"""
    query = db.query(Question).filter(Question.status == 1)
    
    if category:
        query = query.filter(Question.category == category)
    
    questions = query.order_by(desc(Question.created_at)).offset(skip).limit(limit).all()
    return questions

@router.get("/questions/{id}", response_model=QuestionResponse)
async def get_question(
    id: int = Path(..., description="问题ID"),
    db: Session = Depends(get_db_common)
):
    """获取问题详情"""
    question = db.query(Question).filter(Question.id == id, Question.status == 1).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    # 增加浏览量
    question.view_count += 1
    db.commit()
    
    return question

@router.post("/questions", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """创建问题"""
    db_question = Question(
        user_id=current_user.id,
        title=question.title,
        content=question.content,
        image_urls=question.image_urls,
        category=question.category,
        tags=question.tags
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.put("/questions/{id}", response_model=QuestionResponse)
async def update_question(
    question: QuestionUpdate,
    id: int = Path(..., description="问题ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """更新问题"""
    db_question = db.query(Question).filter(Question.id == id, Question.status == 1).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    # 检查权限（只有问题作者可以更新）
    if db_question.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限更新问题")
    
    # 更新问题信息
    update_data = question.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/questions/{id}")
async def delete_question(
    id: int = Path(..., description="问题ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """删除问题"""
    db_question = db.query(Question).filter(Question.id == id, Question.status == 1).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    # 检查权限（只有问题作者可以删除）
    if db_question.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除问题")
    
    # 软删除问题
    db_question.status = 0
    db.commit()
    
    return {"message": "问题删除成功"}

@router.post("/questions/{id}/answers", response_model=AnswerResponse)
async def create_answer(
    answer: AnswerCreate,
    id: int = Path(..., description="问题ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """回答问题"""
    # 检查问题是否存在
    question = db.query(Question).filter(Question.id == id, Question.status == 1).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    # 创建回答
    db_answer = Answer(
        question_id=id,
        user_id=current_user.id,
        content=answer.content,
        image_urls=answer.image_urls
    )
    db.add(db_answer)
    
    # 更新问题的回答数
    question.answer_count += 1
    
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.get("/questions/{id}/answers", response_model=List[AnswerResponse])
async def get_answers(
    id: int = Path(..., description="问题ID"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(20, ge=1, le=100, description="返回的记录数"),
    db: Session = Depends(get_db_common)
):
    """获取问题的回答列表"""
    # 检查问题是否存在
    question = db.query(Question).filter(Question.id == id, Question.status == 1).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    # 获取回答列表，先显示被采纳的，然后按点赞数排序
    answers = db.query(Answer).filter(
        Answer.question_id == id,
        Answer.status == 1
    ).order_by(
        desc(Answer.is_accepted),
        desc(Answer.like_count),
        desc(Answer.created_at)
    ).offset(skip).limit(limit).all()
    
    return answers

@router.put("/answers/{id}", response_model=AnswerResponse)
async def update_answer(
    answer: AnswerUpdate,
    id: int = Path(..., description="回答ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """更新回答"""
    db_answer = db.query(Answer).filter(Answer.id == id, Answer.status == 1).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="回答不存在")
    
    # 检查权限（只有回答作者可以更新）
    if db_answer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限更新回答")
    
    # 更新回答信息
    update_data = answer.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_answer, key, value)
    
    db.commit()
    db.refresh(db_answer)
    return db_answer

@router.delete("/answers/{id}")
async def delete_answer(
    id: int = Path(..., description="回答ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """删除回答"""
    db_answer = db.query(Answer).filter(Answer.id == id, Answer.status == 1).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="回答不存在")
    
    # 检查权限（只有回答作者可以删除）
    if db_answer.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限删除回答")
    
    # 软删除回答
    db_answer.status = 0
    
    # 更新问题的回答数
    question = db.query(Question).filter(Question.id == db_answer.question_id).first()
    if question:
        question.answer_count = max(0, question.answer_count - 1)
    
    db.commit()
    
    return {"message": "回答删除成功"}

@router.post("/answers/{id}/accept")
async def accept_answer(
    id: int = Path(..., description="回答ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """采纳回答"""
    # 检查回答是否存在
    db_answer = db.query(Answer).filter(Answer.id == id, Answer.status == 1).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="回答不存在")
    
    # 检查问题是否存在
    question = db.query(Question).filter(Question.id == db_answer.question_id, Question.status == 1).first()
    if not question:
        raise HTTPException(status_code=404, detail="问题不存在")
    
    # 检查权限（只有问题作者可以采纳）
    if question.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="无权限采纳回答")
    
    # 取消其他回答的采纳状态
    db.query(Answer).filter(
        Answer.question_id == question.id,
        Answer.id != id,
        Answer.is_accepted == True
    ).update({"is_accepted": False})
    
    # 设置当前回答为采纳状态
    db_answer.is_accepted = True
    
    # 更新问题状态为已解决
    question.status = 2
    
    db.commit()
    
    return {"message": "回答采纳成功"}

# 点赞相关接口

@router.post("/like")
async def add_like(
    target_type: int = Query(..., description="目标类型: 1-问题, 2-回答, 3-评论, 4-帖子"),
    target_id: int = Query(..., description="目标ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """点赞"""
    # 检查是否已经点赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.target_type == target_type,
        Like.target_id == target_id
    ).first()
    if existing_like:
        raise HTTPException(status_code=400, detail="已经点过赞")
    
    # 检查目标是否存在
    if target_type == 1:
        target = db.query(Question).filter(Question.id == target_id, Question.status == 1).first()
        if target:
            target.like_count += 1
    elif target_type == 2:
        target = db.query(Answer).filter(Answer.id == target_id, Answer.status == 1).first()
        if target:
            target.like_count += 1
    elif target_type == 3:
        # 这里需要检查是回答评论还是帖子评论
        target = db.query(AnswerComment).filter(AnswerComment.id == target_id, AnswerComment.status == 1).first()
        if not target:
            target = db.query(GroupPostComment).filter(GroupPostComment.id == target_id, GroupPostComment.status == 1).first()
        if target:
            target.like_count += 1
    elif target_type == 4:
        target = db.query(GroupPost).filter(GroupPost.id == target_id, GroupPost.status == 1).first()
        if target:
            target.like_count += 1
    else:
        raise HTTPException(status_code=400, detail="无效的目标类型")
    
    if not target:
        raise HTTPException(status_code=404, detail="目标不存在")
    
    # 创建点赞记录
    db_like = Like(
        user_id=current_user.id,
        target_type=target_type,
        target_id=target_id
    )
    db.add(db_like)
    db.commit()
    
    return {"message": "点赞成功"}

@router.delete("/like")
async def remove_like(
    target_type: int = Query(..., description="目标类型: 1-问题, 2-回答, 3-评论, 4-帖子"),
    target_id: int = Query(..., description="目标ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """取消点赞"""
    # 检查是否已经点赞
    existing_like = db.query(Like).filter(
        Like.user_id == current_user.id,
        Like.target_type == target_type,
        Like.target_id == target_id
    ).first()
    if not existing_like:
        raise HTTPException(status_code=400, detail="未点过赞")
    
    # 减少目标的点赞数
    if target_type == 1:
        target = db.query(Question).filter(Question.id == target_id).first()
        if target:
            target.like_count = max(0, target.like_count - 1)
    elif target_type == 2:
        target = db.query(Answer).filter(Answer.id == target_id).first()
        if target:
            target.like_count = max(0, target.like_count - 1)
    elif target_type == 3:
        # 这里需要检查是回答评论还是帖子评论
        target = db.query(AnswerComment).filter(AnswerComment.id == target_id).first()
        if not target:
            target = db.query(GroupPostComment).filter(GroupPostComment.id == target_id).first()
        if target:
            target.like_count = max(0, target.like_count - 1)
    elif target_type == 4:
        target = db.query(GroupPost).filter(GroupPost.id == target_id).first()
        if target:
            target.like_count = max(0, target.like_count - 1)
    
    # 删除点赞记录
    db.delete(existing_like)
    db.commit()
    
    return {"message": "取消点赞成功"}

# 文件上传接口

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    """上传文件"""
    # 检查文件类型
    allowed_extensions = {"jpg", "jpeg", "png", "gif", "webp"}
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="只支持图片文件")
    
    # 生成文件名
    import uuid
    file_name = f"{uuid.uuid4()}.{file_extension}"
    
    # 确保上传目录存在
    upload_dir = "uploads/community"
    os.makedirs(upload_dir, exist_ok=True)
    
    # 保存文件
    file_path = os.path.join(upload_dir, file_name)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 返回文件URL
    file_url = f"/uploads/community/{file_name}"
    return {"url": file_url}


# 群聊消息相关接口

@router.get("/groups/{id}/messages")
async def get_group_messages(
    id: int = Path(..., description="小组ID"),
    skip: int = Query(0, ge=0, description="跳过的记录数"),
    limit: int = Query(100, ge=1, le=200, description="返回的记录数"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """获取群聊消息列表"""
    # 检查小组是否存在
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 检查用户是否是小组成员
    member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == 1
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="您不是小组成员，无法查看消息")
    
    # 获取消息列表
    messages = db.query(GroupMessage).filter(
        GroupMessage.group_id == id,
        GroupMessage.status == 1
    ).order_by(GroupMessage.created_at).offset(skip).limit(limit).all()
    
    # 构建返回数据
    result = []
    for msg in messages:
        sender = db.query(User).filter(User.id == msg.user_id).first()
        result.append({
            "id": msg.id,
            "user_id": msg.user_id,
            "sender_name": sender.username if sender else "未知用户",
            "sender_avatar": sender.avatar if sender else None,
            "message_type": msg.message_type,
            "content": msg.content,
            "image_url": msg.image_url,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return result


@router.post("/groups/{id}/messages")
async def send_group_message(
    id: int = Path(..., description="小组ID"),
    message_type: int = Body(1, description="消息类型: 1-文字, 2-图片"),
    content: Optional[str] = Body(None, description="消息内容"),
    image_url: Optional[str] = Body(None, description="图片URL"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_common)
):
    """发送群聊消息"""
    # 检查小组是否存在
    group = db.query(Group).filter(Group.id == id, Group.status == 1).first()
    if not group:
        raise HTTPException(status_code=404, detail="小组不存在")
    
    # 检查用户是否是小组成员
    member = db.query(GroupMember).filter(
        GroupMember.group_id == id,
        GroupMember.user_id == current_user.id,
        GroupMember.status == 1
    ).first()
    if not member:
        raise HTTPException(status_code=403, detail="您不是小组成员，无法发送消息")
    
    # 验证消息内容
    if message_type == 1 and not content:
        raise HTTPException(status_code=400, detail="文字消息不能为空")
    if message_type == 2 and not image_url:
        raise HTTPException(status_code=400, detail="图片消息需要提供图片URL")
    
    # 创建消息
    db_message = GroupMessage(
        group_id=id,
        user_id=current_user.id,
        message_type=message_type,
        content=content,
        image_url=image_url
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    
    return {"message": "消息发送成功", "message_id": db_message.id}
