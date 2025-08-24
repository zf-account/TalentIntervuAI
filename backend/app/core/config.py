import os
from typing import Optional
from pydantic import BaseSettings


class Settings(BaseSettings):
    """应用配置类"""
    
    # 应用基本信息
    app_name: str = "TalentIntervuAI"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # OpenAI配置
    openai_api_key: str
    openai_model: str = "gpt-3.5-turbo"
    openai_embedding_model: str = "text-embedding-ada-002"
    
    # 数据库路径配置
    vector_db_path: str = "./data/vector_db"
    knowledge_base_path: str = "./data/knowledge_base"
    uploads_path: str = "./data/uploads"
    
    # 服务配置
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    frontend_port: int = 8501
    
    # RAG配置
    chunk_size: int = 512
    chunk_overlap: int = 50
    top_k_retrieval: int = 5
    
    # 安全配置
    secret_key: str = "your-secret-key-change-in-production"
    encryption_key: str = "your-encryption-key-change-in-production"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# 创建全局配置实例
settings = Settings()

# 确保必要的目录存在
def ensure_directories():
    """确保必要的目录存在"""
    directories = [
        settings.vector_db_path,
        settings.knowledge_base_path,
        settings.uploads_path
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# 初始化时创建目录
ensure_directories()
