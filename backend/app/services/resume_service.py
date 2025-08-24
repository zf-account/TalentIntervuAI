import os
import logging
from typing import Dict, Any, Optional, List
from ..utils.document_processor import DocumentProcessor
from ..services.rag_service import RAGService
from ..models.schemas import ResumeAnalysisRequest, ResumeAnalysisResponse

logger = logging.getLogger(__name__)


class ResumeService:
    """简历分析服务"""
    
    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.rag_service = RAGService()
    
    def analyze_resume(self, request: ResumeAnalysisRequest) -> ResumeAnalysisResponse:
        """
        分析简历与岗位的匹配度
        
        Args:
            request: 简历分析请求
            
        Returns:
            ResumeAnalysisResponse: 分析结果
        """
        try:
            # 清理简历文本
            cleaned_resume = self.doc_processor.clean_text(request.resume_text)
            
            # 提取简历章节
            sections = self.doc_processor.extract_resume_sections(cleaned_resume)
            
            # 使用RAG服务分析简历
            analysis_result = self.rag_service.analyze_resume(
                cleaned_resume,
                request.job_description or "",
                request.job_type.value
            )
            
            # 处理分析结果
            if "error" in analysis_result:
                return self._create_error_response(analysis_result["error"])
            
            # 构建响应
            return ResumeAnalysisResponse(
                overall_score=analysis_result.get("overall_score", 0),
                section_scores=analysis_result.get("section_scores", {}),
                strengths=analysis_result.get("strengths", []),
                weaknesses=analysis_result.get("weaknesses", []),
                suggestions=analysis_result.get("suggestions", []),
                keywords_match=analysis_result.get("keywords_match", []),
                missing_keywords=analysis_result.get("missing_keywords", [])
            )
            
        except Exception as e:
            logger.error(f"简历分析失败: {str(e)}")
            return self._create_error_response(str(e))
    
    def _create_error_response(self, error_message: str) -> ResumeAnalysisResponse:
        """创建错误响应"""
        return ResumeAnalysisResponse(
            overall_score=0,
            section_scores={},
            strengths=[],
            weaknesses=[error_message],
            suggestions=["请检查输入数据格式是否正确"],
            keywords_match=[],
            missing_keywords=[]
        )
    
    def process_uploaded_file(self, file_path: str) -> Dict[str, Any]:
        """
        处理上传的文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        try:
            # 检查文件格式
            if not self._is_supported_format(file_path):
                return {
                    "success": False,
                    "error": "不支持的文件格式",
                    "supported_formats": self.doc_processor.supported_formats
                }
            
            # 提取文本
            full_text, chunks = self.doc_processor.extract_text(file_path)
            
            # 清理文本
            cleaned_text = self.doc_processor.clean_text(full_text)
            
            # 提取章节
            sections = self.doc_processor.extract_resume_sections(cleaned_text)
            
            return {
                "success": True,
                "full_text": cleaned_text,
                "text_chunks": chunks,
                "sections": sections,
                "file_size": os.path.getsize(file_path),
                "filename": os.path.basename(file_path)
            }
            
        except Exception as e:
            logger.error(f"文件处理失败: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _is_supported_format(self, file_path: str) -> bool:
        """检查文件格式是否支持"""
        file_ext = os.path.splitext(file_path)[1].lower()
        return file_ext in self.doc_processor.supported_formats
    
    def get_resume_summary(self, resume_text: str) -> Dict[str, Any]:
        """
        获取简历摘要信息
        
        Args:
            resume_text: 简历文本
            
        Returns:
            Dict[str, Any]: 摘要信息
        """
        try:
            sections = self.doc_processor.extract_resume_sections(resume_text)
            
            summary = {
                "total_length": len(resume_text),
                "section_count": len([s for s in sections.values() if s]),
                "sections": {}
            }
            
            for section_name, section_content in sections.items():
                summary["sections"][section_name] = {
                    "count": len(section_content),
                    "content": section_content[:3]  # 只显示前3项
                }
            
            return summary
            
        except Exception as e:
            logger.error(f"获取简历摘要失败: {str(e)}")
            return {"error": str(e)}
    
    def suggest_improvements(self, resume_text: str, target_job: str) -> List[str]:
        """
        建议简历改进
        
        Args:
            resume_text: 简历文本
            target_job: 目标岗位
            
        Returns:
            List[str]: 改进建议列表
        """
        try:
            # 使用RAG服务生成改进建议
            prompt = f"""基于以下简历和目标岗位，提供具体的改进建议：

目标岗位：{target_job}
简历内容：{resume_text}

请提供5-10条具体的、可执行的改进建议。"""

            # 这里可以调用RAG服务或直接使用OpenAI
            # 简化实现，返回通用建议
            suggestions = [
                "确保简历包含目标岗位的关键技能和关键词",
                "量化工作成果，使用具体的数据和指标",
                "突出与目标岗位相关的项目经验",
                "优化简历格式，确保信息层次清晰",
                "添加相关的认证或培训经历"
            ]
            
            return suggestions
            
        except Exception as e:
            logger.error(f"生成改进建议失败: {str(e)}")
            return ["无法生成改进建议，请稍后重试"]
