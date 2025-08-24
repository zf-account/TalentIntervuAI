import os
import json
import logging
from typing import List, Dict, Any
import openai
from ..core.config import settings

logger = logging.getLogger(__name__)


class RAGService:
    """RAG服务，实现检索增强生成功能"""
    
    def __init__(self):
        openai.api_key = settings.openai_api_key
    
    def analyze_resume(self, resume_text: str, job_description: str, 
                      job_type: str) -> Dict[str, Any]:
        """分析简历与岗位的匹配度"""
        try:
            prompt = f"""分析简历与岗位匹配度：

岗位类型：{job_type}
岗位描述：{job_description}
简历内容：{resume_text}

请分析：
1. 总体匹配度评分（0-100分）
2. 各章节评分
3. 优势分析
4. 改进建议
5. 匹配和缺失的关键词

以JSON格式返回。"""
            
            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "你是简历分析专家"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except:
                return {"error": "解析失败"}
                
        except Exception as e:
            logger.error(f"简历分析失败: {str(e)}")
            return {"error": str(e)}
    
    def generate_interview_questions(self, job_type: str, user_background: str, 
                                   num_questions: int = 5) -> List[Dict[str, str]]:
        """生成面试问题"""
        try:
            prompt = f"""生成{num_questions}个面试问题：

岗位类型：{job_type}
用户背景：{user_background}

请生成相关问题，以JSON格式返回。"""

            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "你是专业面试官"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                return result if isinstance(result, list) else []
            except:
                return []
                
        except Exception as e:
            logger.error(f"生成面试问题失败: {str(e)}")
            return []
    
    def evaluate_interview_answer(self, question: str, answer: str, 
                                job_type: str) -> Dict[str, Any]:
        """评估面试回答"""
        try:
            prompt = f"""评估面试回答：

岗位类型：{job_type}
问题：{question}
回答：{answer}

请评估并返回JSON格式结果。"""

            response = openai.ChatCompletion.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": "你是面试评估专家"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            
            try:
                return json.loads(response.choices[0].message.content)
            except:
                return {"error": "解析失败"}
                
        except Exception as e:
            logger.error(f"面试评估失败: {str(e)}")
            return {"error": str(e)}
