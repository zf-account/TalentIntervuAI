# TalentIntervuAI - 垂域私人AI面试助手

基于RAG（检索增强生成）+私有知识库构建的垂域私人AI助手，帮助用户优化简历、诊断知识漏洞、进行模拟面试，并提供个性化学习建议。

## 🚀 核心功能

- **简历优化**：针对用户简历内容给出可执行的优化建议
- **知识储备诊断**：发现用户在面试中容易出现的知识盲区
- **模拟面试**：提供可交互的面试模拟对话
- **个性化学习路径**：根据漏洞生成提升计划
- **私有化数据管理**：确保用户数据仅用于个人，支持本地部署

## 🏗️ 技术架构

- **后端**：Python + FastAPI
- **前端**：Streamlit Web应用
- **向量数据库**：FAISS/Milvus/neo4j
- **LLM调用**：Zhipu/OpenAI API
- **RAG框架**：LangChain
- **文档处理**：PyPDF2, python-docx

## 📁 项目结构

```
TalentIntervuAI/
├── backend/                 # 后端API服务
│   ├── app/
│   │   ├── api/            # API路由
│   │   ├── core/           # 核心配置
│   │   ├── models/         # 数据模型
│   │   ├── services/       # 业务逻辑
│   │   └── utils/          # 工具函数
│   ├── requirements.txt     # 依赖包
│   └── main.py             # 启动文件
├── frontend/                # 前端Streamlit应用
│   ├── pages/              # 页面模块
│   ├── components/          # 组件
│   └── main.py             # 主应用
├── data/                    # 数据存储
│   ├── uploads/            # 上传文件
│   ├── vector_db/          # 向量数据库
│   └── knowledge_base/     # 知识库
├── config/                  # 配置文件
├── tests/                   # 测试文件
└── docs/                    # 文档
```

## 🛠️ 安装与运行

### 1. 环境要求
- Python 3.8+
- 8GB+ RAM
- Zhipu/OpenAI API Key

### 2. 安装依赖
```bash
# 安装后端依赖
cd backend
pip install -r requirements.txt

# 安装前端依赖
cd ../frontend
pip install -r requirements.txt
```

### 3. 配置环境变量
```bash
# 复制配置文件
cp config/.env.example config/.env

# 编辑配置文件，添加OpenAI API Key
OPENAI_API_KEY=your_api_key_here
```

### 4. 启动服务
```bash
# 启动后端API服务
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 启动前端应用
cd ../frontend
streamlit run main.py
```

## 📖 使用说明

1. **简历上传**：上传PDF或Word格式的简历
2. **岗位匹配**：输入目标岗位JD，分析匹配度
3. **简历优化**：获取针对性的优化建议
4. **模拟面试**：选择岗位类型，开始模拟面试
5. **知识诊断**：上传面试记录，分析知识漏洞
6. **学习建议**：获取个性化学习路径

## 🔒 隐私保护

- 所有数据本地存储，不上传到第三方服务器
- 支持本地向量数据库部署
- 用户数据加密存储
- 可选择私有云部署

## 📝 后续开发计划

- **MVP版本**（已完成）：基础简历分析、岗位匹配度建议和知识查缺补漏
- **第二阶段**（8-9月）：面试记录分析和评估报告
- **第三阶段**（9-10月）：高级功能和语音交互

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License
