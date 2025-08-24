from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..services.interview_service import InterviewService
from ..models.schemas import JobType

router = APIRouter(prefix="/interview", tags=["模拟面试"])
interview_service = InterviewService()


@router.post("/create-session")
async def create_interview_session(job_type: JobType, user_background: str):
    """
    创建新的面试会话
    """
    try:
        session = interview_service.create_interview_session(job_type, user_background)
        return {
            "session_id": session.session_id,
            "job_type": session.job_type.value,
            "total_questions": len(session.questions),
            "start_time": session.start_time.isoformat(),
            "message": "面试会话创建成功"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建面试会话失败: {str(e)}")


@router.get("/session/{session_id}/current-question")
async def get_current_question(session_id: str):
    """
    获取当前面试问题
    """
    try:
        question = interview_service.get_current_question(session_id)
        
        if not question:
            raise HTTPException(status_code=404, detail="问题不存在或面试已完成")
        
        return {
            "question": question.question,
            "category": question.category,
            "difficulty": question.difficulty,
            "context": question.context
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问题失败: {str(e)}")


@router.post("/session/{session_id}/submit-answer")
async def submit_answer(session_id: str, answer: str):
    """
    提交面试回答
    """
    try:
        result = interview_service.submit_answer(session_id, answer)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"提交回答失败: {str(e)}")


@router.post("/session/{session_id}/evaluate")
async def evaluate_interview(session_id: str):
    """
    评估面试表现
    """
    try:
        evaluation = interview_service.evaluate_interview(session_id)
        
        if "error" in evaluation:
            raise HTTPException(status_code=400, detail=evaluation["error"])
        
        return evaluation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"评估面试失败: {str(e)}")


@router.get("/session/{session_id}/summary")
async def get_session_summary(session_id: str):
    """
    获取面试会话摘要
    """
    try:
        summary = interview_service.get_session_summary(session_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        return summary
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取会话摘要失败: {str(e)}")


@router.get("/job-types")
async def get_job_types():
    """
    获取支持的岗位类型
    """
    return {
        "job_types": [
            {"value": job_type.value, "label": job_type.value.replace("_", " ").title()}
            for job_type in JobType
        ]
    }


@router.get("/session/{session_id}/questions")
async def get_session_questions(session_id: str):
    """
    获取面试会话的所有问题
    """
    try:
        summary = interview_service.get_session_summary(session_id)
        
        if "error" in summary:
            raise HTTPException(status_code=404, detail=summary["error"])
        
        # 获取会话数据
        session_data = interview_service.active_sessions.get(session_id)
        if not session_data:
            raise HTTPException(status_code=404, detail="会话不存在")
        
        session = session_data['session']
        questions = []
        
        for i, question in enumerate(session.questions):
            questions.append({
                "index": i,
                "question": question.question,
                "category": question.category,
                "difficulty": question.difficulty,
                "context": question.context
            })
        
        return {
            "session_id": session_id,
            "total_questions": len(questions),
            "questions": questions
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取问题列表失败: {str(e)}")
