import logging
import uuid
from typing import Dict, Any, List
from datetime import datetime
from ..services.rag_service import RAGService
from ..models.schemas import InterviewSession, InterviewQuestion, JobType

logger = logging.getLogger(__name__)


class InterviewService:
    """面试服务，处理模拟面试和评估"""
    
    def __init__(self):
        self.rag_service = RAGService()
        self.active_sessions = {}
    
    def create_interview_session(self, job_type: JobType, user_background: str) -> InterviewSession:
        """创建新的面试会话"""
        try:
            session_id = str(uuid.uuid4())
            
            # 生成面试问题
            questions = self.rag_service.generate_interview_questions(
                job_type.value, user_background, num_questions=5
            )
            
            # 构建面试问题对象
            interview_questions = []
            for i, q in enumerate(questions):
                question = InterviewQuestion(
                    question=q.get('question', f'问题{i+1}'),
                    category=q.get('category', 'general'),
                    difficulty=q.get('difficulty', 'medium'),
                    context=q.get('context', '')
                )
                interview_questions.append(question)
            
            # 创建面试会话
            session = InterviewSession(
                session_id=session_id,
                job_type=job_type,
                user_background=user_background,
                questions=interview_questions,
                current_question_index=0,
                start_time=datetime.now()
            )
            
            # 存储会话
            self.active_sessions[session_id] = {
                'session': session,
                'answers': [],
                'current_question': 0
            }
            
            return session
            
        except Exception as e:
            logger.error(f"创建面试会话失败: {str(e)}")
            raise
    
    def get_current_question(self, session_id: str):
        """获取当前问题"""
        try:
            if session_id not in self.active_sessions:
                return None
            
            session_data = self.active_sessions[session_id]
            current_index = session_data['current_question']
            session = session_data['session']
            
            if current_index < len(session.questions):
                return session.questions[current_index]
            else:
                return None
                
        except Exception as e:
            logger.error(f"获取当前问题失败: {str(e)}")
            return None
    
    def submit_answer(self, session_id: str, answer_text: str) -> Dict[str, Any]:
        """提交面试回答"""
        try:
            if session_id not in self.active_sessions:
                return {"success": False, "error": "会话不存在"}
            
            session_data = self.active_sessions[session_id]
            current_index = session_data['current_question']
            session = session_data['session']
            
            if current_index >= len(session.questions):
                return {"success": False, "error": "面试已完成"}
            
            # 存储回答
            session_data['answers'].append({
                'question_id': str(current_index),
                'answer': answer_text,
                'timestamp': datetime.now()
            })
            
            # 移动到下一个问题
            session_data['current_question'] += 1
            
            # 检查是否完成
            is_completed = session_data['current_question'] >= len(session.questions)
            
            return {
                "success": True,
                "is_completed": is_completed,
                "next_question": self.get_current_question(session_id) if not is_completed else None
            }
            
        except Exception as e:
            logger.error(f"提交回答失败: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def evaluate_interview(self, session_id: str) -> Dict[str, Any]:
        """评估面试表现"""
        try:
            if session_id not in self.active_sessions:
                raise ValueError("会话不存在")
            
            session_data = self.active_sessions[session_id]
            session = session_data['session']
            answers = session_data['answers']
            
            if not answers:
                raise ValueError("没有回答记录")
            
            # 评估每个回答
            evaluations = []
            total_score = 0
            
            for answer in answers:
                question_index = int(answer['question_id'])
                if question_index < len(session.questions):
                    question = session.questions[question_index]
                    
                    # 使用RAG服务评估回答
                    evaluation = self.rag_service.evaluate_interview_answer(
                        question.question,
                        answer['answer'],
                        session.job_type.value
                    )
                    
                    evaluations.append(evaluation)
                    
                    # 累加分数
                    if "overall_score" in evaluation:
                        total_score += evaluation["overall_score"]
            
            # 计算平均分
            avg_score = total_score / len(answers) if answers else 0
            
            return {
                "session_id": session_id,
                "overall_score": avg_score,
                "evaluations": evaluations,
                "total_questions": len(session.questions),
                "answered_questions": len(answers)
            }
            
        except Exception as e:
            logger.error(f"评估面试失败: {str(e)}")
            return {"error": str(e)}
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """获取会话摘要"""
        try:
            if session_id not in self.active_sessions:
                return {"error": "会话不存在"}
            
            session_data = self.active_sessions[session_id]
            session = session_data['session']
            answers = session_data['answers']
            
            return {
                "session_id": session_id,
                "job_type": session.job_type.value,
                "total_questions": len(session.questions),
                "answered_questions": len(answers),
                "current_question": session_data['current_question'],
                "start_time": session.start_time.isoformat(),
                "is_completed": session_data['current_question'] >= len(session.questions)
            }
            
        except Exception as e:
            logger.error(f"获取会话摘要失败: {str(e)}")
            return {"error": str(e)}
