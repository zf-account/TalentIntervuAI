from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import os
import aiofiles
from ..services.resume_service import ResumeService
from ..models.schemas import ResumeAnalysisRequest, ResumeAnalysisResponse
from ..core.config import settings

router = APIRouter(prefix="/resume", tags=["简历分析"])
resume_service = ResumeService()


@router.post("/analyze", response_model=ResumeAnalysisResponse)
async def analyze_resume(request: ResumeAnalysisRequest):
    """
    分析简历与岗位的匹配度
    """
    try:
        result = resume_service.analyze_resume(request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):
    """
    上传简历文件
    """
    try:
        # 检查文件格式
        allowed_extensions = ['.pdf', '.docx', '.doc', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"不支持的文件格式。支持格式: {', '.join(allowed_extensions)}"
            )
        
        # 保存文件
        upload_path = os.path.join(settings.uploads_path, file.filename)
        os.makedirs(settings.uploads_path, exist_ok=True)
        
        async with aiofiles.open(upload_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # 处理文件
        result = resume_service.process_uploaded_file(upload_path)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "filename": file.filename,
            "file_size": result["file_size"],
            "sections": result["sections"],
            "message": "文件上传成功"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")


@router.get("/summary/{filename}")
async def get_resume_summary(filename: str):
    """
    获取简历摘要信息
    """
    try:
        file_path = os.path.join(settings.uploads_path, filename)
        
        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail="文件不存在")
        
        # 读取文件内容
        async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
            content = await f.read()
        
        # 获取摘要
        summary = resume_service.get_resume_summary(content)
        
        if "error" in summary:
            raise HTTPException(status_code=400, detail=summary["error"])
        
        return summary
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取摘要失败: {str(e)}")


@router.post("/suggestions")
async def get_improvement_suggestions(resume_text: str, target_job: str):
    """
    获取简历改进建议
    """
    try:
        suggestions = resume_service.suggest_improvements(resume_text, target_job)
        return {
            "suggestions": suggestions,
            "count": len(suggestions)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取建议失败: {str(e)}")


@router.get("/supported-formats")
async def get_supported_formats():
    """
    获取支持的文件格式
    """
    return {
        "supported_formats": resume_service.doc_processor.supported_formats,
        "description": "支持PDF、Word文档和文本文件"
    }
