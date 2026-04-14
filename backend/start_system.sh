#!/bin/bash
# 考研考公双赛道系统 - AI功能启动脚本

echo "🦞 启动考研考公双赛道情报监控系统"
echo "============================================================"

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    exit 1
fi

# 检查AI配置
if grep -q "AI_ENABLED=true" .env; then
    echo "✅ AI功能已启用"
    echo "   模型: $(grep VOLCENGINE_MODEL .env | cut -d= -f2)"
    echo "   API端点: $(grep VOLCENGINE_API_URL .env | cut -d= -f2)"
else
    echo "⚠️  AI功能未启用"
    echo "   如需启用，请在 .env 中设置 AI_ENABLED=true"
fi

# 启动系统
echo "\n🚀 启动系统..."
python3 main.py
