#!/bin/bash
# 考研考公双赛道系统 - Celery启动脚本

echo "🦞 启动考研考公双赛道情报监控系统 - Celery服务"
echo "============================================================"

# 检查环境变量
if [ ! -f ".env" ]; then
    echo "❌ 错误: .env 文件不存在"
    exit 1
fi

# 启动Celery worker和beat
echo "\n🚀 启动Celery worker..."
celery -A core.celery_app worker --loglevel=info --concurrency=4 &

WORKER_PID=$!
echo "✅ Celery worker 已启动，PID: $WORKER_PID"

echo "\n🚀 启动Celery beat..."
celery -A core.celery_app beat --loglevel=info --schedule=celerybeat-schedule &

BEAT_PID=$!
echo "✅ Celery beat 已启动，PID: $BEAT_PID"

echo "\n📅 配置定时任务..."
echo "   - 每小时检查一次服务到期时间"
echo "   - 每小时发送一次推送通知"

echo "\n✅ Celery服务已全部启动"
echo "============================================================"
echo "按 Ctrl+C 停止所有服务"

# 等待用户输入
wait $WORKER_PID $BEAT_PID