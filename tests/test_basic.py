import pytest
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.app.models.schemas import JobType, ResumeSection
from backend.app.utils.document_processor import DocumentProcessor


class TestSchemas:
    """测试数据模型"""
    
    def test_job_type_enum(self):
        """测试岗位类型枚举"""
        assert JobType.SOFTWARE_ENGINEER.value == "software_engineer"
        assert JobType.DATA_SCIENTIST.value == "data_scientist"
        assert JobType.PRODUCT_MANAGER.value == "product_manager"
    
    def test_resume_section_enum(self):
        """测试简历章节枚举"""
        assert ResumeSection.EDUCATION.value == "education"
        assert ResumeSection.EXPERIENCE.value == "experience"
        assert ResumeSection.SKILLS.value == "skills"


class TestDocumentProcessor:
    """测试文档处理器"""
    
    def setup_method(self):
        """测试前准备"""
        self.processor = DocumentProcessor()
    
    def test_supported_formats(self):
        """测试支持的文件格式"""
        expected_formats = ['.pdf', '.docx', '.doc', '.txt']
        assert self.processor.supported_formats == expected_formats
    
    def test_clean_text(self):
        """测试文本清理"""
        dirty_text = "  这是一个  测试文本  \n\n  包含多余空格  "
        cleaned = self.processor.clean_text(dirty_text)
        assert cleaned == "这是一个 测试文本 包含多余空格"
    
    def test_chunk_text(self):
        """测试文本分块"""
        text = "这是一个测试文本。它包含多个句子。每个句子都应该被正确处理。"
        chunks = self.processor.chunk_text(text, chunk_size=20, overlap=5)
        assert len(chunks) > 0
        assert all(len(chunk) <= 20 for chunk in chunks)
    
    def test_extract_resume_sections(self):
        """测试简历章节提取"""
        resume_text = """
        教育背景
        北京大学 计算机科学 本科
        
        工作经验
        腾讯公司 软件工程师 2年
        
        技能
        Python, Java, 机器学习
        
        项目经验
        推荐系统开发
        
        成就
        获得优秀员工奖
        """
        
        sections = self.processor.extract_resume_sections(resume_text)
        
        assert 'education' in sections
        assert 'experience' in sections
        assert 'skills' in sections
        assert 'projects' in sections
        assert 'achievements' in sections


if __name__ == "__main__":
    pytest.main([__file__])
