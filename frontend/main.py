import streamlit as st
import requests
from datetime import datetime

# 页面配置
st.set_page_config(
    page_title="TalentIntervuAI - AI面试助手",
    page_icon="🚀",
    layout="wide"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header { font-size: 3rem; font-weight: bold; color: #1f77b4; text-align: center; }
    .feature-card { background-color: #f8f9fa; padding: 1.5rem; border-radius: 10px; margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">TalentIntervuAI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem;">垂域私人AI面试助手</p>', unsafe_allow_html=True)
    
    # 功能选择
    page = st.sidebar.selectbox(
        "选择功能",
        ["🏠 首页", "📄 简历分析", "🎯 模拟面试"]
    )
    
    if page == "🏠 首页":
        show_home()
    elif page == "📄 简历分析":
        show_resume_analysis()
    elif page == "🎯 模拟面试":
        show_interview()

def show_home():
    st.markdown("## 🚀 核心功能")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📄 简历优化</h3>
            <p>AI分析简历，提供优化建议</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 模拟面试</h3>
            <p>定制化面试问题，实时互动</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 智能评估</h3>
            <p>多维度评估，生成学习路径</p>
        </div>
        """, unsafe_allow_html=True)

def show_resume_analysis():
    st.title("📄 简历分析")
    
    uploaded_file = st.file_uploader("选择简历文件", type=['pdf', 'docx', 'doc', 'txt'])
    
    if uploaded_file:
        st.info(f"已上传: {uploaded_file.name}")
        
        target_job = st.text_input("目标岗位")
        job_type = st.selectbox("岗位类型", ["software_engineer", "data_scientist", "product_manager"])
        
        if st.button("开始分析"):
            # 模拟分析结果
            st.success("分析完成！")
            st.json({
                "overall_score": 78,
                "strengths": ["技术背景优秀", "项目经验丰富"],
                "suggestions": ["增加具体数据", "优化项目描述"]
            })

def show_interview():
    st.title("🎯 模拟面试")
    
    job_type = st.selectbox("岗位类型", ["software_engineer", "data_scientist", "product_manager"])
    
    if st.button("开始面试"):
        st.info("面试开始...")
        
        questions = [
            "请介绍您的技术背景？",
            "描述一个技术难题的解决过程？",
            "您如何看待团队协作？"
        ]
        
        for i, question in enumerate(questions):
            st.markdown(f"**问题 {i+1}:** {question}")
            answer = st.text_area(f"回答 {i+1}", key=f"answer_{i}")
        
        if st.button("提交评估"):
            st.success("评估完成！")
            st.json({
                "overall_score": 82,
                "feedback": ["逻辑清晰", "表达流畅"]
            })

if __name__ == "__main__":
    main()
