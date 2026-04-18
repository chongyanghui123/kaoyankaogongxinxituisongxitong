#!/usr/bin/env python3

import os
import sys

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import get_db_kaogong
from models.kaogong import KaogongInfo

def clear_kaogong_data():
    """清空考公测试数据"""
    db = next(get_db_kaogong())
    try:
        # 删除所有考公测试数据
        deleted_count = db.query(KaogongInfo).delete()
        db.commit()
        print(f"成功删除 {deleted_count} 条考公测试数据")
    except Exception as e:
        print(f"清空考公测试数据失败: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """主函数"""
    print("开始清空考公测试数据...")
    clear_kaogong_data()
    print("考公测试数据清空完成！")

if __name__ == "__main__":
    main()
