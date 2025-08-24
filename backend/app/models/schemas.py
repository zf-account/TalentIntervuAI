from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class JobType(str, Enum):
    """岗位类型枚举"""
    SOFTWARE_ENGINEER = "software_engineer"
    DATA_SCIENTIST = "data_scientist"
    PRODUCT_MANAGER = "product_manager"
    UI_UX_DESIGNER = "ui_ux_designer"
    MARKETING = "marketing"
    SALES = "sales"
    OTHER = "other"


class ResumeSection(str, Enum):
    """简历章节枚举"""
    EDUCATION = "education"
    EXPERIENCE = "experience"
    SKILLS = "skills"
    PROJECTS = "projects"
    ACHIEVEMENTS = "achievements"


class ResumeAnalysisRequest(BaseModel):
    """简历分析请求"""
    resume_text: str = Field(..., description="简历文本内容")
    target_job: str = Field(..., description="目标岗位")
    job_description: Optional[str] = Field(None, description="岗位描述")
    job_type: JobType = Field(..., description="岗位类型")


class ResumeAnalysisResponse(BaseModel):
    """简历分析响应"""
    overall_score: float = Field(..., description="总体匹配度评分")
    section_scores: Dict[ResumeSection, float] = Field(..., description="各章节评分")
    strengths: List[str] = Field(..., description="优势分析")
    weaknesses: List[str] = Field(..., description="需要改进的地方")
    suggestions: List[str] = Field(..., description="具体优化建议")
    keywords_match: List[str] = Field(..., description="匹配的关键词")
    missing_keywords: List[str] = Field(..., description="缺失的关键词")


class InterviewQuestion(BaseModel):
    """面试问题"""
    question: str = Field(..., description="问题内容")
    category: str = Field(..., description="问题类别")
    difficulty: str = Field(..., description="难度级别")
    context: Optional[str] = Field(None, description="问题背景")


class InterviewSession(BaseModel):
    """面试会话"""
    session_id: str = Field(..., description="会话ID")
    job_type: JobType = Field(..., description="岗位类型")
    user_background: str = Field(..., description="用户背景")
    questions: List[InterviewQuestion] = Field(..., description="面试问题列表")
    current_question_index: int = Field(0, description="当前问题索引")
    start_time: datetime = Field(default_factory=datetime.now, description="开始时间")


class InterviewAnswer(BaseModel):
    """面试回答"""
    question_id: str = Field(..., description="问题ID")
    answer: str = Field(..., description="用户回答")
    timestamp: datetime = Field(default_factory=datetime.now, description="回答时间")


class InterviewEvaluation(BaseModel):
    """面试评估"""
    session_id: str = Field(..., description="会话ID")
    overall_score: float = Field(..., description="总体评分")
    category_scores: Dict[str, float] = Field(..., description="各维度评分")
    feedback: List[str] = Field(..., description="具体反馈")
    improvement_suggestions: List[str] = Field(..., description="改进建议")
    strengths: List[str] = Field(..., description="表现优势")
    areas_for_improvement: List[str] = Field(..., description="需要改进的方面")


class KnowledgeGapAnalysis(BaseModel):
    """知识漏洞分析"""
    gaps: List[str] = Field(..., description="识别的知识漏洞")
    frequency: Dict[str, int] = Field(..., description="各漏洞出现频率")
    impact_level: Dict[str, str] = Field(..., description="各漏洞影响级别")
    learning_resources: Dict[str, List[str]] = Field(..., description="学习资源推荐")


class LearningPath(BaseModel):
    """学习路径"""
    user_id: str = Field(..., description="用户ID")
    gaps: List[str] = Field(..., description="需要填补的知识漏洞")
    learning_goals: List[str] = Field(..., description="学习目标")
    resources: List[Dict[str, Any]] = Field(..., description="学习资源")
    timeline: Dict[str, str] = Field(..., description="学习时间安排")
    milestones: List[str] = Field(..., description="学习里程碑")


class FileUploadResponse(BaseModel):
    """文件上传响应"""
    filename: str = Field(..., description="文件名")
    file_size: int = Field(..., description="文件大小")
    upload_time: datetime = Field(default_factory=datetime.now, description="上传时间")
    status: str = Field(..., description="上传状态")
    message: str = Field(..., description="状态消息")


class ErrorResponse(BaseModel):
    """错误响应"""
    error: str = Field(..., description="错误类型")
    message: str = Field(..., description="错误消息")
    details: Optional[Dict[str, Any]] = Field(None, description="错误详情")
