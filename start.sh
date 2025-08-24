#!/bin/bash

echo "🚀 启动 TalentIntervuAI 项目..."

# 检查Python版本
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.8" | bc -l) -eq 0 ]]; then
    echo "❌ 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装后端依赖
echo "📥 安装后端依赖..."
cd backend
pip install -r requirements.txt
cd ..

# 安装前端依赖
echo "📥 安装前端依赖..."
cd frontend
pip install -r requirements.txt
cd ..

# 检查环境变量配置
if [ ! -f "config/.env" ]; then
    echo "⚠️  警告: 未找到配置文件 config/.env"
    echo "请复制 config/env_example.txt 为 config/.env 并配置OpenAI API Key"
    echo ""
fi

echo ""
echo "🎯 启动说明:"
echo "1. 启动后端服务: cd backend && python main.py"
echo "2. 启动前端应用: cd frontend && streamlit run main.py"
echo ""
echo "📖 访问地址:"
echo "- 前端应用: http://localhost:8501"
echo "- 后端API: http://localhost:8000"
echo "- API文档: http://localhost:8000/docs"
echo ""

# 询问是否立即启动服务
read -p "是否立即启动服务? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🚀 启动后端服务..."
    cd backend
    python main.py &
    backend_pid=$!
    cd ..
    
    echo "🚀 启动前端应用..."
    cd frontend
    streamlit run main.py &
    frontend_pid=$!
    cd ..
    
    echo "✅ 服务已启动!"
    echo "后端PID: $backend_pid"
    echo "前端PID: $frontend_pid"
    echo ""
    echo "按 Ctrl+C 停止所有服务"
    
    # 等待用户中断
    trap "echo '🛑 停止服务...'; kill $backend_pid $frontend_pid 2>/dev/null; exit" INT
    wait
fi

echo "👋 再见!"
