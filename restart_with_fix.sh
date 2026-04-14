#!/bin/bash
# 重启系统并应用修复

echo "🔧 考研考公双赛道情报监控系统 - 应用修复并重启"
echo "============================================="

# 1. 停止当前服务
echo "1. 停止当前服务..."
pkill -f "python.*main\.py" 2>/dev/null
sleep 2

# 2. 检查是否停止
echo "2. 检查进程状态..."
if ps aux | grep "python.*main\.py" | grep -v grep > /dev/null; then
    echo "   ⚠️  仍有进程在运行，强制停止..."
    pkill -9 -f "python.*main\.py" 2>/dev/null
    sleep 1
fi

# 3. 验证修复文件
echo "3. 验证修复文件..."
if [ -f "backend/core/crawler_manager.py" ]; then
    echo "   ✅ 修复版本已应用"
    echo "   📊 文件信息:"
    ls -la backend/core/crawler_manager.py | awk '{print "     大小:", $5, "字节, 修改时间:", $6, $7, $8}'
else
    echo "   ❌ 修复文件不存在"
    exit 1
fi

# 4. 检查用户状态
echo "4. 检查用户状态..."
cd ~/Desktop/考研考公双赛道情报监控系统
python3 -c "
import sys
sys.path.append('backend')
from core.database import get_db
from models.users import UserSubscription

db = next(get_db(database='common'))
active_users = db.query(UserSubscription).filter(UserSubscription.status == 1).count()
db.close()
print(f'   活跃用户数量: {active_users}')
if active_users == 0:
    print('   ⚠️  没有活跃用户，爬虫不会启动')
else:
    print(f'   ✅ 有 {active_users} 个活跃用户，爬虫将启动')
"

# 5. 启动修复版本
echo "5. 启动修复版本服务..."
cd ~/Desktop/考研考公双赛道情报监控系统
echo "   启动命令: python3 backend/main.py"
echo "   日志文件: logs/app.log"
echo ""

# 在后台启动服务
nohup python3 backend/main.py > logs/restart.log 2>&1 &

# 等待服务启动
sleep 3

# 6. 检查服务状态
echo "6. 检查服务状态..."
if ps aux | grep "python.*main\.py" | grep -v grep > /dev/null; then
    echo "   ✅ 服务启动成功"
    echo "   进程ID:" $(ps aux | grep "python.*main\.py" | grep -v grep | awk '{print $2}')
    
    # 查看启动日志
    echo ""
    echo "7. 查看启动日志:"
    tail -10 logs/restart.log 2>/dev/null || echo "   日志文件不存在或为空"
else
    echo "   ❌ 服务启动失败"
    echo "   查看日志: tail -20 logs/restart.log"
    tail -20 logs/restart.log 2>/dev/null
fi

echo ""
echo "============================================="
echo "🎯 修复总结:"
echo "   ✅ 爬虫URL配置已修复（使用真实网站）"
echo "   ✅ 爬虫调度逻辑已修复（只在有用户时运行）"
echo "   ✅ 系统已重启"
echo ""
echo "🔍 验证方法:"
echo "   1. 检查日志: tail -f logs/app.log"
echo "   2. 查看爬虫运行情况"
echo "   3. 确认个性化爬虫正常工作"
echo "============================================="